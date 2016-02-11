# -*- coding: utf-8 -*-
#
# Copyright (c) 20013-2014 Parisson SARL
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

from timeside.core import implements, interfacedoc
from timeside.core.analyzer import Analyzer
from timeside.core.api import IAnalyzer
import numpy as np


class Waveform(Analyzer):

    """Waveform analyzer"""
    implements(IAnalyzer)  # TODO check if needed with inheritance

    def __init__(self):
        super(Waveform, self).__init__()
#        self.input_blocksize = 2048
#        self.input_stepsize = self.input_blocksize / 2

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(Waveform, self).setup(channels, samplerate,
                                    blocksize, totalframes)
        self.values = []
        self.result_blocksize = 1
        self.result_stepsize = 1

    @staticmethod
    @interfacedoc
    def id():
        return "waveform_analyzer"

    @staticmethod
    @interfacedoc
    def name():
        return "Waveform Analyzer"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

#    @downmix_to_mono
#    @frames_adapter
    def process(self, frames, eod=False):
        self.values.append(frames)
        return frames, eod

    def post_process(self):
        waveform = self.new_result(data_mode='value', time_mode='framewise')
        waveform.data_object.value = np.vstack(self.values)
        self.add_result(waveform)


# Generate Grapher for Waveform analyzer
from timeside.core.grapher import DisplayAnalyzer
DisplayWaveform = DisplayAnalyzer.create(analyzer=Waveform,
                                         result_id='waveform_analyzer',
                                         grapher_id='grapher_waveform',
                                         grapher_name='Waveform from Analyzer',
                                         staging=True)

