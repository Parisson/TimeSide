# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Paul Brossier <piem@piem.org>
# Copyright (c) 2010 Guillaume Pellerin <yomguy@parisson.com>

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


from timeside.core import Processor, implements, interfacedoc
from timeside.api import IEncoder
from numpy import array, frombuffer, getbuffer, float32

import pygst
pygst.require('0.10')
import gst
import gobject
gobject.threads_init ()


class AacEncoder(Processor):
    """ gstreamer-based AAC encoder """
    implements(IEncoder)

    def __init__(self, output):
        self.file = None
        if isinstance(output, basestring):
            self.filename = output
        else:
            raise Exception("Streaming not supported")

    @interfacedoc
    def setup(self, channels=None, samplerate=None, nframes=None):
        super(AacEncoder, self).setup(channels, samplerate, nframes)
        # TODO open file for writing
        # the output data format we want
        pipeline = gst.parse_launch(''' appsrc name=src
            ! audioconvert
            ! faac
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
        return "gst_aac_enc"

    @staticmethod
    @interfacedoc
    def description():
        return "AAC GStreamer based encoder"

    @staticmethod
    @interfacedoc
    def format():
        return "AAC"

    @staticmethod
    @interfacedoc
    def file_extension():
        return "m4a"

    @staticmethod
    @interfacedoc
    def mime_type():
        return "audio/x-m4a"

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



