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

import os
import string
import subprocess

from timeside.decode.core import *
from timeside.api import IDecoder

class WavDecoder(DecoderCore):
    """Defines methods to decode from WAV"""

    implements(IDecoder)

    @staticmethod
    def id():
        return "wavdec"
    
    def format(self):
        return 'WAV'

    def file_extension(self):
        return 'wav'

    def mime_type(self):
        return 'audio/x-wav'

    def description(self):
        return """
        WAV (or WAVE), short for Waveform audio format, also known as Audio for
        Windows, is a Microsoft and IBM audio file format standard for storing
        an audio bitstream on PCs. It is an application of the RIFF bitstream
        format method for storing data in “chunks”, and thus is also close to
        the 8SVX and the AIFF format used on Amiga and Macintosh computers,
        respectively. It is the main format used on Windows systems for raw and
        typically uncompressed audio. The usual bitstream encoding is the Pulse
        Code Modulation (PCM) format.
        """

    def get_file_info(self):
        try:
            file1, file2 = os.popen4('wavinfo "'+self.dest+'"')
            info = []
            for line in file2.readlines():
                info.append(clean_word(line[:-1]))
            self.info = info
            return self.info
        except:
            raise IOError('DecoderError: wavinfo id not installed or file does not exist.')

