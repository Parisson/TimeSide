# -*- coding: utf-8 -*-

from timeside.core import *
from timeside.decoder import FileDecoder
from timeside.encoder import Mp3Encoder

import sys
if len(sys.argv) > 1:
    source = sys.argv[1]
else:
    import os.path
    audio_file = '../samples/sweep.flac'
    source = os.path.join(os.path.dirname(__file__), audio_file)

decoder = FileDecoder(audio_file)

print "Creating decoder with id=%s for: %s" % (decoder.id(), audio_file)

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

print "sizes : %d , %d" % (dest1_size, dest2_size)

assert os.path.getsize(dest1) == os.path.getsize(dest2)

# Sometime randomly freeze
# Appsink file is always 1 buffer longer than filesink
# TODO : Try to transcode with a pure gstreamer pipe to see the file length
# maybe appsink is fine but filesink not ? just to be checked
