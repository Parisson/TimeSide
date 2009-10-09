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

from timeside.analyze.core import *
from timeside.analyze.api import IMediaItemAnalyzer
import numpy
import datetime

class DurationAnalyzer(AudioProcessor):
    """Media item analyzer driver interface"""

    implements(IMediaItemAnalyzer)

    def get_id(self):
        return "duration"

    def get_name(self):
        return "Duration"

    def get_unit(self):
        return "h:m:s"

    def render(self, media_item, options=None):
        self.pre_process(media_item)
        media_time = numpy.round(float(self.frames)/float(self.samplerate),0)
        return datetime.timedelta(0,media_time)
