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


import optparse, math, sys, numpy

try:
    from PIL import ImageFilter, ImageChops, Image, ImageDraw, ImageColor, ImageEnhance
except ImportError:
    import ImageFilter, ImageChops, Image, ImageDraw, ImageColor, ImageEnhance

from timeside.core import FixedSizeInputAdapter
from color_schemes import default_color_schemes
from utils import *

class Spectrum(object):
    """ FFT based frequency analysis of audio frames."""

    def __init__(self, fft_size, nframes, samplerate, lower, higher, window_function=numpy.hanning):
        self.fft_size = fft_size
        self.window = window_function(self.fft_size)
        self.window_function = window_function
        self.spectrum_range = None
        self.lower = lower
        self.higher = higher
        self.lower_log = math.log10(self.lower)
        self.higher_log = math.log10(self.higher)
        self.clip = lambda val, low, high: min(high, max(low, val))
        self.nframes = nframes
        self.samplerate = samplerate

    def process(self, frames, eod, spec_range=120.0):
        """ Returns a tuple containing the spectral centroid and the spectrum (dB scales) of the input audio frames. FFT window sizes are adatable to the input frame size."""

        samples = frames[:,0]
        nsamples = len(samples)
        window = self.window_function(nsamples)
        samples *= window

        while nsamples > self.fft_size:
            self.fft_size = 2 * self.fft_size

        zeros_p = numpy.zeros(self.fft_size/2-int(nsamples/2))
        if nsamples % 2:
            zeros_n = numpy.zeros(self.fft_size/2-int(nsamples/2)-1)
        else:
            zeros_n = numpy.zeros(self.fft_size/2-int(nsamples/2))

        samples = numpy.concatenate((zeros_p, samples, zeros_n), axis=0)

        fft = numpy.fft.fft(samples)
        spectrum = numpy.abs(fft[:fft.shape[0] / 2 + 1]) / float(nsamples) # normalized abs(FFT) between 0 and 1
        length = numpy.float64(spectrum.shape[0])

        # scale the db spectrum from [- spec_range db ... 0 db] > [0..1]
        db_spectrum = ((20*(numpy.log10(spectrum + 1e-30))).clip(-spec_range, 0.0) + spec_range)/spec_range
        energy = spectrum.sum()
        spectral_centroid = 0

        if energy > 1e-20:
            # calculate the spectral centroid
            if self.spectrum_range == None:
                self.spectrum_range = numpy.arange(length)

            spectral_centroid = (spectrum * self.spectrum_range).sum() / (energy * (length - 1)) * self.samplerate * 0.5
            # clip > log10 > scale between 0 and 1
            spectral_centroid = (math.log10(self.clip(spectral_centroid, self.lower, self.higher)) - self.lower_log) / (self.higher_log - self.lower_log)

        return (spectral_centroid, db_spectrum)



class WaveformImage(object):
    """ Builds a PIL image representing a waveform of the audio stream.
    Adds pixels iteratively thanks to the adapter providing fixed size frame buffers.
    Peaks are colored relative to the spectral centroids of each frame packet. """

    def __init__(self, image_width, image_height, nframes, samplerate,
                 fft_size, bg_color, color_scheme):
        self.image_width = image_width
        self.image_height = image_height
        self.nframes = nframes
        self.samplerate = samplerate
        self.fft_size = fft_size
        self.bg_color = bg_color
        self.color_scheme = color_scheme

        if isinstance(color_scheme, dict):
            colors = color_scheme['waveform']
        else:
            colors = default_color_schemes[color_scheme]['waveform']

        self.color_lookup = interpolate_colors(colors)

        self.samples_per_pixel = self.nframes / float(self.image_width)
        self.buffer_size = int(round(self.samples_per_pixel, 0))
        self.pixels_adapter = FixedSizeInputAdapter(self.buffer_size, 1, pad=False)
        self.pixels_adapter_nframes = self.pixels_adapter.blocksize(self.nframes)

        self.lower = 800
        self.higher = 12000
        self.spectrum = Spectrum(self.fft_size, self.nframes, self.samplerate, self.lower, self.higher, numpy.hanning)

        self.image = Image.new("RGBA", (self.image_width, self.image_height), self.bg_color)
        self.pixel = self.image.load()
        self.draw = ImageDraw.Draw(self.image)
        self.previous_x, self.previous_y = None, None
        self.frame_cursor = 0
        self.pixel_cursor = 0

    def peaks(self, samples):
        """ Find the minimum and maximum peak of the samples.
        Returns that pair in the order they were found.
        So if min was found first, it returns (min, max) else the other way around. """
        max_index = numpy.argmax(samples)
        max_value = samples[max_index]

        min_index = numpy.argmin(samples)
        min_value = samples[min_index]

        if min_index < max_index:
            return (min_value, max_value)
        else:
            return (max_value, min_value)

    def color_from_value(self, value):
        """ given a value between 0 and 1, return an (r,g,b) tuple """

        return ImageColor.getrgb("hsl(%d,%d%%,%d%%)" % (int( (1.0 - value) * 360 ), 80, 50))

    def draw_peaks(self, x, peaks, spectral_centroid):
        """ draw 2 peaks at x using the spectral_centroid for color """

        y1 = self.image_height * 0.5 - peaks[0] * (self.image_height - 4) * 0.5
        y2 = self.image_height * 0.5 - peaks[1] * (self.image_height - 4) * 0.5

        line_color = self.color_lookup[int(spectral_centroid*255.0)]

        if self.previous_y:
            self.draw.line([self.previous_x, self.previous_y, x, y1, x, y2], line_color)
        else:
            self.draw.line([x, y1, x, y2], line_color)

        self.previous_x, self.previous_y = x, y2

        self.draw_anti_aliased_pixels(x, y1, y2, line_color)

    def draw_anti_aliased_pixels(self, x, y1, y2, color):
        """ vertical anti-aliasing at y1 and y2 """

        y_max = max(y1, y2)
        y_max_int = int(y_max)
        alpha = y_max - y_max_int

        if alpha > 0.0 and alpha < 1.0 and y_max_int + 1 < self.image_height:
            current_pix = self.pixel[int(x), y_max_int + 1]

            r = int((1-alpha)*current_pix[0] + alpha*color[0])
            g = int((1-alpha)*current_pix[1] + alpha*color[1])
            b = int((1-alpha)*current_pix[2] + alpha*color[2])

            self.pixel[x, y_max_int + 1] = (r,g,b)

        y_min = min(y1, y2)
        y_min_int = int(y_min)
        alpha = 1.0 - (y_min - y_min_int)

        if alpha > 0.0 and alpha < 1.0 and y_min_int - 1 >= 0:
            current_pix = self.pixel[x, y_min_int - 1]

            r = int((1-alpha)*current_pix[0] + alpha*color[0])
            g = int((1-alpha)*current_pix[1] + alpha*color[1])
            b = int((1-alpha)*current_pix[2] + alpha*color[2])

            self.pixel[x, y_min_int - 1] = (r,g,b)

    def process(self, frames, eod):
        if len(frames) != 1:
            buffer = frames[:,0].copy()
            buffer.shape = (len(buffer),1)
            for samples, end in self.pixels_adapter.process(buffer, eod):
                if self.pixel_cursor < self.image_width:
                    (spectral_centroid, db_spectrum) = self.spectrum.process(samples, True)
                    peaks = self.peaks(samples)
                    self.draw_peaks(self.pixel_cursor, peaks, spectral_centroid)
                    self.pixel_cursor += 1

    def watermark(self, text, color=None, opacity=.6, margin=(10,10)):
        self.image = im_watermark(self.image, text, color=color, opacity=opacity, margin=margin)

    def save(self, filename):
        """ Apply last 2D transforms and write all pixels to the file. """

        # middle line (0 for none)
        a = 1
        for x in range(self.image_width):
            self.pixel[x, self.image_height/2] = tuple(map(lambda p: p+a, self.pixel[x, self.image_height/2]))
        self.image.save(filename)

    def release(self):
        pass


class WaveformImageJoyContour(WaveformImage):

    def __init__(self, image_width, image_height, nframes, samplerate,
                 fft_size, bg_color, color_scheme, ndiv=1, symetry=None, color_offset=160):
        WaveformImage.__init__(self, image_width, image_height, nframes, samplerate,
                               fft_size, bg_color, color_scheme)
        self.contour = numpy.zeros(self.image_width)
        self.centroids = numpy.zeros(self.image_width)
        self.ndiv = ndiv
        self.x = numpy.r_[0:self.image_width-1:1]
        self.dx1 = self.x[1]-self.x[0]
        self.symetry = symetry
        self.color_offset = color_offset

    def get_peaks_contour(self, x, peaks, spectral_centroid=None):
        self.contour[x] = numpy.max(peaks)
        self.centroids[x] = spectral_centroid

    def mean(self, samples):
        return numpy.mean(samples)

    def normalize(self, contour):
        contour = contour-min(contour)
        return contour/max(contour)

    def draw_peaks_contour(self):
        contour = self.contour.copy()

        # Smoothing
        contour = smooth(contour, window_len=16)

        # Normalize
        contour = self.normalize(contour)

        # Scaling
        #ratio = numpy.mean(contour)/numpy.sqrt(2)
        ratio = 1
        contour = self.normalize(numpy.expm1(contour/ratio))*(1-10**-6)

        # Spline
        #contour = cspline1d(contour)
        #contour = cspline1d_eval(contour, self.x, dx=self.dx1, x0=self.x[0])

        if self.symetry:
            height = int(self.image_height/2)
        else:
            height = self.image_height

        # Multicurve rotating
        for i in range(0,self.ndiv):
            self.previous_x, self.previous_y = None, None

            bright_color = int(255*(1-float(i)/(self.ndiv*2)))
            bright_color = 255-bright_color+self.color_offset
            #line_color = self.color_lookup[int(self.centroids[j]*255.0)]
            line_color = (bright_color,bright_color,bright_color)

            # Linear
            #contour = contour*(1.0-float(i)/self.ndiv)
            #contour = contour*(1-float(i)/self.ndiv)

            # Scaled
            contour = contour*numpy.arccos(float(i)/self.ndiv)*2/numpy.pi
            #contour = self.contour*(1-float(i)*numpy.arccos(float(i)/self.ndiv)*2/numpy.pi/self.ndiv)
            #contour = contour + ((1-contour)*2/numpy.pi*numpy.arcsin(float(i)/self.ndiv))

            curve = (height-1)*contour
            #curve = contour*(height-2)/2+height/2

            for x in self.x:
                x = int(x)
                y = curve[x]
                if not x == 0:
                    if not self.symetry:
                        self.draw.line([self.previous_x, self.previous_y, x, y], line_color)
                        self.draw_anti_aliased_pixels(x, y, y, line_color)
                    else:
                        self.draw.line([self.previous_x, self.previous_y+height, x, y+height], line_color)
                        self.draw_anti_aliased_pixels(x, y+height, y+height, line_color)
                        self.draw.line([self.previous_x, -self.previous_y+height, x, -y+height], line_color)
                        self.draw_anti_aliased_pixels(x, -y+height, -y+height, line_color)
                else:
                    if not self.symetry:
                        self.draw.point((x, y), line_color)
                    else:
                        self.draw.point((x, y+height), line_color)
                self.previous_x, self.previous_y = x, y

    def process(self, frames, eod):
        if len(frames) != 1:
            buffer = frames[:,0].copy()
            buffer.shape = (len(buffer),1)
            for samples, end in self.pixels_adapter.process(buffer, eod):
                if self.pixel_cursor < self.image_width:
                    peaks = self.peaks(samples)
                    self.get_peaks_contour(self.pixel_cursor, peaks)
                    self.pixel_cursor += 1
        if eod:
            self.draw_peaks_contour()

    def watermark(self, text, color=None, opacity=.6, margin=(10,10)):
        self.image = im_watermark(self.image, text, color=color, opacity=opacity, margin=margin)

    def save(self, filename):
        """ Apply last 2D transforms and write all pixels to the file. """
        # middle line (0 for none)
        a = 1
        for x in range(self.image_width):
            self.pixel[x, self.image_height/2] = tuple(map(lambda p: p+a, self.pixel[x, self.image_height/2]))
        #self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        self.image.save(filename)

    def release(self):
        pass


class WaveformImageSimple(object):
    """ Builds a PIL image representing a waveform of the audio stream.
    Adds pixels iteratively thanks to the adapter providing fixed size frame buffers.
    """

    def __init__(self, image_width, image_height, nframes, samplerate, fft_size, bg_color, color_scheme):
        self.image_width = image_width
        self.image_height = image_height
        self.nframes = nframes
        self.samplerate = samplerate
        self.fft_size = fft_size
        self.bg_color = bg_color
        self.color_scheme = color_scheme

        if isinstance(color_scheme, dict):
            colors = color_scheme['waveform']
        else:
            colors = default_color_schemes[color_scheme]['waveform']
        self.line_color = colors[0]

        self.samples_per_pixel = self.nframes / float(self.image_width)
        self.buffer_size = int(round(self.samples_per_pixel, 0))
        self.pixels_adapter = FixedSizeInputAdapter(self.buffer_size, 1, pad=False)
        self.pixels_adapter_nframes = self.pixels_adapter.blocksize(self.nframes)

        self.image = Image.new("RGBA", (self.image_width, self.image_height))
        self.pixel = self.image.load()
        self.draw = ImageDraw.Draw(self.image)
        self.previous_x, self.previous_y = None, None
        self.frame_cursor = 0
        self.pixel_cursor = 0

    def normalize(self, contour):
        contour = contour-min(contour)
        return contour/max(contour)

    def peaks(self, samples):
        """ Find the minimum and maximum peak of the samples.
        Returns that pair in the order they were found.
        So if min was found first, it returns (min, max) else the other way around. """

        max_index = numpy.argmax(samples)
        max_value = samples[max_index]

        min_index = numpy.argmin(samples)
        min_value = samples[min_index]

        if min_index < max_index:
            return (min_value, max_value)
        else:
            return (max_value, min_value)

    def draw_peaks(self, x, peaks):
        """ draw 2 peaks at x using the spectral_centroid for color """

        y1 = self.image_height * 0.5 - peaks[0] * (self.image_height - 4) * 0.5
        y2 = self.image_height * 0.5 - peaks[1] * (self.image_height - 4) * 0.5

        if self.previous_y and x < self.image_width-1:
            if y1 < y2:
                self.draw.line((x, 0, x, y1), self.line_color)
                self.draw.line((x, self.image_height , x, y2), self.line_color)
            else:
                self.draw.line((x, 0, x, y2), self.line_color)
                self.draw.line((x, self.image_height , x, y1), self.line_color)
        else:
            self.draw.line((x, 0, x, self.image_height), self.line_color)

        self.previous_x, self.previous_y = x, y1

    def process(self, frames, eod):
        if len(frames) != 1:
            buffer = frames[:,0]
            buffer.shape = (len(buffer),1)
            for samples, end in self.pixels_adapter.process(buffer, eod):
                if self.pixel_cursor < self.image_width-1:
                    self.draw_peaks(self.pixel_cursor, self.peaks(samples))
                    self.pixel_cursor += 1
            if self.pixel_cursor == self.image_width-1:
                self.draw_peaks(self.pixel_cursor, (0, 0))
                self.pixel_cursor += 1

    def watermark(self, text, color=None, opacity=.6, margin=(10,10)):
        self.image = im_watermark(self.image, text, color=color, opacity=opacity, margin=margin)

    def save(self, filename):
        """ Apply last 2D transforms and write all pixels to the file. """

        # middle line (0 for none)
        a = 1
        for x in range(self.image_width):
            self.pixel[x, self.image_height/2] = tuple(map(lambda p: p+a, self.pixel[x, self.image_height/2]))
        self.image.save(filename)

    def release(self):
        pass


class SpectrogramImage(object):
    """ Builds a PIL image representing a spectrogram of the audio stream (level vs. frequency vs. time).
    Adds pixels iteratively thanks to the adapter providing fixed size frame buffers."""

    def __init__(self, image_width, image_height, nframes, samplerate, fft_size, bg_color=None, color_scheme='default'):
        self.image_width = image_width
        self.image_height = image_height
        self.nframes = nframes
        self.samplerate = samplerate
        self.fft_size = fft_size
        self.color_scheme = color_scheme

        if isinstance(color_scheme, dict):
            colors = color_scheme['spectrogram']
        else:
            colors = default_color_schemes[color_scheme]['spectrogram']

        self.image = Image.new("P", (self.image_height, self.image_width))
        self.image.putpalette(interpolate_colors(colors, True))

        self.samples_per_pixel = self.nframes / float(self.image_width)
        self.buffer_size = int(round(self.samples_per_pixel, 0))
        self.pixels_adapter = FixedSizeInputAdapter(self.buffer_size, 1, pad=False)
        self.pixels_adapter_nframes = self.pixels_adapter.blocksize(self.nframes)

        self.lower = 100
        self.higher = 22050
        self.spectrum = Spectrum(self.fft_size, self.nframes, self.samplerate, self.lower, self.higher, numpy.hanning)

        # generate the lookup which translates y-coordinate to fft-bin
        self.y_to_bin = []
        f_min = float(self.lower)
        f_max = float(self.higher)
        y_min = math.log10(f_min)
        y_max = math.log10(f_max)
        for y in range(self.image_height):
            freq = math.pow(10.0, y_min + y / (image_height - 1.0) *(y_max - y_min))
            bin = freq / 22050.0 * (self.fft_size/2 + 1)

            if bin < self.fft_size/2:
                alpha = bin - int(bin)

                self.y_to_bin.append((int(bin), alpha * 255))

        # this is a bit strange, but using image.load()[x,y] = ... is
        # a lot slower than using image.putadata and then rotating the image
        # so we store all the pixels in an array and then create the image when saving
        self.pixels = []
        self.pixel_cursor = 0

    def draw_spectrum(self, x, spectrum):
        for (index, alpha) in self.y_to_bin:
            self.pixels.append( int( ((255.0-alpha) * spectrum[index] + alpha * spectrum[index + 1] )) )

        for y in range(len(self.y_to_bin), self.image_height):
            self.pixels.append(0)

    def process(self, frames, eod):
        if len(frames) != 1:
            buffer = frames[:,0].copy()
            buffer.shape = (len(buffer),1)

            # FIXME : breaks spectrum linearity
            for samples, end in self.pixels_adapter.process(buffer, eod):
                if self.pixel_cursor < self.image_width:
                    (spectral_centroid, db_spectrum) = self.spectrum.process(samples, True)
                    self.draw_spectrum(self.pixel_cursor, db_spectrum)
                    self.pixel_cursor += 1

    def watermark(self, text, color=None, opacity=.6, margin=(10,10)):
        #self.image = im_watermark(self.image, text, color=color, opacity=opacity, margin=margin)
        pass

    def save(self, filename):
        """ Apply last 2D transforms and write all pixels to the file. """
        self.image.putdata(self.pixels)
        self.image.transpose(Image.ROTATE_90).save(filename)

    def release(self):
        pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()