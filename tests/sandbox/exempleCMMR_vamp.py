# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 13:22:37 2013

@author: thomas
"""

from __future__ import division
import timeside
import matplotlib.pyplot as plt
import numpy as np
import sys

#wav_file = sys.argv[-1]
wav_file =  '/home/thomas/code/timeside/TimeSide/tests/samples/sweep.wav'

# normal
d = timeside.decoder.FileDecoder(wav_file)

specgram = timeside.analyzer.Spectrogram()
waveform = timeside.analyzer.Waveform()

# Get available Vamp plugins list
from timeside.analyzer.vamp_plugin import VampSimpleHost
plugins_list = VampSimpleHost.get_plugins_list()

# Display avalaible plugins
print 'index \t soname \t \t identifier \t output '
print '------ \t \t ---------- \t ------ '
for index, line in zip(xrange(len(plugins_list)),plugins_list):
    print '%d : %s \t %s \t %s' % (index,line[0],line[1],line[2])

# Let's choose #7
my_plugin = plugins_list[7]
print my_plugin

#
# Vamp plugin Analyzer
#vamp = timeside.analyzer.VampSimpleHost([my_plugin])
vamp = timeside.analyzer.VampSimpleHost()

#
myPipe = (d | vamp | specgram | waveform).run()

# Get spectrogram result and plot the spectrogram
spec_res = specgram.results['spectrogram_analyzer']
N = spec_res.parameters['FFT_SIZE']
max_freq = (N // 2 + 1) / N * spec_res.frame_metadata.samplerate



# Get the vamp plugin result and plot it
for key in vamp.results.keys():
    print vamp.results[key].data

res_vamp = vamp.results['vamp_simple_host.percussiononsets.detectionfunction']

plt.figure(1)

plt.subplot(2,1,1)
plt.plot(res_vamp.time, res_vamp.data)
plt.xlabel('time in s')
plt.grid
plt.title(res_vamp.name)

plt.subplot(2,1,2)
plt.imshow(20 * np.log10(spec_res.data.T + 1e-6),
           origin='lower',
           extent=[spec_res.time[0], spec_res.time[-1], 0,
                   max_freq],
           aspect='auto')

data = (res_vamp.data - res_vamp.data.mean()).clip(0)
plt.plot(res_vamp.time, abs(data / data.max() * max_freq))


plt.xlabel('time in s')
plt.show()