# -*- coding: utf-8 -*-

from timeside.decoder import *
from timeside.encoder import *
import os.path
import sys

source = sys.argv[-1]
dest = source+'.ogg'

decoder  = FileDecoder(source)
encoder  = VorbisEncoder(dest)

(decoder | encoder).run()
