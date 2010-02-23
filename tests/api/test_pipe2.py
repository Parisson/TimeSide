from timeside.tests.api import examples
from timeside.core import *
from timeside.api import *
from sys import stdout

use_gst = 0
if use_gst:
    from timeside.tests.api.gstreamer import FileDecoder, WavEncoder
else:
    from timeside.tests.api.examples import FileDecoder, WavEncoder

import os.path
source = os.path.join (os.path.dirname(__file__), "../samples/guitar.wav")

print "Normalizing %s" % source
decoder  = FileDecoder(source)
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
encoder  = WavEncoder("normalized.wav")

subpipe  = gain | maxlevel

(decoder | subpipe | encoder).run()

print "output maxlevel: %f" % maxlevel.result()


