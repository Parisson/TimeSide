from numpy import vstack, zeros

from timeside.decoder import *
from timeside.encoder import *

import sys, os.path

def transcode(source, target):
    decoder = FileDecoder(source)
    decoder.setup()

    channels  = decoder.channels()
    samplerate = decoder.samplerate()

    print channels, samplerate

    encoder = Mp3Encoder(target)
    encoder.setup(channels = channels, samplerate = samplerate)

    totalframes = 0
    while True:
        frames, eod = decoder.process()
        encoder.process(frames, eod)
        totalframes += frames.shape[0]
        if eod or encoder.eod:
            break

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print 'needs 2 args'
        sys.exit(1)
    transcode(sys.argv[1], sys.argv[2])
