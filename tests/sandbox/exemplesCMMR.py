# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 13:04:49 2013

@author: thomas
"""
from __future__ import division
import timeside
import matplotlib.pyplot as plt
import numpy as np
import sys

if not '.wav' in sys.argv[-1]:
    wav_file = 'toto.wav'
else:
    wav_file = sys.argv[-1]

# normal
decoder = timeside.decoder.FileDecoder(wav_file, start=10, duration=15)
#e = timeside.encoder.VorbisEncoder('output.ogg', overwrite = True)
aubio_pitch = timeside.analyzer.AubioPitch()
aubio_temporal = timeside.analyzer.AubioTemporal()
specgram = timeside.analyzer.Spectrogram()
waveform = timeside.analyzer.Waveform()
#g  =  timeside.grapher.Spectrogram()

pipe = (decoder | aubio_pitch | aubio_temporal | specgram | waveform).run()

pipe.results.keys()

# Display Spectrogram + Aubio Pitch + Aubio Beat
plt.figure(1)

spec_res = specgram.results['spectrogram_analyzer']
N = spec_res.parameters['FFT_SIZE']
plt.imshow(20 * np.log10(spec_res.data.T),
           origin='lower',
           extent=[spec_res.time[0], spec_res.time[-1], 0,
                   (N // 2 + 1) / N * spec_res.frame_metadata.samplerate],
           aspect='auto')

res_pitch = aubio_pitch.results['aubio_pitch']
plt.plot(res_pitch.time, res_pitch.data)


res_beats = aubio_temporal.results['aubio_temporal.beat']

for time in res_beats.time:
    plt.axvline(time, color='r')

plt.title('Spectrogram + Aubio pitch + Aubio beat')
plt.grid()

# Display waveform + Onsets
plt.figure(2)
res_wave = waveform.results['waveform_analyzer']
plt.plot(res_wave.time, res_wave.data)
res_onsets = aubio_temporal.results['aubio_temporal.onset']
for time in res_onsets.time:
    plt.axvline(time, color='g')
plt.grid()
plt.title('Waveform + Aubio onset')
plt.show()
