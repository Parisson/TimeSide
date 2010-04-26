# -*- coding: utf-8 -*-
from timeside.tests.api import examples
from timeside.core import *
from timeside.api import *
import os

use_gst = 1
if use_gst:
    from timeside.tests.api.gstreamer import FileDecoder
else:
    from timeside.tests.api.examples import FileDecoder

sample_dir = '../samples'
img_dir = '../results/img'
if not os.path.exists(img_dir):
    os.mkdir(img_dir)

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
    waveform = examples.Waveform(width=1024, height=256, output=image, bg_color=(0,0,0), color_scheme='default')
    (decoder | waveform).run()
    print 'frames per pixel = ', waveform.graph.samples_per_pixel
    print "render waveform to: %s" %  image
    waveform.render()


