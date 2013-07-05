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
from aubio import filterbank, pvoc

class AubioMelEnergy(Processor):
    implements(IValueAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(AubioMelEnergy, self).setup(channels, samplerate, blocksize, totalframes)
        self.win_s = 1024
        self.hop_s = self.win_s / 4
        self.n_filters = 40
        self.n_coeffs = 13
        self.pvoc = pvoc(self.win_s, self.hop_s)
        self.melenergy = filterbank(self.n_filters, self.win_s)
        self.melenergy.set_mel_coeffs_slaney(samplerate)
        self.block_read = 0
        self.melenergy_results = numpy.zeros([self.n_filters, ])

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_mel_analyzer"

    @staticmethod
    @interfacedoc
    def name():
        return "Mel Energy analysis (aubio)"

    def process(self, frames, eod=False):
        for samples in downsample_blocking(frames, self.hop_s):
            fftgrain = self.pvoc(samples)
            self.melenergy_results = numpy.vstack( [ self.melenergy_results, self.melenergy(fftgrain) ])
            self.block_read += 1
        return frames, eod

    def results(self):

        container = AnalyzerResultContainer()
        melenergy = AnalyzerResult()
              
        # Get attributes
        sampleRate = self.samplerate()
        blockSize = self.win_s
        stepSize = self.hop_s
        parameters = dict(n_filters= self.n_filters,
                          n_coeffs=  self.n_coeffs)
        # Set attributes
        melenergy.attributes = AnalyzerAttributes(id="aubio_melenergy",
                                                  name="melenergy (aubio)",
                                                  unit='',
                                                  sampleRate = sampleRate,
                                                  blockSize = blockSize,
                                                  stepSize = stepSize,
                                                  parameters = parameters)                         
        # Set Data
        melenergy.data = self.melenergy_results
        container.add_result(melenergy)
        return container

