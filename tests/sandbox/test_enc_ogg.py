# -*- coding: utf-8 -*-

from timeside.decoder import *
from timeside.encoder import *
import os.path
import sys

if len(sys.argv) < 2:
    print 'usage:', sys.argv[0], '<inputfile>'
    sys.exit(1)

source = sys.argv[-1]
dest = source+'.ogg'

print 'converting', source, 'to', dest

decoder  = FileDecoder(source)
encoder  = VorbisEncoder(dest, overwrite=True)

(decoder | encoder).run()
