#! /usr/bin/env python

import unittest
from unit_timeside import TestRunner
from timeside.core import get_processor
from timeside.core.tools.test_samples import samples

FileDecoder = get_processor('file_decoder')
try:
    AubioMelEnergy = get_processor('aubio_melenergy')
except:
    AubioMelEnergy = None


@unittest.skipIf(not AubioMelEnergy, 'Aubio library is not available')
class TestAubioMelEnergy(unittest.TestCase):

    def setUp(self):
        self.analyzer = AubioMelEnergy()

    def testOnSweep(self):
        "runs on sweep"
        self.source = samples["sweep.wav"]

    def testOnGuitar(self):
        "runs on C4_scale"
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
