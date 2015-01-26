#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
from timeside.plugins.decoder.file import FileDecoder
from timeside.core.tools.test_samples import samples

from timeside.core import _WITH_YAAFE
if _WITH_YAAFE:
    from timeside.plugins.analyzer.externals.yaafe import Yaafe
import os


@unittest.skipIf(not _WITH_YAAFE, 'Yaafe library is not available')
class TestYaafe(unittest.TestCase):

    def setUp(self):
        self.samplerate = 16000

    def testOnSweepWithFeaturePlan(self):
        "runs on sweep"
        self.source = samples["sweep.wav"]

        # Setup Yaafe Analyzer
        # Define Yaafe Feature Plan
        fp = ['mfcc: MFCC blockSize=512 stepSize=256',
              'mfcc_d1: MFCC blockSize=512 stepSize=256 > Derivate DOrder=1',
              'mfcc_d2: MFCC blockSize=512 stepSize=256 > Derivate DOrder=2']

        # Setup a new Yaafe TimeSide analyzer
        # from FeaturePlan
        self.analyzer = Yaafe(feature_plan=fp,
                              input_samplerate=self.samplerate)

        # Expected Results
        self.result_length = 3

    def tearDown(self):
        decoder = FileDecoder(self.source)
        decoder.output_samplerate = self.samplerate
        (decoder | self.analyzer).run()
        results = self.analyzer.results
        self.assertEquals(self.result_length, len(results))
        # print results
        # print results.to_yaml()
        # print results.to_json()
        # print results.to_xml()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
