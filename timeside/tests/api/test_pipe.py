# -*- coding: utf-8 -*-

from timeside.tests.api.examples import Gain
from timeside.core import *
from timeside.decoder import *
from timeside.analyzer import *
from timeside.encoder import *
from timeside.api import *
from sys import stdout
import os.path
import numpy

source = os.path.join(os.path.dirname(__file__),  "../samples/guitar.wav")

print "Normalizing %s" % source
decoder  = FileDecoder(source)
maxlevel = MaxLevel()
duration = Duration()

(decoder | maxlevel | duration).run()

gain = 1
if maxlevel.result() < 0:
    gain = 0.9 / numpy.exp(maxlevel.result()/20)

print "input maxlevel: %f" % maxlevel.result()
print "gain: %f" % gain
print "duration: %f %s" % (duration.result(), duration.unit())

gain     = Gain(gain)
encoder  = WavEncoder("../results/guitar_normalized.wav")

subpipe  = gain | maxlevel

(decoder | subpipe | encoder).run()

print "output maxlevel: %f" % maxlevel.result()


