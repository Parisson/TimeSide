#! /usr/bin/env python

from unit_timeside import *
from timeside.decoder import *
from timeside.analyzer.dc import MeanDCShift
from timeside.analyzer.core import AnalyzerResult, AnalyzerAttributes
from numpy import round

class TestAnalyzerDC(TestCase):

    def setUp(self):
        self.analyzer = MeanDCShift()

    def testOnSweep(self):
        "runs on sweep"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "sweep.wav")
        attributes=AnalyzerAttributes(name="Mean DC shift",
                                      unit="%",
                                      id="mean_dc_shift",
                                      samplerate=44100,
                                      blocksize=None,
                                      stepsize=None)

        self.expected = AnalyzerResult(data=-0.000, attributes=attributes)

    def testOnGuitar(self):
        "runs on guitar"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "guitar.wav")
        attributes=AnalyzerAttributes(name="Mean DC shift",
                                      unit="%",
                                      id="mean_dc_shift",
                                      samplerate=44100,
                                      blocksize=None,
                                      stepsize=None)
        self.expected = AnalyzerResult(data=0.054, attributes=attributes)

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        results = self.analyzer.results()
        self.assertEquals(results[0], self.expected)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
