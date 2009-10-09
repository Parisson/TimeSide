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
from timeside.decode.api import IDecoder
from mutagen.flac import FLAC
from tempfile import NamedTemporaryFile

class FlacDecoder(DecoderCore):
    """Defines methods to decode from FLAC"""

    implements(IDecoder)

    def format(self):
        return 'FLAC'

    def file_extension(self):
        return 'flac'

    def mime_type(self):
        return 'application/flac'

    def description(self):
        return """
        Free Lossless Audio Codec (FLAC) is a file format for lossless audio
        data compression. During compression, FLAC does not lose quality from
        the audio stream, as lossy compression formats such as MP3, AAC, and
        Vorbis do. Josh Coalson is the primary author of FLAC.
        (source Wikipedia)
        """

    def get_file_info(self):
        try:
            file1, file2 = os.popen4('metaflac --list "'+self.dest+'"')
            info = []
            for line in file2.readlines():
                info.append(clean_word(line[:-1]))
            self.info = info
            return self.info
        except:
            raise IOError('DecoderError: metaflac is not installed or ' + \
                           'file does not exist.')

