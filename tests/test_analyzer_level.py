#! /usr/bin/env python

from unit_timeside import *
from timeside.decoder import *
from timeside.analyzer.level import Level
from timeside.analyzer import AnalyzerResult, AnalyzerResultContainer
from timeside.analyzer import AnalyzerAttributes

class TestAnalyzerLevel(TestCase):

    def setUp(self):
        self.analyzer = Level()

    def testOnSweep(self):
        "runs on sweep"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "sweep.wav")

        # Max level
        attr = AnalyzerAttributes(id="max_level",
                                  name="Max level",
                                  unit = "dBFS",
                                  samplerate=44100)
        max_level = AnalyzerResult(-6.021, attr)

        # RMS level
        attr = AnalyzerAttributes(id="rms_level",
                                  name="RMS level",
                                  unit="dBFS",
                                  samplerate=44100)
        rms_level = AnalyzerResult(-9.856, attr)
        self.expected = AnalyzerResultContainer([max_level,rms_level])

    def testOnGuitar(self):
        "runs on guitar"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "guitar.wav")

        # Max level
        attr = AnalyzerAttributes(id="max_level",
                                  name="Max level",
                                  unit = "dBFS",
                                  samplerate=44100)
        max_level = AnalyzerResult(-4.258, attr)

        # RMS level
        attr = AnalyzerAttributes(id="rms_level",
                                  name="RMS level",
                                  unit="dBFS",
                                  samplerate=44100)
        rms_level = AnalyzerResult(-21.945, attr)
        self.expected = AnalyzerResultContainer([max_level,rms_level])

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
