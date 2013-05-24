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
from timeside.api import IValueAnalyzer
from aubio import pitch

class AubioPitch(Processor):
    implements(IValueAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(AubioPitch, self).setup(channels, samplerate, blocksize, totalframes)
        self.win_s = 2048
        self.hop_s = self.win_s / 2
        self.p = pitch("default", self.win_s, self.hop_s, samplerate)
        self.p.set_unit("freq")
        self.block_read = 0
        self.pitches = []

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_pitch_analyzer"

    @staticmethod
    @interfacedoc
    def name():
        return "f0 (aubio)"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def __str__(self):
        return "pitch values"

    def process(self, frames, eod=False):
        for samples in downsample_blocking(frames, self.hop_s):
            #time = self.block_read * self.hop_s * 1. / self.samplerate()
            self.pitches += [self.p(samples)[0]]
            self.block_read += 1
        return frames, eod

    def results(self):

        #container = AnalyzerResultContainer()

        self.pitches = numpy.array(self.pitches)

        pitch = AnalyzerResult(id = "aubio_pitch", name = "f0 (aubio)", unit = "Hz")
        pitch.value = self.pitches
        #container.add_result(pitch)

        pitch_mean = AnalyzerResult(id = "aubio_pitch_mean", name = "f0 mean (aubio)", unit = "Hz")
        pitch_mean.value = numpy.mean(self.pitches)
        #container.add_result(pitch_mean)

        pitch_median = AnalyzerResult(id = "aubio_pitch_median", name = "f0 median (aubio)", unit = "Hz")
        pitch_median.value = numpy.median(self.pitches)
        #container.add_result(pitch_median)

        #return container
        return AnalyzerResultContainer([pitch, pitch_mean, pitch_median])
