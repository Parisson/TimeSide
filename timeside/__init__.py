# -*- coding: utf-8 -*-

import api

def get_processors(proc_type):
    import timeside.decoder
    import timeside.encoder
    import timeside.grapher
    import timeside.analyzer
    return core.processors(proc_type)

__version__ = '0.5'
