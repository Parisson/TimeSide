# -*- coding: utf-8 -*-

from timeside.core import *
from timeside.decoder.file import FileDecoder
from timeside.encoder import Mp3Encoder

import sys
if len(sys.argv) > 1:
    source = sys.argv[1]
else:
    import os.path
    audio_file = '../samples/sweep.flac'
    source = os.path.join(os.path.dirname(__file__), audio_file)

#source = '/home/thomas/data/CNRSMH_E_1985_001_001_001_04.wav'
decoder = FileDecoder(source)

print "Creating decoder with id=%s for: %s" % (decoder.id(), source)

dest1 = "/tmp/test_filesink.mp3"
dest2 = "/tmp/test_appsink.mp3"
f = open(dest2, 'w')


streaming = True
encoder = Mp3Encoder(dest1, streaming=streaming, overwrite=True)

pipe = (decoder | encoder)
print pipe
#pipe.run()

for chunk in pipe.stream():
    f.write(chunk)
#while True:
#    encoder.process(*decoder.process())
#    if streaming:
#        f.write(encoder.chunk)
#    if encoder.eod:
#        break

f.close()
#print encoder.pipe

import os
dest1_size = os.path.getsize(dest1)
dest2_size = os.path.getsize(dest2)

print "Filesink filesize: %d" % dest1_size
print "Appsink filesize: %d" % dest2_size
#assert os.path.getsize(dest1) == os.path.getsize(dest2)
