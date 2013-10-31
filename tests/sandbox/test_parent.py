# -*- coding: utf-8 -*-

import timeside
import os.path

source = os.path.join(os.path.dirname(__file__), "../samples/sweep.wav")

d = timeside.decoder.FileDecoder(source)
a  = timeside.analyzer.OnsetDetectionFunction()

(d | a).run()

print a.results