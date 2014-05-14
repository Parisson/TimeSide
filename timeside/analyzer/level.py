# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2009 Guillaume Pellerin <yomguy@parisson.com>
# Copyright (c) 2009 Olivier Guilyardi <olivier@samalyse.com>

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

# Author: Guillaume Pellerin <yomguy@parisson.com>

from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from timeside.api import IValueAnalyzer
import numpy as np
from timeside.analyzer.utils import MACHINE_EPSILON


class Level(Analyzer):

    """RMS level analyzer"""
    implements(IValueAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None,
              totalframes=None):
        super(Level, self).setup(channels, samplerate, blocksize, totalframes)
        # max_level
        self.max_value = 0
        # rms_level
        self.mean_values = np.array([])

    @staticmethod
    @interfacedoc
    def id():
        return "level"

    @staticmethod
    @interfacedoc
    def name():
        return "Level"

    @staticmethod
    @interfacedoc
    def unit():
        return "dBFS"

    def process(self, frames, eod=False):
        if frames.size:
            # max_level
            max_value = np.abs(frames).max()
            if max_value > self.max_value:
                self.max_value = max_value
            # rms_level
            self.mean_values = np.append(self.mean_values,
                                         np.mean(np.square(frames)))
        return frames, eod

    def post_process(self):
        # Max level
        max_level = self.new_result(data_mode='value', time_mode='global')

        max_level.id_metadata.id += '.' + "max"
        max_level.id_metadata.name += ' ' + "Max"

        if self.max_value == 0:  # Prevent np.log10(0) = Inf
            self.max_value = MACHINE_EPSILON

        max_level.data_object.value = np.round(
            20 * np.log10(self.max_value), 3)
        self.process_pipe.results.add(max_level)

        # RMS level
        rms_level = self.new_result(data_mode='value', time_mode='global')
        rms_level.id_metadata.id += '.' + "rms"
        rms_level.id_metadata.name += ' ' + "RMS"

        rms_val = np.sqrt(np.mean(self.mean_values))

        if rms_val == 0:
            rms_val = MACHINE_EPSILON

        rms_level.data_object.value = np.round(20 * np.log10(rms_val), 3)
        self.process_pipe.results.add(rms_level)
