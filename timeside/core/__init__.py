# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Thomas Fillon <thomas@parisson.com>

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
#
# Authors:
# Thomas Fillon <thomas@parisson.com>

from __future__ import absolute_import

from . import api
from . import processor
from . import provider

from .processor import Processor, get_processor, list_processors
from .provider import get_provider, list_providers
from .component import implements, interfacedoc, abstract

__version__ = '0.9'

from .tools import package as ts_package

# Check Availability of Gstreamer python bindings
ts_package.check_gstreamer()

# Check Availability of external Audio feature extraction librairies
_WITH_AUBIO = ts_package.check_aubio()
_WITH_YAAFE = ts_package.check_yaafe()
_WITH_VAMP = ts_package.check_vamp()

__all__ = ['api', 'processor']

ts_package.discover_modules('plugins', 'timeside')#__name__)

# Clean-up
del ts_package
del absolute_import
