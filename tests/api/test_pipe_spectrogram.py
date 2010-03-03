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

image_file = './spectrogram.png'

# mono
#source = os.path.join(os.path.dirname(__file__), "../samples/sweep_source.wav")
#source = os.path.join(os.path.dirname(__file__), "../samples/guitar.wav")
#source = os.path.join(os.path.dirname(__file__), "../samples/sweep_source.mp3")

# stereo
source = os.path.join(os.path.dirname(__file__), "../samples/sweep.wav")
#source = os.path.join(os.path.dirname(__file__), "../samples/guitar_stereo.wav")
#source = os.path.join(os.path.dirname(__file__), "/home/momo/music/flac/Isabelle Aboulker/Mon imagier des instruments/16 - Isabelle Aboulker - 16 instru.flac")
#source = os.path.join(os.path.dirname(__file__), "/home/momo/music/ogg/Emilie_Jolie/01 - Henri Salvador - Prologue.ogg")

decoder  = FileDecoder(source)
spectrogram = examples.Spectrogram(width=1024, height=256, output=image_file, bg_color=(0,0,0), color_scheme='default')

(decoder | spectrogram).run()

print 'frames per pixel = ', spectrogram.graph.samples_per_pixel
print "render spectrogram to: %s" % image_file
spectrogram.render()


