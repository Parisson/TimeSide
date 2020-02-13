#! /usr/bin/env python

import unittest
from unit_timeside import TestRunner
from timeside.core.tools.test_samples import samples
from timeside.core import get_processor


FileDecoder = get_processor('file_decoder')
try:
    VampSimpleHost = get_processor('vamp_simple_host')
except:
    VampSimpleHost = None

@unittest.skipIf(not VampSimpleHost, 'vamp-simple-host library is not available')
class TestVampsimpleHost(unittest.TestCase):

    def setUp(self):
        self.analyzer = VampSimpleHost()

    def testOnC4_scale(self):
        "runs on C4_scale"
        self.source = samples["C4_scale.wav"]

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        results = self.analyzer.results
        print(results.keys())
        #print(results)
        #print(results.to_yaml())
        #print(results.to_json())
        #print(results.to_xml())

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
