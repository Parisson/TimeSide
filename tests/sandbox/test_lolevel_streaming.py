# -*- coding: utf-8 -*-

from timeside.core import *
from timeside.decoder import FileDecoder
from timeside.encoder import Mp3Encoder

import sys
if len(sys.argv) > 1:
    source = sys.argv[1]
else:
    import os.path
    source= os.path.join (os.path.dirname(__file__),  "../samples/sweep.flac")

decoder = FileDecoder(source)

print "Creating decoder with id=%s for: %s" % (decoder.id(), source)
decoder.setup()

channels  = decoder.channels()
print 'channels :', channels
samplerate = decoder.samplerate()
#nframes = decoder.nframes()

dest1 = "/tmp/test_filesink.mp3"
dest2 = "/tmp/test_appsink.mp3"
f = open(dest2,'w')

streaming=True
encoder = Mp3Encoder(dest1, streaming=True, overwrite=True)
encoder.setup(channels=channels, samplerate=samplerate,
              blocksize=decoder.blocksize(), totalframes=decoder.totalframes())
while True:
    encoder.process(*decoder.process())
    if streaming:
        f.write(encoder.chunk)
    if encoder.eod:
        break

f.close()
print encoder.pipe

import os
dest1_size = os.path.getsize(dest1)
dest2_size = os.path.getsize(dest2)

print "sizes : %d , %d" % (dest1_size, dest2_size)

assert os.path.getsize(dest1)==os.path.getsize(dest2)
