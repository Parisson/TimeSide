# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Paul Brossier <piem@piem.org>

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

# Author: Paul Brossier <piem@piem.org>
from __future__ import division
from timeside.core import implements, interfacedoc
from timeside.core.analyzer import Analyzer
from timeside.core.api import IAnalyzer
from timeside.core.preprocessors import downmix_to_mono, frames_adapter
from timeside.core.tools.buffering import BufferTable
from timeside.core.tools.parameters import store_parameters, Int, HasTraits

import numpy as np


class Spectrogram(Analyzer):

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
    >>> spectrogram = get_processor('spectrogram_analyzer')(input_blocksize=2048, input_stepsize=1024)
    >>> pipe = (decoder | spectrogram)
    >>> pipe.run()
    >>> spectrogram.results.keys()
    ['spectrogram_analyzer']
    >>> result = spectrogram.results['spectrogram_analyzer']
    >>> result.data.shape
    (344, 1025)

     .. plot::

      import timeside
      from timeside.core import get_processor
      from timeside.core.tools.test_samples import samples
      audio_source = samples['sweep.wav']
      decoder = get_processor('file_decoder')(uri=audio_source)
      spectrogram = get_processor('spectrogram_analyzer')(input_blocksize=2048,
                                                          input_stepsize=1024)
      pipe = (decoder | spectrogram)
      pipe.run()
      res = spectrogram.results['spectrogram_analyzer']
      res.render()
    """

    implements(IAnalyzer)

    _schema = {"type": "object",
               "properties": {
                   "fft_size": {"type": "integer"},
                   "input_blocksize": {"type": "integer"},
                   "input_stepsize": {"type": "integer"}
               }
               }
    # Define Parameters

    class _Param(HasTraits):
        fft_size = Int()
        input_blocksize = Int()
        input_stepsize = Int()

    @store_parameters
    def __init__(self, input_blocksize=2048, input_stepsize=None,
                 fft_size=None):
        super(Spectrogram, self).__init__()

        self.input_blocksize = input_blocksize
        if input_stepsize:
            self.input_stepsize = input_stepsize
        else:
            self.input_stepsize = input_blocksize // 2

        if not fft_size:
            self.fft_size = input_blocksize
        else:
            self.fft_size = fft_size

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
        self.values.append(np.abs(np.fft.rfft(frames, self.fft_size)))
        return frames, eod

    def post_process(self):
        spectrogram = self.new_result(data_mode='value', time_mode='framewise')
        spectrogram.parameters = {'fft_size': self.fft_size}
        # spectrogram.data_object.value = self.values['spectrogram']
        spectrogram.data_object.value = self.values
        nb_freq = spectrogram.data_object.value.shape[1]
        spectrogram.data_object.y_value = (np.arange(0, nb_freq) *
                                           self.samplerate() / self.fft_size)
        self.add_result(spectrogram)


# Generate Grapher for Spectrogram analyzer
from timeside.core.grapher import DisplayAnalyzer

DisplayLinearSpectrogram = DisplayAnalyzer.create(
    analyzer=Spectrogram,
    result_id='spectrogram_analyzer',
    grapher_id='spectrogram',
    grapher_name='Linear Spectrogram',
    staging=False)


if __name__ == "__main__":
    import doctest
    import timeside
    doctest.testmod(timeside.plugins.analyzer.spectrogram, verbose=True)
