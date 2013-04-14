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

# Authors:
#   Guillaume Pellerin <yomguy at parisson.com>

class AnalyzerResult(object):

    def __init__(self, id = "", name = "", unit = "s", value = None):
        self.id = id
        self.name = name
        self.unit = unit
        self.value = value

    def __repr__(self):
        o = {}
        for attr in ['id', 'name', 'unit', 'value']:
            o[attr] = getattr(self, attr)
        return repr(o)
