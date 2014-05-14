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
from timeside.analyzer.preprocessors import downmix_to_mono, frames_adapter
import numpy as np


class Spectrogram(Analyzer):

    """Spectrogram analyzer"""
    implements(IAnalyzer)

    def __init__(self, blocksize=2048, stepsize=None, fft_size=None):
        super(Spectrogram, self).__init__()

        self.input_blocksize = blocksize
        if stepsize:
            self.input_stepsize = stepsize
        else:
            self.input_stepsize = blocksize / 2

        if not fft_size:
            self.FFT_SIZE = blocksize
        else:
            self.FFT_SIZE = fft_size

        self.values = []

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(Spectrogram, self).setup(channels, samplerate,
                                       blocksize, totalframes)

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

    @downmix_to_mono
    @frames_adapter
    def process(self, frames, eod=False):
            self.values.append(np.abs(np.fft.rfft(frames, self.FFT_SIZE)))
            return frames, eod

    def post_process(self):
        spectrogram = self.new_result(data_mode='value', time_mode='framewise')
        spectrogram.parameters = {'FFT_SIZE': self.FFT_SIZE}
        spectrogram.data_object.value = self.values
        self.process_pipe.results.add(spectrogram)
