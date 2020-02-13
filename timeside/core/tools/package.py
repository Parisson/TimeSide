# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2014 Thomas Fillon <thomas.fillon@parisson.com>

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

# Author: Thomas Fillon <thomas.fillon@parisson.com>


from importlib import import_module
import warnings
import pkgutil

def discover_modules(subpackage, package=None):

    if package:
        try:
            _pkg = import_module('.' + subpackage, package)
        except ImportError as e:
            raise e
    else:
        _pkg = import_module(subpackage)

    pkg_path = _pkg.__path__
    pkg_prefix = _pkg.__name__ + '.'

    _list = [import_module_with_exceptions(modname)
             for importer, modname, ispkg
             in pkgutil.walk_packages(pkg_path, pkg_prefix)]

    modules_list = [mod for mod in _list if mod is not None]
    return modules_list


def import_module_with_exceptions(name, package=None):
    """Wrapper around importlib.import_module to import TimeSide subpackage
    and ignoring ImportError if Aubio, Yaafe and Vamp Host are not available"""

    if name.count('.server.'):
        # TODO:
        # Temporary skip all timeside.server submodules before check dependencies
        return
    try:
        import_module(name, package)
    except Exception as e:
        warnings.warn("Failed loading %s (%s)" % (name, e), UserWarning,
                stacklevel=2)
        #raise e
        return
    return name
