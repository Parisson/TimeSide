# -*- coding: utf-8 -*-
from timeside.tests.api import examples
from timeside.core import *
from timeside.api import *
import os.path

use_gst = 1
if use_gst:
    from timeside.tests.api.gstreamer import FileDecoder, WavEncoder
else:
    from timeside.tests.api.examples import FileDecoder, WavEncoder

image_file = './waveform.png'
source = '../samples/sweep.wav'

decoder  = FileDecoder(source)
waveform = examples.Waveform(width=1024, height=256, output=image_file, bg_color=(0,0,0), color_scheme='default')

(decoder | waveform).run()

print 'frames per pixel = ', waveform.graph.samples_per_pixel
print "render waveform to: %s" % image_file
waveform.render()


