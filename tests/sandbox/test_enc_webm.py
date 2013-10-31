# -*- coding: utf-8 -*-

from timeside.decoder import *
from timeside.encoder import *
import os.path
import sys

source = sys.argv[-1]
dest = source+'.webm'

decoder  = FileDecoder(source)
encoder  = WebMEncoder(dest)

(decoder | encoder).run()
