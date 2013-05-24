#! /usr/bin/env python

from unit_timeside import *
from timeside.decoder import *
from timeside.analyzer.dc import MeanDCShift
from timeside.analyzer.core import AnalyzerResultContainer

class TestAnalyzerDC(TestCase):

    def setUp(self):
        self.analyzer = MeanDCShift()

    def testOnSweep(self):
        "runs on sweep"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "sweep.wav")
        self.expected = [{"value": -0.0, "name": "Mean DC shift", "unit": "%", "id": "mean_dc_shift"}]

    def testOnGuitar(self):
        "runs on guitar"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "guitar.wav")
        self.expected = [{"value": 0.054, "name": "Mean DC shift", "unit": "%", "id": "mean_dc_shift"}]

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        results = self.analyzer.results()
        self.assertEquals(results, AnalyzerResultContainer(self.expected))

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
