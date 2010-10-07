# -*- coding: utf-8 -*-

import timeside
from sys import stdout
import os.path
import numpy


class TestAnalyzer:

    graphers = timeside.core.processors(timeside.api.IGrapher)
    decoders = timeside.core.processors(timeside.api.IDecoder)
    encoders= timeside.core.processors(timeside.api.IEncoder)
    analyzers = timeside.core.processors(timeside.api.IAnalyzer)

    def __init__(self, path):
        self.source = os.path.join(os.path.dirname(__file__), path)
        print "Processing %s" % self.source
        self.decoder  = timeside.decoder.FileDecoder(self.source)
        print 'format: ', self.decoder.format()
        self.pipe = self.decoder
        self.analyzers_sub_pipe = []

    def process(self):
        for analyzer in self.analyzers:
            sub_pipe = analyzer()
            self.analyzers_sub_pipe.append(sub_pipe)
            self.pipe = self.pipe | sub_pipe
        self.pipe.run()

    def results(self):
        analyzers = []
        for analyzer in self.analyzers_sub_pipe:
            value = analyzer.result()
            analyzers.append({'name':analyzer.name(),
                            'id':analyzer.id(),
                            'unit':analyzer.unit(),
                            'value':str(value)})
        print analyzers


test = TestAnalyzer('../samples/guitar.wav')
#test = TestAnalyzer('/home/momo/music/wav/Cellar/Cellar-FinallyMix_01.wav')
test.process()
test.results()

