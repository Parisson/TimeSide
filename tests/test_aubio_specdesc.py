#! /usr/bin/env python

import unittest
from unit_timeside import TestRunner
from timeside.core.tools.test_samples import samples
from timeside.core import get_processor


FileDecoder = get_processor('file_decoder')
try:
    AubioSpecdesc = get_processor('aubio_specdesc')
except:
    AubioSpecdesc = None


@unittest.skipIf(not AubioSpecdesc, 'Aubio library is not available')
class TestAubioSpecdesc(unittest.TestCase):

    def setUp(self):
        self.analyzer = AubioSpecdesc()

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
        #results.to_yaml()
        #results.to_json()
        #results.to_xml()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
