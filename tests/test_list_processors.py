#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
import timeside
import os
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

    def testListProcessorsCSV(self):
        "list processors in .csv file"
        fpath = timeside.core.processor.list_processors_csv()
        path = os.getcwd() + '/list_processors.csv'
        self.assertEqual(fpath, path)
        self.assertTrue(os.path.isfile(fpath))
        
    def tearDown(self):
        path = os.getcwd() + '/list_processors.csv'
        if os.path.isfile(path):
            os.remove(path)



if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
