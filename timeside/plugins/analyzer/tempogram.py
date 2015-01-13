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

# Author: Thomas Fillon <thomas.fillon@parisson.com>

from __future__ import division

from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from timeside.analyzer.odf import OnsetDetectionFunction
from timeside.api import IAnalyzer
#from scipy import signal
from matplotlib.mlab import specgram, detrend_mean

import numpy as np


class Tempogram(Analyzer):
    """ Tempogram Analyzer

    Examples
    --------
    >>> import timeside
    >>> from timeside.core import get_processor
    >>> from timeside.tools.test_samples import samples
    >>> audio_source = samples['C4_scale.wav']
    >>> decoder = get_processor('file_decoder')(uri=audio_source)
    >>> tempogram = get_processor('tempogram')(input_blocksize=2048, input_stepsize=1024)
    >>> pipe = (decoder | tempogram)
    >>> pipe.run()
    >>> tempogram.results.keys()
    ['tempogram']
    >>> result = tempogram.results['tempogram']
    >>> result.data.shape
    (344, 1025)

     .. plot::

      import timeside
      from timeside.core import get_processor
      from timeside.tools.test_samples import samples
      audio_source = samples['sweep.wav']
      decoder = get_processor('file_decoder')(uri=audio_source)
      spectrogram = get_processor('spectrogram_analyzer')(input_blocksize=2048,
                                                          input_stepsize=1024)
      pipe = (decoder | spectrogram)
      pipe.run()
      res = spectrogram.results['spectrogram_analyzer']
      res.render()


    """
    implements(IAnalyzer)  # TODO check if needed with inheritance

    def __init__(self, input_blocksize=1024, input_stepsize=None):
        super(Tempogram, self).__init__()

        self.input_blocksize = input_blocksize
        if input_stepsize:
            self.input_stepsize = input_stepsize
        else:
            self.input_stepsize = input_blocksize / 2

        self.parents['odf'] = OnsetDetectionFunction(
            input_blocksize=self.input_blocksize,
            input_stepsize=self.input_stepsize)

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(Tempogram, self).setup(channels, samplerate,
                                     blocksize, totalframes)

    @staticmethod
    @interfacedoc
    def id():
        return "tempogram"

    @staticmethod
    @interfacedoc
    def name():
        return "Tempogram"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def process(self, frames, eod=False):
        return frames, eod

#    def generalized_autocorrelation_function(alpha=2):
#
#        NFFT = 2^(nextpow2(win_length)+1);
#        gac_func = zeros(NFFT,1);
#        for k=1:nb_bands,
#            %S = fft(xsband(k,:)-mean(xsband(k,:)),NFFT); TODO ou pas
#            S = fft(xsband(k,:),NFFT);
#            S = abs(S).^alpha;
#            S = real(ifft(S))';
#            gac_func = gac_func + S;
#

    def post_process(self):

        odf = self.parents['odf'].results['onset_detection_function'].data
        print odf.shape

        NFFT = np.round(20 * self.input_samplerate // self.input_stepsize)
        tempogram, freqs, t = specgram(odf.T,
                                       Fs=self.input_samplerate /
                                       self.input_stepsize,
                                       NFFT=NFFT, pad_to=4 * NFFT,
                                       noverlap=NFFT - 32,
                                       detrend=detrend_mean)

        result = self.new_result(data_mode='value', time_mode='framewise')
        #odf.parameters = {'FFT_SIZE': self.FFT_SIZE}
        result.data_object.value = tempogram
        self.add_result(result)


if __name__ == "__main__":
    import doctest
    import timeside
    doctest.testmod(timeside.analyzer.tempogram)
