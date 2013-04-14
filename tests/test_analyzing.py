from timeside.decoder import *
from timeside.analyzer import *
from unit_timeside import *

import os.path

__all__ = ['TestAnalyzing']

class TestAnalyzing(TestCase):
    "Test all analyzers"

    def setUp(self):
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")

    def testDC(self):
        "Test mean DC shift"
        self.analyzer = MeanDCShift()
        self.value = -0

    def testMeanLevel(self):
        "Test mean level"
        self.analyzer = MeanLevel()
        self.value = -9.856

    def testMaxLevel(self):
        "Test max level"
        self.analyzer = MaxLevel()
        self.value = -6.0209999999999999

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        self.assertEquals(self.analyzer.result(), self.value)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())

