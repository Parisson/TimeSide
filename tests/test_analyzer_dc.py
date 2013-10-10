#! /usr/bin/env python

from unit_timeside import *
from timeside.decoder import FileDecoder
from timeside.analyzer.dc import MeanDCShift

class TestAnalyzerDC(TestCase):

    def setUp(self):
        self.analyzer = MeanDCShift()

    def testOnSweep(self):
        "runs on sweep"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "sweep.wav")

        self.expected = {'mean_dc_shift': -0.000}

    def testOnGuitar(self):
        "runs on guitar"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "guitar.wav")
        self.expected = {'mean_dc_shift': 0.054}

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        results = self.analyzer.results
        for key in self.expected.keys():
            self.assertEquals(results[key].data_object.value, self.expected[key])

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
