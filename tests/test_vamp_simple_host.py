#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
from timeside.plugins.decoder.file import FileDecoder
from timeside.core import get_processor
from timeside.core import _WITH_VAMP
from timeside.core.tools.test_samples import samples


@unittest.skipIf(not _WITH_VAMP, 'vamp-simple-host library is not available')
class TestVampsimpleHost(unittest.TestCase):

    def setUp(self):
        self.analyzer = get_processor('vamp_simple_host')()

    def testOnC4_scale(self):
        "runs on C4_scale"
        self.source = samples["C4_scale.wav"]

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        results = self.analyzer.results
        print results.keys()
        #print results
        #print results.to_yaml()
        #print results.to_json()
        #print results.to_xml()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
