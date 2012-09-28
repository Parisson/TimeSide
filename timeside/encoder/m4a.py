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
from timeside.encoder.gstutils import *

class AacEncoder(GstEncoder):
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

        self.streaming = False
        self.pipe = ''' appsrc name=src
            ! audioconvert
            ! faac
            ! filesink location=%s ''' % self.filename

        # start pipeline
        self.start_pipeline(channels, samplerate)

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
