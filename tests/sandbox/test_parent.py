# -*- coding: utf-8 -*-

import timeside
import os.path

source = os.path.join(os.path.dirname(__file__), "../samples/sweep.wav")

d = timeside.decoder.FileDecoder(source)
a  = timeside.analyzer.OnsetDetectionFunction()

pipe = d | a
pipe.run()

print pipe.results

a.results.to_hdf5('../results/sweep_odf.hdf5')
