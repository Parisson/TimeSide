# -*- coding: utf-8 -*-

import timeside
import sys
import os.path
import numpy
import time


class TestAnalyzer:

    analyzer = timeside.analyzer.Level()

    def __init__(self, path):
        self.source = path
        print "Processing %s" % self.source
        self.decoder  = timeside.decoder.FileDecoder(self.source)
        print 'format: ', self.decoder.format()
        self.pipe = self.decoder
        self.sub_pipe = self.analyzer

    def process(self):
        self.pipe = self.pipe | self.sub_pipe
        self.pipe.run()

    def results(self):
        print self.sub_pipe.results()

test = TestAnalyzer(sys.argv[-1])
test.process()
test.results()
