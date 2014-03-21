# -*- coding: utf-8 -*-

import sys
import time
import timeside

metadata = {'TIT2': 'title',  #title2
             'TCOM': 'composer',  #composer
             'TPE1': 'lead creator', #lead
             'UFID': 'identifier',  #Unique ID...
             'TALB': 'album',  #album
             'TCON': 'genre',  #genre
             'TDRC': '2011', #year
#             'COMM': 'blabla',  #comment
             }

decoder  =  timeside.decoder.FileDecoder(sys.argv[-1])

encoder  =  timeside.encoder.Mp3Encoder('/tmp/output.mp3', overwrite=True)
encoder.set_metadata(metadata)

(decoder | encoder).run()
