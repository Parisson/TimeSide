#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
import timeside
verbose = 0

class TestListCoreProcessors(unittest.TestCase):
    """ test get list of processors """

    def testHasSomeDecoders(self):
        "has some decoders"
        procs = timeside.core.processor.processors(timeside.core.api.IDecoder)
        self.assertNotEquals(len(procs), 0)

    def testHasSomeEncoders(self):
        "has some encoders"
        procs = timeside.core.processor.processors(timeside.core.api.IEncoder)
        self.assertNotEquals(len(procs), 0)

    def testHasSomeAnalyzers(self):
        "has some analyzers"
        procs = timeside.core.processor.processors(timeside.core.api.IAnalyzer)
        self.assertNotEquals(len(procs), 0)

    def testHasSomeGraphers(self):
        "has some graphers"
        procs = timeside.core.processor.processors(timeside.core.api.IGrapher)
        self.assertNotEquals(len(procs), 0)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
