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

from timeside.core import Processor, implements, interfacedoc, FixedSizeInputAdapter
from timeside.analyzer.core import *
from timeside.api import IValueAnalyzer


class Duration(Processor):
    """A rather useless duration analyzer. Its only purpose is to test the
       nframes characteristic."""
    implements(IValueAnalyzer)

    @interfacedoc
    def setup(self, channels, samplerate, blocksize=None, totalframes=None):
        super(Duration, self).setup(channels, samplerate, blocksize, totalframes)
        if not totalframes:
            raise Exception("nframes argument required")

    @staticmethod
    @interfacedoc
    def id():
        return "duration"

    @staticmethod
    @interfacedoc
    def name():
        return "Duration"

    @staticmethod
    @interfacedoc
    def unit():
        return "seconds"

    def __str__(self):
        return "%s %s" % (str(self.value), unit())

    def process(self, frames, eod=False):
        return frames, eod

    def result(self):
        return self.input_nframes / float(self.input_samplerate)

