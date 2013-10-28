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
from timeside.grapher.waveform_contour_black import WaveformContourBlack


class WaveformContourWhite(WaveformContourBlack):

    implements(IGrapher)

    @interfacedoc
    def __init__(self, width=1024, height=256, bg_color=(255,255,255), color_scheme='default'):
        super(WaveformContourWhite, self).__init__(width, height, bg_color, color_scheme)
        self.color_offset = 60

    @staticmethod
    @interfacedoc
    def id():
        return "waveform_contour_white"

    @staticmethod
    @interfacedoc
    def name():
        return "Contour white"

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(WaveformContourWhite, self).setup(channels, samplerate, blocksize, totalframes)
