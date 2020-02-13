#! /usr/bin/env python

import unittest
from unit_timeside import TestRunner
from timeside.core.tools.test_samples import samples
from timeside.core import get_processor

FileDecoder = get_processor('file_decoder')
try:
    AubioPitch = get_processor('aubio_pitch')
except:
    AubioPitch = None

@unittest.skipIf(not AubioPitch, 'Aubio library is not available')
class TestAubioPitch(unittest.TestCase):

    def setUp(self):
        self.analyzer = AubioPitch()

    def testOnSweep(self):
        "runs on sweep"
        self.source = samples["sweep.wav"]

    def testOnC4Scale(self):
        "runs on C4 scale"
        self.source = samples["C4_scale.wav"]

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        results = self.analyzer.results
        #print ("result:", results)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
