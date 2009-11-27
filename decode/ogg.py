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
from mutagen.oggvorbis import OggVorbis

class OggDecoder(DecoderCore):
    """Defines methods to decode from OGG Vorbis"""

    implements(IDecoder)

    @staticmethod
    def id():
        return "oggdec"
    
    def format(self):
        return 'OggVorbis'

    def file_extension(self):
        return 'ogg'

    def mime_type(self):
        return 'application/ogg'

    def description(self):
        return """
        Vorbis is a free software / open source project headed by the Xiph.Org
        Foundation (formerly Xiphophorus company). The project produces an audio
        format specification and software implementation (codec) for lossy audio
        compression. Vorbis is most commonly used in conjunction with the Ogg
        container format and it is therefore often referred to as Ogg Vorbis.
        (source Wikipedia)
        """

    def get_file_info(self):
        try:
            file_out1, file_out2 = os.popen4('ogginfo "'+self.dest+'"')
            info = []
            for line in file_out2.readlines():
                info.append(clean_word(line[:-1]))
            self.info = info
            return self.info
        except:
            raise IOError('DecoderError: file does not exist.')

