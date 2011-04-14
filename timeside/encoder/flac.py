# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2009 Guillaume Pellerin <yomguy@parisson.com>

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

# Author: Guillaume Pellerin <yomguy@parisson.com>

from timeside.core import Processor, implements, interfacedoc
from timeside.api import IEncoder
from numpy import array, frombuffer, getbuffer, float32

import pygst
pygst.require('0.10')
import gst
import gobject
gobject.threads_init()

class FlacEncoder(Processor):
    """ gstreamer-based FLAC encoder """
    implements(IEncoder)

    def __init__(self, output,  streaming=False):
        if isinstance(output, basestring):
            self.filename = output
        else:
            self.filename = None
        self.streaming = streaming
        
        if not self.filename and not self.streaming:
            raise Exception('Must give an output')
        
        self.eod = False

    @interfacedoc
    def setup(self, channels=None, samplerate=None, nframes=None):
        super(FlacEncoder, self).setup(channels, samplerate, nframes)
        # TODO open file for writing
        # the output data format we want        
        self.pipe = ''' appsrc name=src ! audioconvert 
                        ! flacenc '''
                        
        if self.filename and self.streaming:            
            self.pipe += ''' ! tee name=t
            ! queue ! filesink location=%s
            t. ! queue ! appsink name=app sync=False
            ''' % self.filename
            
        elif self.filename :
            self.pipe += '! filesink location=%s ' % self.filename
        else:
            self.pipe += '! appsink name=app sync=False '
            
        self.pipeline = gst.parse_launch(self.pipe)
        # store a pointer to appsrc in our encoder object
        self.src = self.pipeline.get_by_name('src')
        # store a pointer to appsink in our encoder object
        self.app = self.pipeline.get_by_name('app')
        
        srccaps = gst.Caps("""audio/x-raw-float,
            endianness=(int)1234,
            channels=(int)%s,
            width=(int)32,
            rate=(int)%d""" % (int(channels), int(samplerate)))
        self.src.set_property("caps", srccaps)

        # start pipeline
        self.pipeline.set_state(gst.STATE_PLAYING)

    @staticmethod
    @interfacedoc
    def id():
        return "gst_flac_enc"

    @staticmethod
    @interfacedoc
    def description():
        return "FLAC GStreamer based encoder"

    @staticmethod
    @interfacedoc
    def format():
        return "FLAC"

    @staticmethod
    @interfacedoc
    def file_extension():
        return "flac"

    @staticmethod
    @interfacedoc
    def mime_type():
        return 'audio/x-flac'

    @interfacedoc
    def set_metadata(self, metadata):
        #TODO:
        pass

    @interfacedoc
    def process(self, frames, eod=False):
        self.eod = eod
        buf = self.numpy_array_to_gst_buffer(frames)
        self.src.emit('push-buffer', buf)
        if self.streaming:
            self.chunk = self.app.emit('pull-buffer')
        return frames, eod

    def numpy_array_to_gst_buffer(self, frames):
        """ gstreamer buffer to numpy array conversion """
        buf = gst.Buffer(getbuffer(frames))
        return buf

