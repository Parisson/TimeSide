# -*- coding: utf-8 -*-

import timeside
import sys

analyzers = [timeside.analyzer.Level(),
                 timeside.analyzer.AubioTemporal(),]

source = sys.argv[-1]
print "Processing %s" % source
pipe  = timeside.decoder.FileDecoder(source, stack=True)
print 'format: ', pipe.format()
for analyzer in analyzers:
    pipe |= analyzer

pipe.run()
print pipe.results

