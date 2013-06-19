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
from aubio import specdesc, pvoc

class AubioSpecdesc(Processor):
    implements(IValueAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(AubioSpecdesc, self).setup(channels, samplerate, blocksize, totalframes)
        self.block_read = 0
        self.win_s = 1024
        self.hop_s = self.win_s / 4
        self.pvoc = pvoc(self.win_s, self.hop_s)
        self.methods = ['default', 'energy', 'hfc', 'complex', 'phase', 'specdiff', 'kl',
                'mkl', 'specflux', 'centroid', 'slope', 'rolloff', 'spread', 'skewness',
                'kurtosis', 'decrease']
        self.specdesc = {}
        self.specdesc_results = {}
        for method in self.methods:
            self.specdesc[method] = specdesc(method, self.win_s)
            self.specdesc_results[method] = []

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_specdesc_analyzer"

    @staticmethod
    @interfacedoc
    def name():
        return "Mel Energy analysis (aubio)"

    def process(self, frames, eod=False):
        for samples in downsample_blocking(frames, self.hop_s):
            fftgrain = self.pvoc(samples)
            for method in self.methods:
                self.specdesc_results[method] += [self.specdesc[method](fftgrain)[0]]
        return frames, eod

    def results(self):

        container = AnalyzerResultContainer()

        for method in self.methods:
            id = '_'.join(["aubio_specdesc", method])
            name = ' '.join(["spectral descriptor", method, "(aubio)"])
            unit = ""

            values = numpy.array(self.specdesc_results[method])

            specdesc = AnalyzerResult(id = id, name = name, unit = unit)
            specdesc.value = values

            mean_id = '_'.join([id, 'mean'])
            mean_name = ' '.join(["spectral descriptor", method, "mean", "(aubio)"])
            specdesc_mean = AnalyzerResult(id = mean_id, name = mean_name, unit = "")
            specdesc_mean.value = numpy.mean(values,axis=0)

            median_id = '_'.join([id, 'median'])
            median_name = ' '.join(["spectral descriptor", method, "median", "(aubio)"])
            specdesc_median = AnalyzerResult(id = median_id , name = median_name , unit = "")
            specdesc_median.value = numpy.median(values,axis=0)

            container.add_result([specdesc, specdesc_mean, specdesc_median])

        return container
