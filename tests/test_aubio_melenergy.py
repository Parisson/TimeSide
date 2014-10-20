#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
from timeside.decoder.file import FileDecoder
from timeside.core import get_processor
from timeside import _WITH_AUBIO
from timeside.tools.data_samples import samples as ts_samples


@unittest.skipIf(not _WITH_AUBIO, 'Aubio library is not available')
class TestAubioMelEnergy(unittest.TestCase):

    def setUp(self):
        self.analyzer = get_processor('aubio_melenergy')()

    def testOnSweep(self):
        "runs on sweep"
        self.source = ts_samples["sweep.wav"]

    def testOnGuitar(self):
        "runs on C4_scale"
        self.source = ts_samples["C4_scale.wav"]

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
