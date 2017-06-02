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

from ..exceptions import VampImportError

def discover_modules(subpackage, package=None):
    import pkgutil

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

    from timeside.core import _WITH_AUBIO, _WITH_YAAFE, _WITH_VAMP

    if name.count('.server.'):
        # TODO:
        # Temporary skip all timeside.server submodules before check dependencies
        return
    try:
        import_module(name, package)
    except VampImportError:
        # No Vamp Host
        if _WITH_VAMP:
            raise VampImportError
        else:
            # Ignore Vamp ImportError
            return
    except ImportError as e:
        if str(e).count('yaafelib') and not _WITH_YAAFE:
            # Ignore Yaafe ImportError
            return
        elif str(e).count('aubio') and not _WITH_AUBIO:
            # Ignore Aubio ImportError
            return
        elif str(e).count('DJANGO_SETTINGS_MODULE'):
            # Ignore module requiring DJANGO_SETTINGS_MODULE in environnement
            return
        else:
            print (name, package)
            raise e
    return name


# Check Availability of external Audio feature extraction librairies
def check_aubio():
    "Check Aubio availability"
    try:
        import aubio
    except ImportError:
        warnings.warn('Aubio librairy is not available', ImportWarning,
                      stacklevel=2)
        _WITH_AUBIO = False
    else:
        _WITH_AUBIO = True
        del aubio

    return _WITH_AUBIO


def check_yaafe():
    "Check Aubio availability"
    try:
        import yaafelib
    except ImportError:
        warnings.warn('Yaafe librairy is not available', ImportWarning,
                      stacklevel=2)
        _WITH_YAAFE = False
    else:
        _WITH_YAAFE = True
        del yaafelib
    return _WITH_YAAFE


def check_vamp():
    "Check Vamp host availability"

    try:
        from timeside.plugins.analyzer.externals import vamp_plugin
    except VampImportError:
        warnings.warn('Vamp host is not available', ImportWarning,
                      stacklevel=2)
        _WITH_VAMP = False
    else:
        _WITH_VAMP = True
        del vamp_plugin

    return _WITH_VAMP


def add_gstreamer_packages():
    import os
    import sys
    from distutils.sysconfig import get_python_lib

    dest_dir = get_python_lib()

    packages = ['gobject', 'glib', 'pygst', 'pygst.pyc', 'pygst.pth',
                'gst-0.10', 'pygtk.pth', 'pygtk.py', 'pygtk.pyc']

    python_version = sys.version[:3]
    global_path = os.path.join('/usr/lib', 'python' + python_version)
    global_sitepackages = [os.path.join(global_path,
                                        'dist-packages'),  # for Debian-based
                           os.path.join(global_path,
                                        'site-packages')]  # for others

    for package in packages:
        for pack_dir in global_sitepackages:
            src = os.path.join(pack_dir, package)
            sys.path.append(src)
            # dest = os.path.join(dest_dir, package)
            # if not os.path.exists(dest) and os.path.exists(src):
            #     os.symlink(src, dest)


def check_gstreamer():
    try:
        import gobject, pygst
    except ImportError:
        add_gstreamer_packages()
