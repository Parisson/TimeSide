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

from timeside.core import Processor, implements, interfacedoc,  \
                            FixedSizeInputAdapter
from timeside.analyzer.core import Analyzer
from timeside.api import IValueAnalyzer
import numpy


class Level(Analyzer):
    implements(IValueAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None,
              totalframes=None):
        super(Level, self).setup(channels, samplerate, blocksize, totalframes)
        # max_level
        self.max_value = 0
        # rms_level
        self.mean_values = numpy.array([])

    @staticmethod
    @interfacedoc
    def id():
        return "level_analyzer"

    @staticmethod
    @interfacedoc
    def name():
        return "level analyzer"

    def process(self, frames, eod=False):
        if frames.size:
            # max_level
            max_value = frames.max()
            if max_value > self.max_value:
                self.max_value = max_value
            # rms_level
            self.mean_values = numpy.append(self.mean_values,
                                            numpy.mean(numpy.square(frames)))
        return frames, eod

    def release(self):
        # Max level
        max_level = self.new_result(dataMode='value', timeMode='global')

        max_level.idMetadata.id = "max_level"
        max_level.idMetadata.name = "Max level"
        max_level.idMetadata.unit = "dBFS"

        max_level.data.value = numpy.round(20*numpy.log10(self.max_value), 3)
        self.resultContainer.add_result(max_level)

        # RMS level
        rms_level = self.new_result(dataMode='value', timeMode='global')
        rms_level.idMetadata.id = "rms_level"
        rms_level.idMetadata.name="RMS level"
        rms_level.idMetadata.unit="dBFS"

        rms_level.data.value = numpy.round(20*numpy.log10(
                                numpy.sqrt(numpy.mean(self.mean_values))), 3)
        self.resultContainer.add_result(rms_level)

