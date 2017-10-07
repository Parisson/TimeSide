#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
from timeside.plugins.decoder.file import FileDecoder
from timeside.core import get_processor

from timeside.core.tools.test_samples import samples


class TestLoudnessITU(unittest.TestCase):

    def setUp(self):
        self.analyzer = get_processor('loudness_itu')()

    def testOnC4Scale(self):
        "runs on C4 scale"
        self.source = samples["C4_scale.wav"]

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        self.assertEqual(self.analyzer.results['loudness_itu.block_loudness'].data_object.value.shape[0], 91)
        self.assertAlmostEqual(self.analyzer.results['loudness_itu.block_loudness'].data_object.value.mean(), -64.06, places=1)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
