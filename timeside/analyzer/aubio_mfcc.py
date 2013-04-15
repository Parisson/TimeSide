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

import numpy
from aubio import mfcc, pvoc

from math import isnan

class AubioMfcc(Processor):
    implements(IValueAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(AubioMfcc, self).setup(channels, samplerate, blocksize, totalframes)
        self.win_s = 1024
        self.hop_s = self.win_s / 4
        self.n_filters = 40
        self.n_coeffs = 13
        self.pvoc = pvoc(self.win_s, self.hop_s)
        self.mfcc = mfcc(self.win_s, self.n_filters, self.n_coeffs, samplerate)
        self.block_read = 0
        self.mfcc_results = numpy.zeros([self.n_coeffs, ])

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_mfcc_analyzer"

    @staticmethod
    @interfacedoc
    def name():
        return "MFCC analysis (aubio)"

    def process(self, frames, eod=False):
        i = 0
        while i < frames.shape[0]:
            downmixed_samples = frames[i:i+self.hop_s, :].sum(axis = -1)
            time = self.block_read * self.hop_s * 1. / self.samplerate()
            fftgrain = self.pvoc(downmixed_samples)
            coeffs = self.mfcc(fftgrain)
            self.mfcc_results = numpy.vstack((self.mfcc_results, coeffs))
            i += self.hop_s
            self.block_read += 1
        return frames, eod

    def results(self):

        mfcc = AnalyzerResult(id = "aubio_mfcc", name = "mfcc (aubio)", unit = "")
        mfcc.value = [list(line) for line in self.mfcc_results]

        mfcc_mean = AnalyzerResult(id = "aubio_mfcc_mean", name = "mfcc mean (aubio)", unit = "")
        mfcc_mean.value = list(self.mfcc_results.mean(axis=0))

        mfcc_median = AnalyzerResult(id = "aubio_mfcc_median", name = "mfcc median (aubio)", unit = "")
        mfcc_median.value = list(numpy.median(self.mfcc_results,axis=0))

        return AnalyzerResultContainer([mfcc, mfcc_median, mfcc_mean])
