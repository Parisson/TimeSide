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

from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from timeside.api import IAnalyzer
from utils import downsample_blocking

import numpy
from aubio import filterbank, pvoc


class AubioMelEnergy(Analyzer):
    implements(IAnalyzer)

    def __init__(self):
        super(AubioMelEnergy, self).__init__()
        self.input_blocksize = 1024
        self.input_stepsize = self.input_blocksize / 4

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(AubioMelEnergy, self).setup(
            channels, samplerate, blocksize, totalframes)
        self.n_filters = 40
        self.n_coeffs = 13
        self.pvoc = pvoc(self.input_blocksize, self.input_stepsize)
        self.melenergy = filterbank(self.n_filters, self.input_blocksize)
        self.melenergy.set_mel_coeffs_slaney(samplerate)
        self.block_read = 0
        self.melenergy_results = numpy.zeros([self.n_filters, ])

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_melenergy"

    @staticmethod
    @interfacedoc
    def name():
        return "Mel Energy (aubio)"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def process(self, frames, eod=False):
        for samples in downsample_blocking(frames, self.input_stepsize):
            # TODO : check pourquoi on utilise pas le blocksize ?
            fftgrain = self.pvoc(samples)
            self.melenergy_results = numpy.vstack(
                [self.melenergy_results, self.melenergy(fftgrain)])
            self.block_read += 1
        return frames, eod

    def post_process(self):
        melenergy = self.new_result(data_mode='value', time_mode='framewise')
        melenergy.parameters = dict(n_filters=self.n_filters,
                                    n_coeffs=self.n_coeffs)
        melenergy.data_object.value = self.melenergy_results
        self.pipe.results.add(melenergy)
