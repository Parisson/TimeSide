#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008 MUSIC TECHNOLOGY GROUP (MTG)
#                    UNIVERSITAT POMPEU FABRA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Bram de Jong <bram.dejong at domain.com where domain in gmail>
#   Guillaume Pellerin <yomguy@parisson.com>


import math
import numpy

try:
    from PIL import Image, ImageDraw
except ImportError:
    import Image
    import ImageDraw

from timeside.core import Processor, implements, interfacedoc, abstract
from timeside.core import FixedSizeInputAdapter
from timeside.api import IGrapher
from . utils import smooth, im_watermark, normalize


class Spectrum(object):

    """ FFT based frequency analysis of audio frames."""

    def __init__(self, fft_size, samplerate, blocksize,
                 totalframes, lower, higher, window_function=None):
        self.fft_size = fft_size
        self.window = window_function(self.fft_size)
        self.window_function = window_function
        self.spectrum_range = None
        self.lower = lower
        self.higher = higher
        self.blocksize = blocksize
        self.lower_log = math.log10(self.lower)
        self.higher_log = math.log10(self.higher)
        self.clip = lambda val, low, high: min(high, max(low, val))
        self.totalframes = totalframes
        self.samplerate = samplerate
        self.window_function = window_function
        self.window = self.window_function(self.blocksize)
        # Hanning window by default
        if self.window_function:
            self.window = self.window_function(self.blocksize)
        else:
            self.window_function = numpy.hanning
            self.window = self.window_function(self.blocksize)

    def process(self, frames, eod, spec_range=120.0):
        """ Returns a tuple containing the spectral centroid and
        the spectrum (dB scales) of the input audio frames.
        FFT window sizes are adatable to the input frame size."""

        samples = frames[:, 0]
        nsamples = len(frames[:, 0])
        if nsamples != self.blocksize:
            self.window = self.window_function(nsamples)
        samples *= self.window

        while nsamples > self.fft_size:
            self.fft_size = 2 * self.fft_size

        zeros_p = numpy.zeros(self.fft_size / 2 - int(nsamples / 2))
        if nsamples % 2:
            zeros_n = numpy.zeros(self.fft_size / 2 - int(nsamples / 2) - 1)
        else:
            zeros_n = numpy.zeros(self.fft_size / 2 - int(nsamples / 2))
        samples = numpy.concatenate((zeros_p, samples, zeros_n), axis=0)

        fft = numpy.fft.fft(samples)
        # normalized abs(FFT) between 0 and 1
        spectrum = numpy.abs(fft[:fft.shape[0] / 2 + 1]) / float(nsamples)
        length = numpy.float64(spectrum.shape[0])

        # scale the db spectrum from [- spec_range db ... 0 db] > [0..1]
        db_spectrum = ((20 * (numpy.log10(spectrum + 1e-30)))
                       .clip(-spec_range, 0.0) + spec_range) / spec_range
        energy = spectrum.sum()
        spectral_centroid = 0

        if energy > 1e-20:
            # calculate the spectral centroid
            if self.spectrum_range is None:
                self.spectrum_range = numpy.arange(length)
            spectral_centroid = (spectrum * self.spectrum_range).sum() / \
                (energy * (length - 1)) * \
                self.samplerate * 0.5
            # clip > log10 > scale between 0 and 1
            spectral_centroid = (math.log10(self.clip(spectral_centroid,
                                                      self.lower,
                                                      self.higher)) -
                                 self.lower_log) / (self.higher_log -
                                                    self.lower_log)

        return (spectral_centroid, db_spectrum)


class Grapher(Processor):

    '''
    Generic abstract class for the graphers
    '''

    type = 'grapher'

    fft_size = 0x1000
    frame_cursor = 0
    pixel_cursor = 0
    lower_freq = 20

    implements(IGrapher)
    abstract()

    def __init__(self, width=1024, height=256, bg_color=None, color_scheme='default'):
        super(Grapher, self).__init__()
        self.bg_color = bg_color
        self.color_scheme = color_scheme
        self.graph = None
        self.image_width = width
        self.image_height = height
        self.bg_color = bg_color
        self.color_scheme = color_scheme
        self.previous_x, self.previous_y = None, None

    @staticmethod
    def id():
        return "generic_grapher"

    @staticmethod
    def name():
        return "Generic grapher"

    def set_colors(self, bg_color, color_scheme):
        self.bg_color = bg_color
        self.color_color_scheme = color_scheme

    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(Grapher, self).setup(
            channels, samplerate, blocksize, totalframes)
        self.sample_rate = samplerate
        self.higher_freq = self.sample_rate / 2
        self.block_size = blocksize
        self.total_frames = totalframes
        self.image = Image.new(
            "RGBA", (self.image_width, self.image_height), self.bg_color)
        self.samples_per_pixel = self.total_frames / float(self.image_width)
        self.buffer_size = int(round(self.samples_per_pixel, 0))
        self.pixels_adapter = FixedSizeInputAdapter(
            self.buffer_size, 1, pad=False)
        self.pixels_adapter_totalframes = self.pixels_adapter.blocksize(
            self.total_frames)
        self.spectrum = Spectrum(
            self.fft_size, self.sample_rate, self.block_size, self.total_frames,
            self.lower_freq, self.higher_freq, numpy.hanning)
        self.pixel = self.image.load()
        self.draw = ImageDraw.Draw(self.image)

    @interfacedoc
    def render(self, output=None):
        if output:
            try:
                self.image.save(output)
            except AttributeError:
                print "Pixel %s x %d" % (self.image_width, self.image_height)
                self.image.savefig(output, dpi=341)
            return
        return self.image

    def watermark(self, text, font=None, color=(255, 255, 255), opacity=.6, margin=(5, 5)):
        self.image = im_watermark(
            self.image, text, color=color, opacity=opacity, margin=margin)

    def draw_peaks(self, x, peaks, line_color):
        """Draw 2 peaks at x"""

        y1 = self.image_height * 0.5 - peaks[0] * (self.image_height - 4) * 0.5
        y2 = self.image_height * 0.5 - peaks[1] * (self.image_height - 4) * 0.5

        if self.previous_y:
            self.draw.line(
                [self.previous_x, self.previous_y, x, y1, x, y2], line_color)
        else:
            self.draw.line([x, y1, x, y2], line_color)

        self.draw_anti_aliased_pixels(x, y1, y2, line_color)
        self.previous_x, self.previous_y = x, y2

    def draw_peaks_inverted(self, x, peaks, line_color):
        """Draw 2 inverted peaks at x"""

        y1 = self.image_height * 0.5 - peaks[0] * (self.image_height - 4) * 0.5
        y2 = self.image_height * 0.5 - peaks[1] * (self.image_height - 4) * 0.5

        if self.previous_y and x < self.image_width - 1:
            if y1 < y2:
                self.draw.line((x, 0, x, y1), line_color)
                self.draw.line((x, self.image_height, x, y2), line_color)
            else:
                self.draw.line((x, 0, x, y2), line_color)
                self.draw.line((x, self.image_height, x, y1), line_color)
        else:
            self.draw.line((x, 0, x, self.image_height), line_color)
        self.draw_anti_aliased_pixels(x, y1, y2, line_color)
        self.previous_x, self.previous_y = x, y1

    def draw_anti_aliased_pixels(self, x, y1, y2, color):
        """ vertical anti-aliasing at y1 and y2 """

        y_max = max(y1, y2)
        y_max_int = int(y_max)
        alpha = y_max - y_max_int

        if alpha > 0.0 and alpha < 1.0 and y_max_int + 1 < self.image_height:
            current_pix = self.pixel[int(x), y_max_int + 1]
            r = int((1 - alpha) * current_pix[0] + alpha * color[0])
            g = int((1 - alpha) * current_pix[1] + alpha * color[1])
            b = int((1 - alpha) * current_pix[2] + alpha * color[2])
            self.pixel[x, y_max_int + 1] = (r, g, b)

        y_min = min(y1, y2)
        y_min_int = int(y_min)
        alpha = 1.0 - (y_min - y_min_int)

        if alpha > 0.0 and alpha < 1.0 and y_min_int - 1 >= 0:
            current_pix = self.pixel[x, y_min_int - 1]
            r = int((1 - alpha) * current_pix[0] + alpha * color[0])
            g = int((1 - alpha) * current_pix[1] + alpha * color[1])
            b = int((1 - alpha) * current_pix[2] + alpha * color[2])
            self.pixel[x, y_min_int - 1] = (r, g, b)

    def draw_peaks_contour(self):
        contour = self.contour.copy()
        contour = smooth(contour, window_len=16)
        contour = normalize(contour)

        # Scaling
        #ratio = numpy.mean(contour)/numpy.sqrt(2)
        ratio = 1
        contour = normalize(numpy.expm1(contour / ratio)) * (1 - 10 ** -6)

        # Spline
        #contour = cspline1d(contour)
        #contour = cspline1d_eval(contour, self.x, dx=self.dx1, x0=self.x[0])

        if self.symetry:
            height = int(self.image_height / 2)
        else:
            height = self.image_height

        # Multicurve rotating
        for i in range(0, self.ndiv):
            self.previous_x, self.previous_y = None, None

            bright_color = int(255 * (1 - float(i) / (self.ndiv * 2)))
            bright_color = 255 - bright_color + self.color_offset
            #line_color = self.color_lookup[int(self.centroids[j]*255.0)]
            line_color = (bright_color, bright_color, bright_color)

            # Linear
            #contour = contour*(1.0-float(i)/self.ndiv)
            #contour = contour*(1-float(i)/self.ndiv)

            # Cosinus
            contour = contour * \
                numpy.arccos(float(i) / self.ndiv) * 2 / numpy.pi
            #contour = self.contour*(1-float(i)*numpy.arccos(float(i)/self.ndiv)*2/numpy.pi/self.ndiv)
            #contour = contour + ((1-contour)*2/numpy.pi*numpy.arcsin(float(i)/self.ndiv))

            curve = (height - 1) * contour
            #curve = contour*(height-2)/2+height/2

            for x in self.x:
                x = int(x)
                y = curve[x]
                if not x == 0:
                    if not self.symetry:
                        self.draw.line(
                            [self.previous_x, self.previous_y, x, y], line_color)
                        self.draw_anti_aliased_pixels(x, y, y, line_color)
                    else:
                        self.draw.line(
                            [self.previous_x, self.previous_y + height, x, y + height], line_color)
                        self.draw_anti_aliased_pixels(
                            x, y + height, y + height, line_color)
                        self.draw.line(
                            [self.previous_x, -self.previous_y + height, x, -y + height], line_color)
                        self.draw_anti_aliased_pixels(
                            x, -y + height, -y + height, line_color)
                else:
                    if not self.symetry:
                        self.draw.point((x, y), line_color)
                    else:
                        self.draw.point((x, y + height), line_color)
                self.previous_x, self.previous_y = x, y


if __name__ == "__main__":
    import doctest
    doctest.testmod()
