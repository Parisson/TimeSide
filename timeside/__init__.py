# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Thomas Fillon <thomas@parisson.com>

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
#
# Authors:
# Thomas Fillon <thomas@parisson.com>

from __future__ import absolute_import

from . import api
from . import core


__version__ = '0.5.6.3'

# Check Availability of external Audio feature extraction librairies
from .tools import package as ts_package
_WITH_AUBIO = ts_package.check_aubio()
_WITH_YAAFE = ts_package.check_yaafe()
_WITH_VAMP = ts_package.check_vamp()


_packages_with_processors = ['decoder', 'analyzer', 'encoder', 'grapher']

__all__ = ['api', 'core']
__all__.extend(_packages_with_processors)

for _sub_pkg in _packages_with_processors:
    ts_package.discover_modules(_sub_pkg, __name__)

# Clean-up
del ts_package
del _packages_with_processors
del _sub_pkg
del absolute_import
