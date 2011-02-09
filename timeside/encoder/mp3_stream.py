    # -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Parisson SARL
# Copyright (c) 2006-2007 Guillaume Pellerin <pellerin@parisson.com>

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

# Authors: Guillaume Pellerin <yomguy@parisson.com>
#          Paul Brossier <piem@piem.org>

from timeside.core import Processor, implements, interfacedoc
from timeside.api import IEncoder
from numpy import array, frombuffer, getbuffer, float32

import pygst
pygst.require('0.10')
import gst
import gobject
gobject.threads_init()


class Mp3EncoderStream(Processor):
    """ gstreamer-based streaming mp3 encoder with an appsink tee"""
    implements(IEncoder)

    def __init__(self, output=None):
#        self.file = None
        self.filename = output
        
    @interfacedoc
    def setup(self, channels=None, samplerate=None, nframes=None):
        super(Mp3EncoderStream, self).setup(channels, samplerate, nframes)
        #TODO: open file for writing
        # the output data format we want
        
        pipe = '''appsrc name=src ! audioconvert 
                  ! lame name=enc vbr=0 bitrate=256 ! id3v2mux 
                  '''
        if self.filename:
            pipe += '''
            ! queue2 name=q0 ! tee name=tee
            tee. ! queue name=q1 ! appsink name=app
            tee. ! queue name=q2 ! filesink location=%s
            ''' % self.filename
        else:
            pipe += '! appsink name=app'
            
        pipeline = gst.parse_launch(pipe)
        # store a pointer to appsrc in our encoder object
        self.src = pipeline.get_by_name('src')
        # store a pointer to appsink in our encoder object
        self.app = pipeline.get_by_name('app')
        
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
        return "gst_mp3_enc_stream"

    @staticmethod
    @interfacedoc
    def description():
        return "MP3 GStreamer based encoder and streamer"

    @staticmethod
    @interfacedoc
    def format():
        return "MP3"

    @staticmethod
    @interfacedoc
    def file_extension():
        return "mp3"

    @staticmethod
    @interfacedoc
    def mime_type():
        return "audio/mpeg"

    @interfacedoc
    def set_metadata(self, metadata):
        #TODO: 
        pass

    @interfacedoc
    def process(self, frames, eod=False):
        buf = self.numpy_array_to_gst_buffer(frames)
        self.src.emit('push-buffer', buf)
        appbuffer = self.app.emit('pull-buffer')
        if eod: self.src.emit('end-of-stream')
        return appbuffer, eod
        
    def numpy_array_to_gst_buffer(self, frames):
        """ gstreamer buffer to numpy array conversion """
        buf = gst.Buffer(getbuffer(frames))
        return buf

