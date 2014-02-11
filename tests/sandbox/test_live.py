# -*- coding: utf-8 -*-

import timeside
import matplotlib.pyplot as plt
import numpy as np


d = timeside.decoder.LiveDecoder(num_buffers=256)
w = timeside.analyzer.Waveform()
s = timeside.analyzer.Spectrogram()
m = timeside.encoder.Mp3Encoder('/tmp/test_live.mp3', overwrite=True)
v = timeside.encoder.VorbisEncoder('/tmp/test_live.ogg', overwrite=True)

(d | w | s | m | v).run()

plt.figure(1)
plt.plot(w.results['waveform_analyzer'].time, w.results['waveform_analyzer'].data)

plt.figure(2)
sr = s.results['spectrogram_analyzer']
N = sr.parameters['FFT_SIZE']
plt.imshow(20 * np.log10(sr.data.T),
           origin='lower',
           extent=[sr.time[0], sr.time[-1], 0,
                   (N // 2 + 1) / N * sr.frame_metadata.samplerate],
           aspect='auto')

plt.show()
