# -*- coding: utf-8 -*-

from timeside.decoder import *
from timeside.encoder import *
import os.path
import sys

source = sys.argv[-1]
dest = source+'.flac'

decoder  = FileDecoder(source)
encoder  = FlacEncoder(dest, overwrite=True)

(decoder | encoder).run()
