#! /usr/bin/env python

from unit_timeside import *
import timeside
verbose = 0

class TestListCoreProcessors(TestCase):
    """ test get list of processors """

    def testHasSomeDecoders(self):
        "has some decoders"
        import timeside.encoder
        procs = timeside.core.processors(timeside.api.IEncoder)
        self.assertNotEquals(len(procs), 0)

    def testHasSomeEncoders(self):
        "has some encoders"
        import timeside.encoder
        procs = timeside.core.processors(timeside.api.IEncoder)
        self.assertNotEquals(len(procs), 0)

    def testHasSomeAnalyzers(self):
        "has some analyzers"
        import timeside.analyzer
        procs = timeside.core.processors(timeside.api.IAnalyzer)
        self.assertNotEquals(len(procs), 0)

    def testHasSomeGraphers(self):
        "has some graphers"
        import timeside.grapher
        procs = timeside.core.processors(timeside.api.IGrapher)
        self.assertNotEquals(len(procs), 0)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
