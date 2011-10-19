# -*- coding: utf-8 -*-

import timeside
import sys
import os.path
import numpy
import time


class TestAnalyzer:

    analyzer = timeside.analyzer.MaxLevel()

    def __init__(self, path):
        self.source = os.path.join(os.path.dirname(__file__), path)
        print "Processing %s" % self.source
        self.decoder  = timeside.decoder.FileDecoder(self.source)
        print 'format: ', self.decoder.format()
        self.pipe = self.decoder
        self.sub_pipe = self.analyzer

    def process(self):
        self.pipe = self.pipe | self.sub_pipe
        self.pipe.run()

    def results(self):
        print {'name':self.analyzer.name(),
                            'id':self.analyzer.id(),
                            'unit':self.analyzer.unit(),
                            'value':str(self.analyzer.value)}

test = TestAnalyzer(sys.argv[-1])
test.process()
test.results()
