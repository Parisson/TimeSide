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

from timeside.core import *
from timeside.api import IGrapher
from tempfile import NamedTemporaryFile
from timeside.grapher.core import *

class SpectrogramGrapherAudiolab(Processor):
    """Spectrogram graph driver (python style thanks to wav2png.py and scikits.audiolab)"""

    implements(IGrapher)

    bg_color = None
    color_scheme = None

    @staticmethod
    def id():
        return "spectrogram"

    def name(self):
        return "Spectrogram (audiolab)"

    def set_colors(self, background=None, scheme=None):
        self.bg_color = background
        self.color_scheme = scheme

    def render(self, media_item, width=None, height=None, options=None):
        """Generator that streams the spectrogram as a PNG image with a python method"""

        wav_file = media_item
        pngFile = NamedTemporaryFile(suffix='.png')

        if not width == None:
            image_width = width
        else:
            image_width = 1500
        if not height == None:
            image_height = height
        else:
            image_height = 200

        fft_size = 2048
        args = (wav_file, pngFile.name, image_width, image_height, fft_size,
                self.bg_color, self.color_scheme)
        create_spectrogram_png(*args)

        buffer = pngFile.read(0xFFFF)
        while buffer:
            yield buffer
            buffer = pngFile.read(0xFFFF)

        pngFile.close()
