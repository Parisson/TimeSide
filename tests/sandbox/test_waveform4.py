# -*- coding: utf-8 -*-

import os
from timeside.core import *
from timeside.api import *
from timeside.decoder import *
from timeside.grapher import *

sample = '/home/momo/music_local/Isabelle Aboulker/Mon imagier des instruments/16 - Isabelle Aboulker - 16 instru.flac'
img_dir = '../results/img'
if not os.path.exists(img_dir):
    os.mkdir(img_dir)

audio = sample
image = img_dir + os.sep + 'toto.png'
decoder  = FileDecoder(audio)
waveform = Waveform(width=1211, height=170, bg_color=(0,0,0), color_scheme='default')
(decoder | waveform).run()
print 'frames per pixel = ', waveform.graph.samples_per_pixel
print "render waveform to: %s" %  image
waveform.render(image)



