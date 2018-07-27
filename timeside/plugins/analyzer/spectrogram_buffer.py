# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2014 Parisson SARL
# Copyright (c) 2013-2014 Thomas Fillon

# This file is part of TimeSide.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author: Thomas Fillon <thomas@parisson.com>

from __future__ import division
from timeside.core import implements, interfacedoc
from timeside.core.analyzer import Analyzer
from timeside.core.api import IAnalyzer
from timeside.core.preprocessors import downmix_to_mono, frames_adapter
from timeside.core.tools.parameters import store_parameters, Int, HasTraits
from timeside.core.tools.buffering import BufferTable
from timeside.plugins.analyzer.spectrogram import Spectrogram

import numpy as np


class SpectrogramBuffer(Spectrogram):
    """
    Spectrogram image builder with an extensible buffer based on tables

    Parameters
    ----------
    input_blocksize : int, optional
        Blocksize of the input signal, default to 2048
    input_stepsize : str, optional
        The second parameter, default to half blocksize.
    fft_size : int, optional
        The size of the fft, default to blocksize.

    Examples
    --------
    >>> import timeside
    >>> from timeside.core import get_processor
    >>> from timeside.core.tools.test_samples import samples
    >>> audio_source = samples['sweep.wav']
    >>> decoder = get_processor('file_decoder')(uri=audio_source)
    >>> spectrogram = get_processor('spectrogram_analyzer_buffer')(input_blocksize=2048, input_stepsize=1024)
    >>> pipe = (decoder | spectrogram)
    >>> pipe.run()
    >>> spectrogram.results.keys()
    ['spectrogram_analyzer_buffer']
    >>> result = spectrogram.results['spectrogram_analyzer_buffer']
    >>> result.data.shape
    (345, 1025)

     .. plot::

      import timeside
      from timeside.core import get_processor
      from timeside.core.tools.test_samples import samples
      audio_source = samples['sweep.wav']
      decoder = get_processor('file_decoder')(uri=audio_source)
      spectrogram = get_processor('spectrogram_analyzer_buffer')(input_blocksize=2048,
                                                          input_stepsize=1024)
      pipe = (decoder | spectrogram)
      pipe.run()
      res = spectrogram.results['spectrogram_analyzer_buffer']
      res.render()
    """

    implements(IAnalyzer)

    @store_parameters
    def __init__(self, input_blocksize=2048, input_stepsize=None,
                 fft_size=None):
        super(SpectrogramBuffer, self).__init__()
        self.values = BufferTable()

    @staticmethod
    @interfacedoc
    def id():
        return "spectrogram_analyzer_buffer"

    @staticmethod
    @interfacedoc
    def name():
        return "Spectrogram Analyzer with extensible buffer"

    @downmix_to_mono
    @frames_adapter
    def process(self, frames, eod=False):
        stft = np.fft.rfft(frames, self.fft_size)
        self.values.append('stft', stft)
        return frames, eod

    def post_process(self):
        spectrogram = self.new_result(data_mode='value', time_mode='framewise')
        spectrogram.parameters = {'fft_size': self.fft_size}
        spectrogram.data_object.value = np.abs(self.values['stft'])
        nb_freq = spectrogram.data_object.value.shape[1]
        spectrogram.data_object.y_value = (np.arange(0, nb_freq) *
                                           self.samplerate() / self.fft_size)
        self.add_result(spectrogram)

    def release(self):
        self.values.close()


if __name__ == "__main__":
    import doctest
    import timeside
    doctest.testmod(timeside.plugins.analyzer.spectrogram_buffer, verbose=True)
