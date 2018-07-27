#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
from timeside.plugins.decoder.file import FileDecoder
from timeside.core import get_processor

from timeside.core.tools.test_samples import samples
import numpy as np

class TestFxGain(unittest.TestCase):

    def setUp(self):
        self.gain = 2
        self.fx = get_processor('fx_gain')(gain=self.gain)
        self.level = get_processor('level')()
 
 
    def testOnC4Scale(self):
        "runs on C4 scale"
        self.source = samples["C4_scale.wav"]
        gain_db = np.round(20*np.log10(self.gain), 3)
        max_level_value = 0 + gain_db
        rms_level_value = -3.705 + gain_db

        self.expected = {'level.max': max_level_value,
                         'level.rms': rms_level_value}

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.fx | self.level).run()
        results = self.level.results
        for result_id in self.expected.keys():
            result = results[result_id]
            self.assertAlmostEquals(result.data_object.value,
                                    self.expected[result_id],
                                    places=2)
 


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
