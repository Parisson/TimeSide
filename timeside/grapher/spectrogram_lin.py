# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2010 Guillaume Pellerin <yomguy@parisson.com>
# Copyright (c) 2010 Olivier Guilyardi <olivier@samalyse.com>

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


from timeside.core import implements, interfacedoc
from timeside.api import IGrapher
#from timeside.grapher.core import *
from timeside.grapher.spectrogram_log import SpectrogramLog


class SpectrogramLinear(SpectrogramLog):

    """ Builds a PIL image representing a spectrogram of the audio stream (level vs. frequency vs. time).
    Adds pixels iteratively thanks to the adapter providing fixed size frame buffers."""

    implements(IGrapher)

    @interfacedoc
    def __init__(self, width=1024, height=256, bg_color=(0, 0, 0), color_scheme='default'):
        super(SpectrogramLinear, self).__init__(
            width, height, bg_color, color_scheme)

    @staticmethod
    @interfacedoc
    def id():
        return "spectrogram_lin"

    @staticmethod
    @interfacedoc
    def name():
        return "Spectrogram Lin"

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(SpectrogramLinear, self).setup(
            channels, samplerate, blocksize, totalframes)

    def set_scale(self):
        """generate the lookup which translates y-coordinate to fft-bin"""

        f_min = float(self.lower_freq)
        f_max = float(self.higher_freq)
        y_min = f_min
        y_max = f_max
        for y in range(self.image_height):
            freq = y_min + y / (self.image_height - 1.0) * (y_max - y_min)
            fft_bin = freq / f_max * (self.fft_size / 2 + 1)
            if fft_bin < self.fft_size / 2:
                alpha = fft_bin - int(fft_bin)
                self.y_to_bin.append((int(fft_bin), alpha * 255))
