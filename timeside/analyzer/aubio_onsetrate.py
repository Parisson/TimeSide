# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Paul Brossier <piem@piem.org>

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

# Author: Paul Brossier <piem@piem.org>

from timeside.core import Processor, implements, interfacedoc, FixedSizeInputAdapter
from timeside.analyzer.core import *
from timeside.api import IValueAnalyzer
from aubio import onset

class AubioOnsetRate(Processor):
    implements(IValueAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(AubioOnsetRate, self).setup(channels, samplerate,  blocksize, totalframes)
        self.win_s = 512
        self.hop_s = self.win_s / 2
        self.t = onset("default", self.win_s, self.hop_s, 1)
        self.block_read = 0
        self.onsets = []

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_onsetrate"

    @staticmethod
    @interfacedoc
    def name():
        return "aubio onset rate"

    @staticmethod
    @interfacedoc
    def unit():
        return "bpm"

    def __str__(self):
        return "%s %s" % (str(self.value), unit())

    def process(self, frames, eod=False):
        i = 0
        while not eod and i < frames.shape[0]:
          isonset = self.t(frames[0,i:i+self.hop_s])
          if isonset: self.onsets += [(isonset[0] + self.block_read * self.hop_s ) / 44100. ]
          i += self.hop_s
          self.block_read += 1
        return frames, eod

    def result(self):
        periods = [60./(b - a) for a,b in zip(self.onsets[:-1],self.onsets[1:])]
        from numpy import mean
        return mean(periods)
