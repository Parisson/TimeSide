#! /usr/bin/env python

import unittest
from unit_timeside import TestRunner
from timeside.plugins.decoder.file import FileDecoder
from timeside.core import get_processor

from timeside.core.tools.test_samples import samples


class TestVampTuning(unittest.TestCase):

    def setUp(self):
        self.analyzer = get_processor('vamp_tuning')()

    def testOnC4Scale(self):
        "runs on C4 scale"
        self.source = samples["C4_scale.wav"]

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        self.assertAlmostEqual( self.analyzer.results['vamp_tuning'].data_object.value.mean(), 440.0, places=1)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
