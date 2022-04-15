#! /usr/bin/env python

import unittest
from unit_timeside import TestRunner
from timeside.plugins.decoder.aubio import AubioDecoder as FileDecoder
from timeside.core import get_processor
from timeside.core.tools.test_samples import samples


class TestVampSpectralCentroid(unittest.TestCase):

    proc_id = 'vamp_spectral_centroid'

    def setUp(self):
        self.analyzer = get_processor(self.proc_id)()

    def testOnC4Scale(self):
        "runs on C4 scale"
        self.source = samples["C4_scale.wav"]

    def testOnSweep(self):
        "runs on sweep"
        self.source = samples["sweep.wav"]

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        results = self.analyzer.results

        result = results.get_result_by_id(self.proc_id)
        duration = result.audio_metadata.duration
        data_duration = result.data_object.time[-1]

        self.assertAlmostEqual (duration, data_duration, 1)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
