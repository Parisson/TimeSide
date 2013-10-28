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


from timeside.core import Processor, implements, interfacedoc, FixedSizeInputAdapter
from timeside.api import IGrapher
from timeside.grapher.core import *


class Spectrogram(Grapher):
    """ Builds a PIL image representing a spectrogram of the audio stream (level vs. frequency vs. time).
    Adds pixels iteratively thanks to the adapter providing fixed size frame buffers."""

    implements(IGrapher)

    @interfacedoc
    def __init__(self, width=1024, height=256, bg_color=(0,0,0), color_scheme='default'):
        super(Spectrogram, self).__init__(width, height, bg_color, color_scheme)
        self.colors = default_color_schemes[color_scheme]['spectrogram']
        self.pixels = []

        # generate the lookup which translates y-coordinate to fft-bin
        self.y_to_bin = []
        f_min = float(self.lower_freq)
        f_max = float(self.higher_freq)
        y_min = math.log10(f_min)
        y_max = math.log10(f_max)
        for y in range(self.image_height):
            freq = math.pow(10.0, y_min + y / (self.image_height - 1.0) *(y_max - y_min))
            bin = freq / 22050.0 * (self.fft_size/2 + 1)
            if bin < self.fft_size/2:
                alpha = bin - int(bin)
                self.y_to_bin.append((int(bin), alpha * 255))

    @staticmethod
    @interfacedoc
    def id():
        return "spectrogram"

    @staticmethod
    @interfacedoc
    def name():
        return "Spectrogram"

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(Spectrogram, self).setup(channels, samplerate, blocksize, totalframes)
        self.spectrum = Spectrum(self.fft_size, self.totalframes, self.samplerate,
                                 self.lower_freq, self.higher_freq, numpy.hanning)
        self.image = Image.new("P", (self.image_height, self.image_width))
        self.image.putpalette(interpolate_colors(self.colors, True))

    def draw_spectrum(self, x, spectrum):
        for (index, alpha) in self.y_to_bin:
            self.pixels.append( int( ((255.0-alpha) * spectrum[index] + alpha * spectrum[index + 1] )) )
        for y in range(len(self.y_to_bin), self.image_height):
            self.pixels.append(0)

    @interfacedoc
    def process(self, frames, eod=False):
        if len(frames) != 1:
            buffer = frames[:,0].copy()
            buffer.shape = (len(buffer),1)
            for samples, end in self.pixels_adapter.process(buffer, eod):
                if self.pixel_cursor < self.image_width:
                    (spectral_centroid, db_spectrum) = self.spectrum.process(samples, True)
                    self.draw_spectrum(self.pixel_cursor, db_spectrum)
                    self.pixel_cursor += 1
        return frames, eod

    def render(self, filename):
        """ Apply last 2D transforms and write all pixels to the file. """
        self.image.putdata(self.pixels)
        self.image.transpose(Image.ROTATE_90).save(filename)
