# -*- coding: utf-8 -*-

import timeside
import os.path

source = os.path.join(os.path.dirname(__file__),  "../samples/sweep.wav")
dest = os.path.join(os.path.dirname(__file__), "../results/sweep_wav_48000.wav")

decoder  = timeside.decoder.FileDecoder(source)
decoder.output_samplerate = 48000
encoder  = timeside.encoder.WavEncoder(dest)
(decoder | encoder).run()
