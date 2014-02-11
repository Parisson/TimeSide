# -*- coding: utf-8 -*-

import os, sys, time

from timeside.core import *
from timeside.decoder import *
from timeside.analyzer import *
from timeside.encoder import *
from timeside.api import *


if len(sys.argv) > 1:
    source = sys.argv[1]
else:
    import os.path
    source= os.path.join(os.path.dirname(__file__),  "../samples/sweep.wav")

streaming = True

dest1 = "/tmp/test_filesink.mp3"
dest2 = "/tmp/test_appsink.mp3"
f = open(dest2,'w')

decoder = FileDecoder(source)
decoder.setup()

encoder = Mp3Encoder(dest1, streaming=streaming, overwrite=True)
encoder.setup(channels=decoder.channels(), samplerate=decoder.samplerate(),
              blocksize=decoder.blocksize(), totalframes=decoder.totalframes())

print encoder.pipe

while True:
    encoder.process(*decoder.process())
    # time.sleep(0.1)
    if streaming:
    	f.write(encoder.chunk)
    if encoder.eod:
        break

decoder.release()
encoder.release()
f.close()

os.system('ls -tl /tmp/test*')