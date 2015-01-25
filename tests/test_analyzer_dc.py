#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
from timeside.plugins.decoder.file import FileDecoder
from timeside.plugins.analyzer.dc import MeanDCShift
from timeside.core.tools.test_samples import samples


class TestAnalyzerDC(unittest.TestCase):

    def setUp(self):
        self.analyzer = MeanDCShift()

    def testOnSweep(self):
        "runs on sweep"
        self.source = samples["sweep.wav"]

        self.expected = {'mean_dc_shift': 0.004}

    def testOnScale(self):
        "runs on C4 Scale"
        self.source = samples["C4_scale.wav"]
        self.expected = {'mean_dc_shift': 0.034}

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        results = self.analyzer.results
        for result_id in self.expected.keys():
            result = results[result_id]
            self.assertEquals(result.data_object.value,
                              self.expected[result_id])

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
