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

class WaveformImageJoyContour(WaveformImage):

    def __init__(self, image_width, image_height, nframes, samplerate, fft_size, bg_color, color_scheme, ndiv=1, symetry=None):
        WaveformImage.__init__(self, image_width, image_height, nframes, samplerate, fft_size, bg_color, color_scheme)
        self.contour = numpy.zeros(self.image_width)
        self.centroids = numpy.zeros(self.image_width)
        self.ndiv = ndiv
        self.x = numpy.r_[0:self.image_width-1:1]
        self.dx1 = self.x[1]-self.x[0]
        self.symetry = symetry

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
            bright_color = 255-bright_color+160
#            line_color = self.color_lookup[int(self.centroids[j]*255.0)]
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
#            curve = contour*(height-2)/2+height/2
            
            for x in self.x:
                x = int(x)
                y = curve[x]
                if not x == 0:
                    if not self.symetry:
                        self.draw.line([self.previous_x, self.previous_y, x, y], line_color)
                        #self.draw_anti_aliased_pixels(x, y, y, line_color)
                    else:
                        self.draw.line([self.previous_x, self.previous_y+height, x, y+height], line_color)
                        #self.draw_anti_aliased_pixels(x, y+height, y+height, line_color)
                        self.draw.line([self.previous_x, -self.previous_y+height, x, -y+height], line_color)
                        #self.draw_anti_aliased_pixels(x, -y+height, -y+height, line_color)
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

    def save(self, filename):
        """ Apply last 2D transforms and write all pixels to the file. """
        # middle line (0 for none)
        a = 1
        for x in range(self.image_width):
            self.pixel[x, self.image_height/2] = tuple(map(lambda p: p+a, self.pixel[x, self.image_height/2]))
#        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        self.image.save(filename)


class WaveformJoyDiv(Processor):
    implements(IGrapher)

    FFT_SIZE = 0x400

    @interfacedoc
    def __init__(self, width=1024, height=256, bg_color=(136,136,136), color_scheme='default'):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.color_scheme = color_scheme
        self.graph = None
        self.ndiv = 4
        self.symetry = True

    @staticmethod
    @interfacedoc
    def id():
        return "waveform_joydiv"

    @staticmethod
    @interfacedoc
    def name():
        return "Waveform JoyDiv"

    @interfacedoc
    def set_colors(self, background, scheme):
        self.bg_color = background
        self.color_scheme = scheme

    @interfacedoc
    def setup(self, channels=None, samplerate=None, nframes=None):
        super(WaveformJoyDiv, self).setup(channels, samplerate, nframes)
        if self.graph:
            self.graph = None
        self.graph = WaveformImageJoyContour(self.width, self.height, self.nframes(), self.samplerate(), self.FFT_SIZE,
                                    bg_color=self.bg_color, color_scheme=self.color_scheme,  ndiv=self.ndiv, symetry=self.symetry)

    @interfacedoc
    def process(self, frames, eod=False):
        self.graph.process(frames, eod)
        return frames, eod

    @interfacedoc
    def render(self, output):
        if output:
            self.graph.save(output)
        return self.graph.image
