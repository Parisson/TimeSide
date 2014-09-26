#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
import os
from timeside.decoder.file import FileDecoder
from timeside.core import get_processor
from timeside import _WITH_AUBIO


@unittest.skipIf(not _WITH_AUBIO, 'Aubio library is not available')
class TestAubioSpecdesc(unittest.TestCase):

    def setUp(self):
        self.analyzer = get_processor('aubio_specdesc')()

    def testOnSweep(self):
        "runs on sweep"
        self.source = os.path.join(os.path.dirname(__file__),
                                   "samples", "sweep.wav")

    def testOnGuitar(self):
        "runs on guitar"
        self.source = os.path.join(os.path.dirname(__file__),
                                   "samples", "guitar.wav")

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        results = self.analyzer.results
        #results.to_yaml()
        #results.to_json()
        #results.to_xml()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
