# -*- coding: utf-8 -*-

import api
import core
import decoder
import analyzer
import grapher
import encoder

__version__ = '0.5.5'

__all__ = ['api', 'core', 'decoder', 'analyzer', 'grapher', 'encoder']

print __file__
print __name__

def _discover_modules():
    import sys
    import pkgutil
    import importlib
    pkg = 'timeside'
    #__import__(pkg)
    package = sys.modules[pkg]
    prefix = pkg + "."

    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__,
                                                          prefix):
        #print modname
        if modname.split('.')[1] in ['decoder', 'analyzer', 'encoder', 'grapher']:
            print modname
            mod = importlib.import_module(modname)

            del mod
        del modname


_discover_modules()
