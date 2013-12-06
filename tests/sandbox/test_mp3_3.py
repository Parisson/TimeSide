# -*- coding: utf-8 -*-

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

decoder  =  timeside.decoder.FileDecoder('/home/momo/dev/telemeta/sandboxes/sandbox_lam/media/items/2012/09/26/LAM_ETUD_01_01_004.wav')

encoder  =  timeside.encoder.Mp3Encoder('/tmp/output.mp3')
encoder.set_metadata(metadata)

(decoder | encoder).run()

