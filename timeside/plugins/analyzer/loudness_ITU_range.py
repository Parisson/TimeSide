# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Thomas Fillon <thomas@parisson.com>
# Copyright (C) 2014-2015 Elio Quinton

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
#
# Thomas Fillon <thomas@parisson.com>
# Elio Quinton

from timeside.core import implements, interfacedoc
from timeside.core.analyzer import Analyzer
from timeside.core.api import IValueAnalyzer
from timeside.core import get_processor
from timeside.core.tools.parameters import HasTraits
from timeside.core.preprocessors import downmix_to_mono, frames_adapter

import numpy as np
import numpy as np
from scipy.signal import lfilter as lfilter
import warnings
#from timeside.core.tools.parameters import store_parameters


class LoudnessITURange(Analyzer):

    """ Measure of audio loudness Range using standard ITU-R BS.1770-3

    WARNING: Sampling frequencies other that 44100Hz and 48000Hz are not fully supported 
    """

    implements(IValueAnalyzer)

    class _Param(HasTraits):
        pass

    _schema = {'$schema': 'http://json-schema.org/schema#',
               'properties': {},
               'type': 'object'}

    #@store_parameters
    def __init__(self):
        super(LoudnessITURange, self).__init__()
        self.parents['loudness'] = get_processor('loudness_itu')()
        self.parents['silence'] = get_processor('aubio_silence')()

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(LoudnessITURange, self).setup(
            channels, samplerate, blocksize, totalframes)

    @staticmethod
    @interfacedoc
    def id():
        return "loudness_itu_range"

    @staticmethod
    @interfacedoc
    def name():
        return "Loudness ITU Range"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def process(self, frames, eod=False):
        return frames, eod

    def post_process(self):
        res_silence = self.parents['silence'].results['aubio_silence']
        res_loudness = self.parents['loudness'].results['loudness_itu.block_loudness']

        start_time = min(res_silence.time[res_silence.data==1])
        end_time = max(res_silence.time[res_silence.data==1] +
                   res_silence.duration[res_silence.data==1])
        end_time -= res_loudness.duration[0]
        loudness = res_loudness.data[(res_loudness.time<end_time) & (res_loudness.time>start_time)]
        loudness_range = np.abs(np.max(loudness)-np.min(loudness))
        result_value = self.new_result(data_mode='value', time_mode='global')
        result_value.data_object.value = loudness_range
        self.add_result(result_value)
