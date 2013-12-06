# -*- coding: utf-8 -*-

from timeside.decoder import *
from timeside.encoder import *
import os.path

source = os.path.join(os.path.dirname(__file__), "../samples/sweep.wav")
dest = os.path.join(os.path.dirname(__file__), "/tmp/sweep_wav.mp3")

decoder  = FileDecoder(source)
encoder  = Mp3Encoder(dest)

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

