# -*- coding: utf-8 -*-

import os
import timeside

audio_dir = '/home/momo/music_local/test/aboul/wav/'
audio_file = 'aboul.wav'
audio_path = audio_dir + audio_file
img_dir = '../results/img'

if not os.path.exists(img_dir):
    os.makedirs(img_dir)

decoder  = timeside.decoder.FileDecoder(audio_path)
analyzers = timeside.core.processors(timeside.api.IAnalyzer)
pipe = decoder

for analyzer in analyzers:
    subpipe = analyzer()
    analyzers_sub.append(subpipe)
    pipe = pipe | subpipe

image = img_dir + os.sep + source + '.png'
print 'Test : decoder(%s) | waveform (%s)' % (source, image)

spectrogram = SpectrogramLinear(width=10240, height=512, bg_color=(0,0,0), color_scheme='default')
(decoder | spectrogram).run()
print 'frames per pixel = ', spectrogram.samples_per_pixel
print "render spectrogram to: %s" %  image
spectrogram.render(image)

