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
import numpy as np


class Spectrogram(Analyzer):
    implements(IAnalyzer)

    def __init__(self, blocksize=2048, stepsize=None):
        super(Spectrogram, self).__init__()

        self.input_blocksize = blocksize
        if stepsize:
            self.input_stepsize = stepsize
        else:
            self.input_stepsize = blocksize / 2

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(Spectrogram, self).setup(channels, samplerate,
              blocksize, totalframes)

        self.values = []
        self.FFT_SIZE = 2048

    @staticmethod
    @interfacedoc
    def id():
        return "spectrogram_analyzer"

    @staticmethod
    @interfacedoc
    def name():
        return "Spectrogram Analyzer"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def process(self, frames, eod=False):
        for samples in downsample_blocking(frames, self.input_stepsize):
            #time = self.block_read * self.input_stepsize * 1. / self.samplerate()
            self.values.append(np.abs(np.fft.rfft(samples, self.FFT_SIZE)))
        return frames, eod

    def post_process(self):
        spectrogram = self.new_result(data_mode='value', time_mode='framewise')
        spectrogram.parameters = {'FFT_SIZE': self.FFT_SIZE}
        spectrogram.data_object.value = self.values
        self.pipe.results.add(spectrogram)
