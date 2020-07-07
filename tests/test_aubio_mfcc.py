#! /usr/bin/env python

import unittest
from unit_timeside import TestRunner
from timeside.core.tools.test_samples import samples
from timeside.core import get_processor

FileDecoder = get_processor('file_decoder')
try:
    AubioMfcc = get_processor('aubio_mfcc')
except:
    AubioMfcc = None

@unittest.skipIf(not AubioMfcc, 'Aubio library is not available')
class TestAubioMfcc(unittest.TestCase):

    def setUp(self):
        self.analyzer = AubioMfcc()

    def testOnSweep(self):
        "runs on sweep"
        self.source = samples["sweep.wav"]

    def testOnScale(self):
        "runs on C4 scale"
        self.source = samples["C4_scale.wav"]

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        results = self.analyzer.results
        #print results
        #print results.to_yaml()
        #print results.to_json()
        #print results.to_xml()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
