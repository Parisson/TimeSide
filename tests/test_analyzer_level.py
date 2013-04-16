#! /usr/bin/env python

from unit_timeside import *
from timeside.decoder import *
from timeside.analyzer.level import Level

class TestAnalyzerLevel(TestCase):

    def setUp(self):
        self.analyzer = Level()

    def testOnSweep(self):
        "runs on sweep"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "sweep.wav")
        self.expected = [{"value": -6.021, "name": "Max level", "unit": "dBFS", "id": "max_level"},
                {"value": -9.856, "name": "RMS level", "unit": "dBFS", "id": "rms_level"}]

    def testOnGuitar(self):
        "runs on guitar"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "guitar.wav")
        self.expected = [{"value": -4.258, "name": "Max level", "unit": "dBFS", "id": "max_level"},
                {"value": -21.945, "name": "RMS level", "unit": "dBFS", "id": "rms_level"}]

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        results = self.analyzer.results()
        self.assertEquals(results, self.expected)
        #print results
        #print results.to_yaml()
        #print results.to_json()
        #print results.to_xml()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
