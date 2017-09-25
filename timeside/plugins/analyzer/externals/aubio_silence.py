# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Thomas Fillon <thomas@parisson.com>

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

# Authors:
#  Thomas Fillon <thomas@parisson.com>

from __future__ import absolute_import

from timeside.core import implements, interfacedoc
from timeside.core.analyzer import Analyzer
from timeside.core.api import IAnalyzer
from timeside.core.preprocessors import downmix_to_mono, frames_adapter
from timeside.core.tools.parameters import Float, HasTraits
from timeside.core.tools.parameters import store_parameters


from aubio import silence_detection

import numpy as np


class AubioSilence(Analyzer):

    """Aubio Silence detection analyzer"""
    implements(IAnalyzer)
    # Define Parameters

    class _Param(HasTraits):
        threshold = Float

    @store_parameters
    def __init__(self, threshold=80):
        super(AubioSilence, self).__init__()
        self.input_blocksize = 1024
        self.input_stepsize = 1024
        self.threshold = threshold
        self.silence = []

    @interfacedoc
    def setup(self,
              channels=None,
              samplerate=None,
              blocksize=None,
              totalframes=None):
        super(AubioSilence, self).setup(channels, samplerate,
                                        blocksize, totalframes)

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_silence"

    @staticmethod
    @interfacedoc
    def name():
        return "silence detection (aubio)"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    @downmix_to_mono
    @frames_adapter
    def process(self, frames, eod=False):
        self.silence.append(silence_detection(frames, self.threshold))
        return frames, eod

    def post_process(self):

        silence = self.new_result(data_mode='label', time_mode='segment')
        silence.data_object.time = (np.arange(0, len(self.silence) * self.input_stepsize,
                                              self.input_stepsize) / self.input_samplerate)
        silence.data_object.label = np.array(self.silence, dtype=int)
        duration = self.input_blocksize / float(self.input_samplerate)
        silence.data_object.duration = np.ones(silence.data_object.label.shape) * duration
        silence.data_object.label_metadata.label = {0: 'Silence', 1: 'Not Silence'}
        silence.data_object.merge_segment()

        self.add_result(silence)

# Generate Grapher
from timeside.core.grapher import DisplayAnalyzer

DisplayAubioSilence = DisplayAnalyzer.create(
    analyzer=AubioSilence,
    result_id='aubio_silence',
    grapher_id='grapher_aubio_silence',
    grapher_name='Aubio Silence',
    staging=False)
