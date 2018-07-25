# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2009 Guillaume Pellerin <yomguy@parisson.com>
# Copyright (c) 2009 Olivier Guilyardi <olivier@samalyse.com>

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

# Author: Guillaume Pellerin <yomguy@parisson.com>

from timeside.core import implements, interfacedoc
from timeside.core.analyzer import Analyzer
from timeside.core.api import IValueAnalyzer
import numpy as np
from timeside.plugins.analyzer.utils import MACHINE_EPSILON


class Level(Analyzer):

    """Audio level analyzer

    Examples
    --------

    >>> import timeside
    >>> from timeside.core import get_processor
    >>> from timeside.core.tools.test_samples import samples
    >>> source = samples['sweep.mp3']
    >>> decoder = get_processor('file_decoder')(uri=source)
    >>> level = get_processor('level')()
    >>> (decoder | level).run()
    >>> level.results.keys()
    ['level.max', 'level.rms']
    >>> max = level.results['level.max']
    >>> print max.data
    [0.]
    >>> rms = level.results['level.rms']
    >>> print rms.data  # doctest: +ELLIPSIS
    [-3.26...]
    """
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
        return "Level Analyzer"

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
        self.add_result(max_level)

        # RMS level
        rms_level = self.new_result(data_mode='value', time_mode='global')
        rms_level.id_metadata.id += '.' + "rms"
        rms_level.id_metadata.name += ' ' + "RMS"

        rms_val = np.sqrt(np.mean(self.mean_values))

        if rms_val == 0:
            rms_val = MACHINE_EPSILON

        rms_level.data_object.value = np.round(20 * np.log10(rms_val), 3)
        self.add_result(rms_level)

if __name__ == "__main__":
    import doctest
    import timeside
    doctest.testmod(timeside.analyzer.level)
