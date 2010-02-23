# -*- coding: utf-8 -*-
from timeside.tests.api import examples
from timeside.core import *
from timeside.api import *
from sys import stdout

import os.path
source = os.path.join(os.path.dirname(__file__), "../samples/sweep_source.wav")
waveform_image = './waveform.png'

print "Normalizing %s" % source
decoder  = examples.FileDecoder(source)
maxlevel = examples.MaxLevel()
waveform = examples.Waveform(width=936, height=200, output=waveform_image)

(decoder | maxlevel).run()

gain = 1
if maxlevel.result() > 0:
    gain = 0.99 / maxlevel.result()

print "input maxlevel: %f" % maxlevel.result()
print "gain: %f" % gain

gain     = examples.Gain(gain)
subpipe  = gain | maxlevel

(decoder | subpipe | waveform).run()

print "render waveform to: %s" % waveform_image
waveform.render()

print "output maxlevel: %f" % maxlevel.result()


