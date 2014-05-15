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
from __future__ import absolute_import

from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from timeside.api import IAnalyzer
from timeside.analyzer.preprocessors import downmix_to_mono, frames_adapter

import numpy
from aubio import mfcc, pvoc


class AubioMfcc(Analyzer):

    """Aubio MFCC analyzer"""
    implements(IAnalyzer)

    def __init__(self):
        super(AubioMfcc, self).__init__()
        self.input_blocksize = 1024
        self.input_stepsize = self.input_blocksize / 4

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(AubioMfcc, self).setup(
            channels, samplerate, blocksize, totalframes)
        self.n_filters = 40
        self.n_coeffs = 13
        self.pvoc = pvoc(self.input_blocksize, self.input_stepsize)
        self.mfcc = mfcc(self.input_blocksize,
                         self.n_filters,
                         self.n_coeffs,
                         samplerate)
        self.block_read = 0
        self.mfcc_results = numpy.zeros([self.n_coeffs, ])

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_mfcc"

    @staticmethod
    @interfacedoc
    def name():
        return "MFCC (aubio)"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    @downmix_to_mono
    @frames_adapter
    def process(self, frames, eod=False):
        fftgrain = self.pvoc(frames)
        coeffs = self.mfcc(fftgrain)
        self.mfcc_results = numpy.vstack((self.mfcc_results, coeffs))
        self.block_read += 1
        return frames, eod

    def post_process(self):
        mfcc = self.new_result(data_mode='value', time_mode='framewise')
        mfcc.parameters = dict(n_filters=self.n_filters,
                               n_coeffs=self.n_coeffs)
        mfcc.data_object.value = self.mfcc_results
        self.process_pipe.results.add(mfcc)
