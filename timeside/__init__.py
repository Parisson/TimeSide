# -*- coding: utf-8 -*-
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
