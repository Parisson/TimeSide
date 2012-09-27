#!/usr/bin/env python
# -*- coding: utf-8 -*-

# wav2png.py -- converts wave files to wave file and spectrogram images
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


import optparse, math, sys
import ImageFilter, ImageChops, Image, ImageDraw, ImageColor, ImageEnhance
import numpy
from timeside.core import FixedSizeInputAdapter

default_color_schemes = {
    'default': {
        'waveform': [(50,0,200), (0,220,80), (255,224,0), (255,0,0)],
        'spectrogram': [(0, 0, 0), (58/4,68/4,65/4), (80/2,100/2,153/2), (90,180,100),
                      (224,224,44), (255,60,30), (255,255,255)]
    },
    'iso': {
        'waveform': [(0,0,255), (0,255,255), (255,255,0), (255,0,0)],
        'spectrogram': [(0, 0, 0), (58/4,68/4,65/4), (80/2,100/2,153/2), (90,180,100),
                      (224,224,44), (255,60,30), (255,255,255)]
    },
    'purple': {
        'waveform': [(173,173,173), (147,149,196), (77,80,138), (108,66,0)],
        'spectrogram': [(0, 0, 0), (58/4,68/4,65/4), (80/2,100/2,153/2), (90,180,100),
                      (224,224,44), (255,60,30), (255,255,255)]
    },
    'awdio': {
        'waveform': [(255,255,255), (255,255,255), (255,255,255), (255,255,255)],
        'spectrogram': [(0, 0, 0), (58/4,68/4,65/4), (80/2,100/2,153/2), (90,180,100),
                      (224,224,44), (255,60,30), (255,255,255)]
    },
}


class Spectrum(object):
    """ FFT based frequency analysis of audio frames."""

    def __init__(self, fft_size, nframes, samplerate, lower, higher, window_function=numpy.ones):
        self.fft_size = fft_size
        self.window = window_function(self.fft_size)
        self.spectrum_range = None
        self.lower = lower
        self.higher = higher
        self.lower_log = math.log10(self.lower)
        self.higher_log = math.log10(self.higher)
        self.clip = lambda val, low, high: min(high, max(low, val))
        self.nframes = nframes
        self.samplerate = samplerate
        self.spectrum_adapter = FixedSizeInputAdapter(self.fft_size, 1, pad=True)

    def process(self, frames, eod, spec_range=120.0):
        """ Returns a tuple containing the spectral centroid and the spectrum (dB scales) of the input audio frames.
            An adapter is used to fix the buffer length and then provide fixed FFT window sizes."""

        for buffer, end in self.spectrum_adapter.process(frames, eod):
            samples = buffer[:,0].copy()
            if end:
                break

        #samples = numpy.concatenate((numpy.zeros(self.fft_size/2), samples), axis=1)
        samples *= self.window
        fft = numpy.fft.fft(samples)
        spectrum = numpy.abs(fft[:fft.shape[0] / 2 + 1]) / float(self.fft_size) # normalized abs(FFT) between 0 and 1
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


def interpolate_colors(colors, flat=False, num_colors=256):
    """ Given a list of colors, create a larger list of colors interpolating
    the first one. If flatten is True a list of numers will be returned. If
    False, a list of (r,g,b) tuples. num_colors is the number of colors wanted
    in the final list """

    palette = []

    for i in range(num_colors):
        index = (i * (len(colors) - 1))/(num_colors - 1.0)
        index_int = int(index)
        alpha = index - float(index_int)

        if alpha > 0:
            r = (1.0 - alpha) * colors[index_int][0] + alpha * colors[index_int + 1][0]
            g = (1.0 - alpha) * colors[index_int][1] + alpha * colors[index_int + 1][1]
            b = (1.0 - alpha) * colors[index_int][2] + alpha * colors[index_int + 1][2]
        else:
            r = (1.0 - alpha) * colors[index_int][0]
            g = (1.0 - alpha) * colors[index_int][1]
            b = (1.0 - alpha) * colors[index_int][2]

        if flat:
            palette.extend((int(r), int(g), int(b)))
        else:
            palette.append((int(r), int(g), int(b)))

    return palette


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
            (spectral_centroid, db_spectrum) = self.spectrum.process(buffer, True)
            for samples, end in self.pixels_adapter.process(buffer, eod):
                if self.pixel_cursor < self.image_width:
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

            #bright_color = 255
            bright_color = int(255*(1-float(i)/(self.ndiv*2)))
            bright_color = 255-bright_color+self.color_offset
            #line_color = self.color_lookup[int(self.centroids[j]*255.0)]
            line_color = (bright_color,bright_color,bright_color)

            # Linear
            #contour = contour*(1.0-float(i)/self.ndiv)
            #contour = contour*(1-float(i)/self.ndiv)

            # Cosine
            contour = contour*numpy.arccos(float(i)/self.ndiv)*2/numpy.pi
            #contour = self.contour*(1-float(i)*numpy.arccos(float(i)/self.ndiv)*2/numpy.pi/self.ndiv)

            # Negative Sine
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
                    #(spectral_centroid, db_spectrum) = self.spectrum.process(buffer, True)
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
                if end:
                    samples = 0
                    buffer = 0
                    break
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

class Noise(object):
    """A class that mimics audiolab.sndfile but generates noise instead of reading
    a wave file. Additionally it can be told to have a "broken" header and thus crashing
    in the middle of the file. Also useful for testing ultra-short files of 20 samples."""

    def __init__(self, num_frames, has_broken_header=False):
        self.seekpoint = 0
        self.num_frames = num_frames
        self.has_broken_header = has_broken_header

    def seek(self, seekpoint):
        self.seekpoint = seekpoint

    def get_nframes(self):
        return self.num_frames

    def get_samplerate(self):
        return 44100

    def get_channels(self):
        return 1

    def read_frames(self, frames_to_read):
        if self.has_broken_header and self.seekpoint + frames_to_read > self.num_frames / 2:
            raise IOError()

        num_frames_left = self.num_frames - self.seekpoint
        if num_frames_left < frames_to_read:
            will_read = num_frames_left
        else:
            will_read = frames_to_read
        self.seekpoint += will_read
        return numpy.random.random(will_read)*2 - 1


# TOOLS

def downsample(vector, factor):
    """
    downsample(vector, factor):
        Downsample (by averaging) a vector by an integer factor.
    """
    if (len(vector) % factor):
        print "Length of 'vector' is not divisible by 'factor'=%d!" % factor
        return 0
    vector.shape = (len(vector)/factor, factor)
    return numpy.mean(vector, axis=1)


def smooth(x, window_len=10, window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    import numpy as np
    t = numpy.linspace(-2,2,0.1)
    x = numpy.sin(t)+numpy.random.randn(len(t))*0.1
    y = smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s=numpy.r_[2*x[0]-x[window_len:1:-1], x, 2*x[-1]-x[-1:-window_len:-1]]

    if window == 'flat': #moving average
        w = numpy.ones(window_len,'d')
    else:
        w = getattr(numpy, window)(window_len)

    y = numpy.convolve(w/w.sum(), s, mode='same')
    return y[window_len-1:-window_len+1]

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def im_watermark(im, inputtext, font=None, color=None, opacity=.6, margin=(30,30)):
    """
    imprints a PIL image with the indicated text in lower-right corner
    """
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    textlayer = Image.new("RGBA", im.size, (0,0,0,0))
    textdraw = ImageDraw.Draw(textlayer)
    textsize = textdraw.textsize(inputtext, font=font)
    textpos = [im.size[i]-textsize[i]-margin[i] for i in [0,1]]
    textdraw.text(textpos, inputtext, font=font, fill=color)
    if opacity != 1:
        textlayer = reduce_opacity(textlayer,opacity)
    return Image.composite(textlayer, im, textlayer)
