# -*- coding: utf-8 -*-
from timeside.tests.api import examples
from timeside.core import *
from timeside.api import *

use_gst = 1
if use_gst:
    from timeside.tests.api.gstreamer import FileDecoder, WavEncoder
else:
    from timeside.tests.api.examples import FileDecoder, WavEncoder

image_file = './spectrogram.png'
source = '../samples/sweep.wav'

decoder  = FileDecoder(source)
spectrogram = examples.Spectrogram(width=1024, height=256, output=image_file, bg_color=(0,0,0), color_scheme='default')

(decoder | spectrogram).run()

print 'frames per pixel = ', spectrogram.graph.samples_per_pixel
print "render spectrogram to: %s" % image_file
spectrogram.render()


