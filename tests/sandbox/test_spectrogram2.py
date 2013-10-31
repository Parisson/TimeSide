# -*- coding: utf-8 -*-

import os
from timeside.decoder import *
from timeside.grapher import *

sample_dir = '../samples'
img_dir = '../results/img'
if not os.path.exists(img_dir):
    os.mkdir(img_dir)

test_dict = {'sweep.wav': 'spec_wav.png',}

for source, image in test_dict.iteritems():
    audio = os.path.join(os.path.dirname(__file__), sample_dir + os.sep + source)
    image = img_dir + os.sep + image
    print 'Test : decoder(%s) | waveform (%s)' % (source, image)
    decoder  = FileDecoder(audio)
    spectrogram = SpectrogramLinear()
    (decoder | spectrogram).run()
    print 'frames per pixel = ', spectrogram.samples_per_pixel
    print "render spectrogram to: %s" %  image
    spectrogram.render(image)



