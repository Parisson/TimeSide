# -*- coding: utf-8 -*-

from timeside.decoder import *
from timeside.encoder import *
import os.path
import sys

if len(sys.argv) < 2:
    print 'usage:', sys.argv[0], '<inputfile>'
    sys.exit(1)

source = sys.argv[-1]
dest = source+'.mp3'

print 'converting', source, 'to', dest

decoder  = FileDecoder(source)
encoder  = Mp3Encoder(dest, overwrite=True)

(decoder | encoder).run()

metadata = {'TIT2': 'title',  #title2
             'TCOM': 'composer',  #composer
             'TPE1': 'lead creator', #lead
             'UFID': 'identifier',  #Unique ID...
             'TALB': 'album',  #album
             'TCON': 'genre',  #genre
             'TDRC': '2011', #year
#             'COMM': 'blabla',  #comment
             }

encoder.set_metadata(metadata)
encoder.write_metadata()
