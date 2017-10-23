#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
from timeside.plugins.decoder.file import FileDecoder
from timeside.core import get_processor

from timeside.core.tools.test_samples import samples


class TestEssentiaDissonance(unittest.TestCase):

    def setUp(self):
        self.analyzer_dissonance = get_processor('essentia_dissonance')()
        self.analyzer_dissonance_value = get_processor('essentia_dissonance_value')()

    def testOnC4Scale(self):
        "runs on C4 scale"
        self.source = samples["C4_scale.wav"]

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer_dissonance | self.analyzer_dissonance_value).run()
        self.assertAlmostEqual(self.analyzer_dissonance.results['essentia_dissonance'].data_object.value.mean(), 0.003, places=3)
        self.assertAlmostEqual(self.analyzer_dissonance_value.results['essentia_dissonance_value'].data_object.value, 0.109, places=2)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
