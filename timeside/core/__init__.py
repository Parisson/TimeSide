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

import sys

from . import api
from . import processor

from .processor import get_processor, Processor, list_processors
from .component import implements, interfacedoc, abstract
from .tools import package as ts_package

# TODO: enable to get TimeSide version without `import timeside.core`
__version__ = '1.0'

__all__ = ['api', 'processor']

# this line will import all plugins found inside timeside/plugins
ts_package.discover_modules('plugins', 'timeside')

# avoid *.pyc file generation
sys.dont_write_bytecode = True
