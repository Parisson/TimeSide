#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2007-2011 Parisson
# Copyright (c) 2007 Olivier Guilyardi <olivier@samalyse.com>
# Copyright (c) 2007-2011 Guillaume Pellerin <pellerin@parisson.com>
# Copyright (c) 2010-2011 Paul Brossier <piem@piem.org>
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

# Authors: Paul Brossier <piem@piem.org>
#          Guilaume Pellerin <yomguy@parisson.com>

from timeside.core import Processor, implements, interfacedoc
from timeside.api import IDecoder
from timeside.encoder.gstutils import *

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
        return "gstreamerdec"

    def setup(self, channels = None, samplerate = None, nframes = None):
        # the output data format we want
        blocksize = 8*1024
        uri = self.uri
        self.pipe = ''' uridecodebin uri=%(uri)s
                  ! audioconvert
                  ! appsink name=sink blocksize=%(blocksize)s sync=False async=True emit-signals=True
                  ''' % locals()
        self.pipeline = gst.parse_launch(self.pipe)

        sink_caps = gst.Caps("""audio/x-raw-float,
            endianness=(int)1234,
            channels=(int)%s,
            width=(int)32,
            rate=(int)%d""" % (int(self.audiochannels), int(self.audiorate)))

        self.sink = self.pipeline.get_by_name('sink')
        self.sink.set_property("caps", sink_caps)
        self.sink.set_property('emit-signals', True)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_message)

        # start pipeline
        self.pipeline.set_state(gst.STATE_PLAYING)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.pipeline.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_ERROR:
            self.pipeline.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
        elif t == gst.MESSAGE_TAG:
            # TODO
            # msg.parse_tags()
            pass

    @interfacedoc
    def process(self, frames = None, eod = False):
        self.eod = eod
        if self.eod:
            self.src.emit('end-of-stream')
        try:
            buf = self.sink.emit('pull-buffer')
        except SystemError, e:
            # should never happen
            print 'SystemError', e
            return array([0.]), True
        if buf == None:
            return array([0.]), True
        return gst_buffer_to_numpy_array(buf, self.audiochannels), self.eod

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
    def release(self):
        while self.bus.have_pending():
          self.bus.pop()

    def __del__(self):
        self.release()

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
        else:
            self.uri = uri

    @interfacedoc
    def format(self):
        # TODO check
        if self.mimetype == 'application/x-id3':
            self.mimetype = 'audio/mpeg'
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

    def duration(self):
        return self.duration

    ## gst.extend discoverer

    def discover(self, path):
        """ gstreamer based helper function to get file attributes """
        from gst.extend import discoverer
        d = discoverer.Discoverer(path, timeout = self.MAX_DISCOVERY_TIME)
        d.connect('discovered', self.discovered)
        self.bus = d.get_bus()
        self.bus.add_signal_watch()
        self.pipeline = d
        self.bus.connect("message", self.on_message)

        # start pipeline
        d.discover()
        self.pipeline.set_state(gst.STATE_PLAYING)
        while self.bus.have_pending():
            self.bus.pop()
        d.print_info()

    def discovered(self, d, is_media):
        """ gstreamer based helper executed upon discover() completion """
        from math import ceil
        if is_media and d.is_audio:
            # copy the discoverer attributes to self
            self.audiorate = d.audiorate
            self.mimetype= d.mimetype
            self.audiochannels = d.audiochannels
            self.audiowidth = d.audiowidth
            # conversion from time in nanoseconds to seconds
            self.duration = d.audiolength * 1.e-9
            # conversion from time in nanoseconds to frames
            self.audionframes = int ( ceil (d.audiorate * d.audiolength * 1.e-9) )
            # copy tags
            self.tags = d.tags
        elif not d.is_audio:
            print "error, no audio found!"
        else:
            print "fail", path
        self.pipeline.set_state(gst.STATE_NULL)
