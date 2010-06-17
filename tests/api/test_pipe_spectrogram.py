# -*- coding: utf-8 -*-

import os
from timeside.core import *
from timeside.api import *
from timeside.decoder import *
from timeside.grapher import *

image_file = '../results/img/spectrogram.png'
source = os.path.join(os.path.dirname(__file__), "../samples/sweep.wav")

decoder  = FileDecoder(source)
spectrogram = Spectrogram(width=1024, height=256, output=image_file, bg_color=(0,0,0), color_scheme='default')

(decoder | spectrogram).run()

print 'frames per pixel = ', spectrogram.graph.samples_per_pixel
print "render spectrogram to: %s" % image_file
spectrogram.render()


