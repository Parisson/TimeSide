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

# Author: Guillaume Pellerin <yomguy@parisson.com>

import os
import string
import subprocess

from timeside.decode.core import *
from timeside.decode.api import IDecoder


class Mp3Decoder(DecoderCore):
    """Defines methods to decode from MP3"""

    implements(IDecoder)

    def __init__(self):
        self.command = 'sox -t mp3 "%s" -q -b 16 -r 44100 -t wav -c2 - '

    @staticmethod
    def id():
        return "mp3dec"
    
    def format(self):
        return 'MP3'

    def file_extension(self):
        return 'mp3'

    def mime_type(self):
        return 'audio/mpeg'

    def description(self):
        return """
        MPEG-1 Audio Layer 3, more commonly referred to as MP3, is a patented
        digital audio encoding format using a form of lossy data compression.
        It is a common audio format for consumer audio storage, as well as a
        de facto standard of digital audio compression for the transfer and
        playback of music on digital audio players. MP3 is an audio-specific
        format that was designed by the Moving Picture Experts Group as part
        of its MPEG-1 standard. (source Wikipedia)
        """

    def get_file_info(self):
        try:
            file_out1, file_out2 = os.popen4('mp3info "'+self.dest+'"')
            info = []
            for line in file_out2.readlines():
                info.append(clean_word(line[:-1]))
            self.info = info
            return self.info
        except:
            raise IOError('DecoderError: file does not exist.')

