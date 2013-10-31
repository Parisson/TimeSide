# -*- coding: utf-8 -*-

import timeside.decoder
import timeside.analyzer


decoder  =  timeside.decoder.FileDecoder('/home/momo/dev/timeside/timeside/tests/samples/sweep.wav')
analyzer = timeside.analyzer.AubioMelEnergy()
(decoder | analyzer).run()

print len(analyzer.results())
print len(analyzer.results())
print len(analyzer.results())



