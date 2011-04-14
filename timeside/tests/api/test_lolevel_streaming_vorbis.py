# -*- coding: utf-8 -*-

from timeside.core import *
from timeside.decoder import *
from timeside.analyzer import *
from timeside.encoder import *
from timeside.api import *

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
nframes = decoder.nframes()

dest1 = "/tmp/test_filesink.ogg"
dest2 = "/tmp/test_appsink.ogg"
f = open(dest2,'w')

streaming=True
encoder = VorbisEncoder(dest1, streaming=True)
encoder.setup(channels=channels, samplerate=samplerate)

print encoder.pipe

while True:
    encoder.process(*decoder.process())
    if streaming:
        f.write(encoder.chunk)
    if encoder.eod :
        break

f.close()
print encoder.pipe
