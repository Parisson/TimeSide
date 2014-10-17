#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
from timeside.decoder.file import FileDecoder
from timeside.core import get_processor
from timeside import _WITH_AUBIO
from timeside.tools.data_samples import samples as ts_samples


@unittest.skipIf(not _WITH_AUBIO, 'Aubio library is not available')
class TestAubioMfcc(unittest.TestCase):

    def setUp(self):
        self.analyzer = get_processor('aubio_mfcc')()

    def testOnSweep(self):
        "runs on sweep"
        self.source = ts_samples["sweep.wav"]

    def testOnScale(self):
        "runs on C4 scale"
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
