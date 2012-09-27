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


class WaveformContourWhite(Processor):
    implements(IGrapher)

    FFT_SIZE = 0x400

    @interfacedoc
    def __init__(self, width=1024, height=256, bg_color=(255,255,255), color_scheme='default'):
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
        return "waveform_contour_wh"

    @staticmethod
    @interfacedoc
    def name():
        return "Contour white"

    @interfacedoc
    def set_colors(self, background, scheme):
        self.bg_color = background
        self.color_scheme = scheme

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(WaveformContourWhite, self).setup(channels, samplerate, blocksize, totalframes)
        self.graph = WaveformImageJoyContour(self.width, self.height, totalframes,
                                             self.samplerate(), self.FFT_SIZE,
                                            bg_color=self.bg_color,
                                            color_scheme=self.color_scheme,
                                            ndiv=self.ndiv, symetry=self.symetry,
                                            color_offset=60)

    @interfacedoc
    def process(self, frames, eod=False):
        self.graph.process(frames, eod)
        return frames, eod

    @interfacedoc
    def render(self, output):
        if output:
            self.graph.save(output)
        return self.graph.image

    def release(self):
        self.graph.release()

    def watermark(self, text, font=None, color=(0, 0, 0), opacity=.6, margin=(5,5)):
        self.graph.watermark(text, color=color, opacity=opacity, margin=margin)
