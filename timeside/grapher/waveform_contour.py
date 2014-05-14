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
from . waveform_simple import Waveform
from . utils import peaks

import numpy


class WaveformContourBlack(Waveform):

    """ Builds a PIL image representing an amplitude coutour (envelop) of the audio stream.
    """

    implements(IGrapher)

    @interfacedoc
    def __init__(self, width=1024, height=256, bg_color=(0, 0, 0), color_scheme='default'):
        super(WaveformContourBlack, self).__init__(
            width, height, bg_color, color_scheme)
        self.contour = numpy.zeros(self.image_width)
        self.ndiv = 4
        self.x = numpy.r_[0:self.image_width - 1:1]
        self.symetry = True
        self.color_offset = 160

    @staticmethod
    @interfacedoc
    def id():
        return "waveform_contour_black"

    @staticmethod
    @interfacedoc
    def name():
        return "Contour black"

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(WaveformContourBlack, self).setup(
            channels, samplerate, blocksize, totalframes)

    @interfacedoc
    def process(self, frames, eod=False):
        if len(frames) != 1:
            buffer = frames[:, 0].copy()
            buffer.shape = (len(buffer), 1)
            for samples, end in self.pixels_adapter.process(buffer, eod):
                if self.pixel_cursor < self.image_width:
                    self.contour[self.pixel_cursor] = numpy.max(peaks(samples))
                    self.pixel_cursor += 1
        if eod:
            self.draw_peaks_contour()
        return frames, eod


class WaveformContourWhite(WaveformContourBlack):

    """ Builds a PIL image representing an amplitude coutour (envelop) of the audio stream.
    """

    implements(IGrapher)

    @interfacedoc
    def __init__(self, width=1024, height=256, bg_color=(255, 255, 255), color_scheme='default'):
        super(WaveformContourWhite, self).__init__(
            width, height, bg_color, color_scheme)
        self.color_offset = 60

    @staticmethod
    @interfacedoc
    def id():
        return "waveform_contour_white"

    @staticmethod
    @interfacedoc
    def name():
        return "Contour white"
