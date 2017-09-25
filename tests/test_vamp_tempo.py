#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
from timeside.plugins.decoder.file import FileDecoder
from timeside.core import get_processor

from timeside.core.tools.test_samples import samples


class TestVampTempo(unittest.TestCase):

    def setUp(self):
        self.analyzer = get_processor('vamp_tempo')()

    def testOnC4Scale(self):
        "runs on C4 scale"
        self.source = samples["C4_scale.wav"]

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        self.assertAlmostEqual(self.analyzer.results['vamp_tempo'].data_object.value, 101.3, places=1)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
