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
from . import decoder
from . import analyzer
from . import grapher
from . import encoder


__version__ = '0.5.5'

__all__ = ['api', 'core', 'decoder', 'analyzer', 'grapher', 'encoder']


def _discover_modules():
    import sys
    import pkgutil
    import importlib

    #pkg_path = os.path.abspath()

    #__import__(pkg)

    proc_modules = ['decoder', 'analyzer', 'encoder', 'grapher']

    for module in proc_modules:
        pkg = '.'.join([__name__, module])
        importlib.import_module(pkg)
        package = sys.modules[pkg]
        prefix = pkg + "."

        for importer, modname, ispkg in pkgutil.walk_packages(package.__path__,
                                                              prefix):
            try:
                importlib.import_module(modname)
                #__import__(modname)
            except ImportError as e:
                if e.message.count('yaafelib'):
                    print 'No Yaafe'
                elif e.message.count('aubio'):
                    print 'No Aubio'
                else:
                    raise e

_discover_modules()
