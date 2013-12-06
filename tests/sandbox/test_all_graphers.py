# -*- coding: utf-8 -*-

import os, sys
import timeside

audio_file = sys.argv[-1]
audio_filename = audio_file.split(os.sep)[-1]
img_dir = '../results/img'

if not os.path.exists(img_dir):
    os.makedirs(img_dir)

decoder  = timeside.decoder.FileDecoder(audio_file)
graphers = timeside.core.processors(timeside.api.IGrapher)
pipe = decoder
proc_list = []

for grapher in graphers:
    proc = grapher()
    proc_list.append(proc)
    print proc.id()
    pipe = pipe | proc

pipe.run()

for grapher in proc_list:
    image = img_dir + os.sep + audio_filename + '-' + grapher.id() + '.png'
    grapher.render(image)
