# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2009 Guillaume Pellerin <yomguy@parisson.com>

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

from timeside.analyzer.core import *
from timeside.api import IValueAnalyzer
import numpy


class MeanLevel(Processor):
    implements(IValueAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, nframes=None):
        super(MeanLevel, self).setup(channels, samplerate, nframes)
        self.value = -140

    @staticmethod
    @interfacedoc
    def id():
        return "meanlevel"

    @staticmethod
    @interfacedoc
    def name():
        return "Mean RMS level"

    @staticmethod
    @interfacedoc
    def unit():
        return "dB"

    def __str__(self):
        return "%s %s" % (str(self.value), unit())

    def process(self, frames, eod=False):
        max = numpy.round(20*numpy.log10(numpy.mean(numpy.sqrt(numpy.square(frames.max())))), 2)
        if max > self.value:
            self.value = max

        return frames, eod

    def result(self):
        return self.value

