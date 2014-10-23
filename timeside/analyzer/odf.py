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

# Author: Thomas Fillon <thomas@parisson.com>

from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from .spectrogram import Spectrogram
from timeside.api import IAnalyzer
import numpy as np
from numpy import pi as Pi
from scipy import signal
from ..tools.parameters import Int, HasTraits


class OnsetDetectionFunction(Analyzer):

    """Onset Detection Function analyzer"""
    implements(IAnalyzer)

    # Define Parameters
    class _Param(HasTraits):
        input_blocksize = Int()
        input_stepsize = Int()

    def __init__(self, input_blocksize=1024, input_stepsize=None):
        super(OnsetDetectionFunction, self).__init__()

        self.input_blocksize = input_blocksize
        if input_stepsize:
            self.input_stepsize = input_stepsize
        else:
            self.input_stepsize = input_blocksize / 2

        self.parents['spectrogram'] = Spectrogram(
            input_blocksize=self.input_blocksize,
            input_stepsize=self.input_stepsize)

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(OnsetDetectionFunction, self).setup(channels, samplerate,
                                                  blocksize, totalframes)

    @staticmethod
    @interfacedoc
    def id():
        return "onset_detection_function"

    @staticmethod
    @interfacedoc
    def name():
        return "Onset Detection Function"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def process(self, frames, eod=False):
        return frames, eod

    def post_process(self):

        #spectrogram = self.parents()[0]['spectrogram_analyzer'].data
        results = self.process_pipe.results
        parent_uuid = self.parents['spectrogram'].uuid()
        spectrogram = results[parent_uuid]['spectrogram_analyzer'].data
        #spectrogram = self.pipe._results[self.parents()[0].id]

        # Low-pass filtering of the spectrogram amplitude along the time axis
        S = signal.lfilter(signal.hann(15)[8:], 1, abs(spectrogram), axis=0)

        # Clip small value to a minimal threshold
        np.maximum(S, 1e-9, out=S)

        S = np.log10(S)

#        plt.figure()
#        plt.imshow(S,origin='lower', aspect='auto', interpolation='nearest')
#        plt.show()

        # S[S<1e-3]=0
        np.maximum(S, 1e-3, out=S)

        # Differentiator filter
        df_filter = signal.fir_filter_design.remez(31, [0, 0.5], [Pi],
                                                   type='differentiator')

        S_diff = signal.lfilter(df_filter, 1, S, axis=0)
        S_diff[S_diff < 1e-10] = 0

        # Summation along the frequency axis
        odf_diff = S_diff.sum(axis=1)
        odf_median = np.median(odf_diff)
        if odf_median:
            odf_diff = odf_diff / odf_median  # Normalize

        odf = self.new_result(data_mode='value', time_mode='framewise')
        #odf.parameters = {'FFT_SIZE': self.FFT_SIZE}
        odf.data_object.value = odf_diff
        self.add_result(odf)
