# -*- coding: utf-8 -*-

import timeside.core
from timeside.api import IEncoder

TS_ENCODERS = timeside.core.processors(IEncoder)
TS_ENCODERS_EXT = {encoder.file_extension(): encoder.id()
                   for encoder in TS_ENCODERS
                   if encoder.file_extension()}

