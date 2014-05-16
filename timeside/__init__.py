# -*- coding: utf-8 -*-
from __future__ import absolute_import

from . import api
from . import core


__version__ = '0.5.5'

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
