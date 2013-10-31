# -*- coding: utf-8 -*-

import os
from timeside.core import *
from timeside.api import *
from timeside.decoder import *
from timeside.grapher import *

sample_dir = '/home/momo/music_local/Isabelle Aboulker/Mon imagier des instruments/wav/'
img_dir = '../results/img'
if not os.path.exists(img_dir):
    os.mkdir(img_dir)

for source in os.listdir(sample_dir):
    audio = sample_dir + os.sep + source
    image = img_dir + os.sep + source + '.png'
    print 'Test : decoder(%s) | waveform (%s)' % (source, image)
    decoder  = FileDecoder(audio)
    waveform = Waveform(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')
    (decoder | waveform).run()
    print 'frames per pixel = ', waveform.graph.samples_per_pixel
    print "render waveform to: %s" %  image
    waveform.render(image)



