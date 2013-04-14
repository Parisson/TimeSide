# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Paul Brossier <piem@piem.org>

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
from timeside.api import IAnalyzer
from aubio import onset, tempo

class AubioTemporal(Processor):
    implements(IAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(AubioTemporal, self).setup(channels, samplerate, blocksize, totalframes)
        self.win_s = 1024
        self.hop_s = 256
        self.o = onset("default", self.win_s, self.hop_s, samplerate)
        self.t = tempo("default", self.win_s, self.hop_s, samplerate)
        self.block_read = 0
        self.onsets = []
        self.beats = []

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_temporal"

    @staticmethod
    @interfacedoc
    def name():
        return "onsets (aubio)"

    @staticmethod
    @interfacedoc
    def unit():
        return "seconds"

    def __str__(self):
        return "%s %s" % (str(self.value), unit())

    def process(self, frames, eod=False):
        i = 0
        while i < frames.shape[0]:
            downmixed = frames[i:i+self.hop_s, :].sum(axis = -1)
            if self.o(downmixed):
                self.onsets += [self.o.get_last_s()]
            if self.t(downmixed):
                self.beats += [self.t.get_last_s()]
            i += self.hop_s
            self.block_read += 1
        return frames, eod

    def results(self):
        from numpy import mean, median

        onsets = AnalyzerResult(id = "aubio_onset", name = "onsets (aubio)", unit = "s")
        onsets.value = self.onsets

        onsetrate_mean = AnalyzerResult(id = "aubio_onset_rate_mean", name = "onset rate (aubio)", unit = "bpm")
        onsetrate_median = AnalyzerResult(id = "aubio_onset_rate_median", name = "onset rate (median) (aubio)", unit = "bpm")
        if len(self.onsets) > 1:
            periods = [60./(b - a) for a,b in zip(self.onsets[:-1],self.onsets[1:])]
            onsetrate_mean.value = mean (periods)
            onsetrate_median.value = median (periods)
        else:
            onsetrate_mean.value = 0
            onsetrate_median.value = 0

        beats = AnalyzerResult(id = "aubio_beat", name = "beats (aubio)", unit = "s")
        beats.value = self.beats

        bpm = AnalyzerResult(id = "aubio_bpm", name = "bpm (aubio)", unit = "bpm")
        if len(self.beats) > 2:
            periods = [60./(b - a) for a,b in zip(self.beats[:-1],self.beats[1:])]
            bpm.value = median (periods)
        else:
            bpm.value = 0

        return AnalyzerResultContainer([onsets, onsetrate_mean, onsetrate_median, beats, bpm])
