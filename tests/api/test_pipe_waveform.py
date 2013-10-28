# -*- coding: utf-8 -*-

import os
from timeside.core import *
from timeside.api import *
from timeside.decoder import *
from timeside.grapher import *

sample_dir = '../samples'
img_dir = '../results/img'
if not os.path.exists(img_dir):
    os.makedirs(img_dir)

test_dict = {'sweep.wav': 'waveform_wav.png',
            'sweep.flac': 'waveform_flac.png',
            'sweep.ogg': 'waveform_ogg.png',
            'sweep.mp3': 'waveform_mp3.png',
            }

for source, image in test_dict.iteritems():
    audio = os.path.join(os.path.dirname(__file__), sample_dir + os.sep + source)
    image = img_dir + os.sep + image
    print 'Test : decoder(%s) | waveform (%s)' % (source, image)
    decoder  = FileDecoder(audio)
    waveform = Waveform(width=1024, height=256, bg_color=(255,255,255), color_scheme='default')
    (decoder | waveform).run()
    print 'frames per pixel = ', waveform.samples_per_pixel
    print "render waveform to: %s" %  image
    waveform.render(image)
