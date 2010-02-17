from timeside.tests.api import examples
from timeside.core import *
from timeside.api import *
from sys import stdout

import os.path
source = os.path.join (os.path.dirname(__file__), "../samples/guitar.wav")

print "Normalizing %s" % source
decoder  = examples.FileDecoder(source)
maxlevel = examples.MaxLevel()
waveform = examples.Waveform(1024, 256, 'waveform.png')
#waveform.set_colors((0xFF, 0xFF, 0xFF), 'iso')

(decoder | maxlevel | waveform).run()

gain = 1
if maxlevel.result() > 0:
    gain = 0.9 / maxlevel.result()

print "input maxlevel: %f" % maxlevel.result()
print "gain: %f" % gain

gain     = examples.Gain(gain)
encoder  = examples.WavEncoder("normalized.wav")

subpipe  = gain | maxlevel

(decoder | subpipe | encoder).run()

print "output maxlevel: %f" % maxlevel.result()


