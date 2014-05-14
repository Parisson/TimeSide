# -*- coding: utf-8 -*-
from __future__ import absolute_import

# ----- Load external libraries ------
# Aubio
try:
    WITH_AUBIO = True
    import aubio
except ImportError:
    WITH_AUBIO = False
else:
    del aubio

# Yaafe
try:
    WITH_YAAFE = True
    import yaafelib
except ImportError:
    WITH_YAAFE = False
else:
    del yaafelib

# Vamp Plugins
try:
    from . vamp_plugin import VampSimpleHost
    VampSimpleHost.SimpleHostProcess(['-v'])
    WITH_VAMP = True
except OSError:
    WITH_VAMP = False
