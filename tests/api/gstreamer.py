# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2009 Parisson
# Copyright (c) 2007 Olivier Guilyardi <olivier@samalyse.com>
# Copyright (c) 2007-2009 Guillaume Pellerin <pellerin@parisson.com>
#
# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

# Author: Paul Brossier <piem@piem.org>

from timeside.core import Processor, implements, interfacedoc
from timeside.api import IDecoder, IEncoder
from numpy import array, frombuffer, getbuffer, float32

import pygst
pygst.require('0.10')
import gst
import gobject
gobject.threads_init ()

class FileDecoder(Processor):
    """ gstreamer-based decoder """
    implements(IDecoder)

    # duration ms, before discovery process times out
    MAX_DISCOVERY_TIME = 3000

    audioformat = None
    audiochannels = None
    audiorate = None
    audionframes = None
    mimetype = ''

    # IProcessor methods

    @staticmethod
    @interfacedoc
    def id():
        return "test_gstreamerdec"

    def setup(self, channels = None, samplerate = None, nframes = None):
        # the output data format we want
        caps = "audio/x-raw-float, width=32"
        pipeline = gst.parse_launch('''uridecodebin uri=%s
            ! audioconvert
            ! %s
            ! appsink name=sink sync=False ''' % (self.uri, caps))
        # store a pointer to appsink in our decoder object 
        self.sink = pipeline.get_by_name('sink')
        # adjust length of emitted buffers
        # self.sink.set_property('blocksize', 0x10000)
        # start pipeline
        pipeline.set_state(gst.STATE_PLAYING)

    @interfacedoc
    def channels(self):
        return  self.audiochannels

    @interfacedoc
    def samplerate(self):
        return self.audiorate 

    @interfacedoc
    def nframes(self):
        return self.audionframes

    @interfacedoc
    def process(self, frames = None, eod = False):
        try:
            buf = self.sink.emit('pull-buffer')
        except SystemError, e:
            # should never happen
            print 'SystemError', e
            return array([0.]), True
        if buf == None:
            return array([0.]), True
        return self.gst_buffer_to_numpy_array(buf), False

    @interfacedoc
    def release(self):
        # nothing to do for now 
        pass

    ## IDecoder methods

    @interfacedoc
    def __init__(self, uri):

        # is this a file? 
        import os.path
        if os.path.exists(uri):
            # get the absolute path
            uri = os.path.abspath(uri)
            # first run the file/uri through the discover pipeline
            self.discover(uri)
            # and make a uri of it
            from urllib import quote
            self.uri = 'file://'+quote(uri)

    @interfacedoc
    def format(self):
        # TODO check
        return self.mimetype

    @interfacedoc
    def encoding(self):
        # TODO check
        return self.mimetype.split('/')[-1]

    @interfacedoc
    def resolution(self):
        # TODO check: width or depth?
        return self.audiowidth 

    @interfacedoc
    def metadata(self):
        # TODO check
        return self.tags

    ## gst.extend discoverer

    def discover(self, path):
        """ gstreamer based helper function to get file attributes """
        from gst.extend import discoverer
        d = discoverer.Discoverer(path, timeout = self.MAX_DISCOVERY_TIME)
        d.connect('discovered', self.discovered)
        self.mainloop = gobject.MainLoop()
        d.discover()
        self.mainloop.run()

    def discovered(self, d, is_media):
        """ gstreamer based helper executed upon discover() completion """
        if is_media and d.is_audio:
            # copy the discoverer attributes to self
            self.audiorate = d.audiorate
            self.mimetype= d.mimetype
            self.audiochannels = d.audiochannels
            self.audiowidth = d.audiowidth
            # conversion from time in nanoseconds to frames 
            from math import ceil
            duration = d.audiorate * d.audiolength * 1.e-9
            self.audionframes = int (ceil ( duration ) )
            self.tags = d.tags
        elif not d.is_audio:
            print "error, no audio found!"
        else:
            print "fail", path
        self.mainloop.quit()

    def gst_buffer_to_numpy_array(self, buf):
        """ gstreamer buffer to numpy array conversion """
        chan = self.audiochannels
        samples = frombuffer(buf.data, dtype=float32) 
        samples.resize([len(samples)/chan, chan])
        return samples

class WavEncoder(Processor):
    """ gstreamer-based encoder """
    implements(IEncoder)

    def __init__(self, output):
        self.file = None
        if isinstance(output, basestring):
            self.filename = output
        else:
            raise Exception("Streaming not supported")

    @interfacedoc
    def setup(self, channels=None, samplerate=None, nframes=None):
        super(WavEncoder, self).setup(channels, samplerate, nframes)
        # TODO open file for writing
        # the output data format we want
        pipeline = gst.parse_launch(''' appsrc name=src
            ! audioconvert
            ! wavenc
            ! filesink location=%s ''' % self.filename)
        # store a pointer to appsink in our encoder object 
        self.src = pipeline.get_by_name('src')
        srccaps = gst.Caps("""audio/x-raw-float,
            endianness=(int)1234,
            channels=(int)%s,
            width=(int)32,
            rate=(int)%d""" % (int(channels), int(samplerate)))
        self.src.set_property("caps", srccaps)

        # start pipeline
        pipeline.set_state(gst.STATE_PLAYING)
        self.pipeline = pipeline

    @staticmethod
    @interfacedoc
    def id():
        return "test_gstreamerenc"

    @staticmethod
    @interfacedoc
    def description():
        return "Gstreamer based encoder"

    @staticmethod
    @interfacedoc
    def file_extension():
        return "wav"

    @staticmethod
    @interfacedoc
    def mime_type():
        return "audio/x-wav"

    @interfacedoc
    def set_metadata(self, metadata):
        #TODO
        pass

    @interfacedoc
    def process(self, frames, eod=False):
        buf = self.numpy_array_to_gst_buffer(frames)
        self.src.emit('push-buffer', buf)
        if eod: self.src.emit('end-of-stream')
        return frames, eod

    def numpy_array_to_gst_buffer(self, frames):
        """ gstreamer buffer to numpy array conversion """
        buf = gst.Buffer(getbuffer(frames))
        return buf
