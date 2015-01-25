#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
from timeside.plugins.decoder.file import FileDecoder
from timeside.plugins.analyzer.level import Level
from timeside.core.tools.test_samples import samples


class TestAnalyzerLevel(unittest.TestCase):

    def setUp(self):
        self.analyzer = Level()

    def testOnSweep(self):
        "runs on sweep"
        self.source = samples["sweep.wav"]

        max_level_value = 0
        rms_level_value = -2.995

        self.expected = {'level.max': max_level_value,
                         'level.rms': rms_level_value}

    def testOnC4_Scale(self):
        "runs on C4 scale"
        self.source = samples["C4_scale.wav"]

        max_level_value = 0
        rms_level_value = -3.705

        self.expected = {'level.max': max_level_value,
                         'level.rms': rms_level_value}

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        results = self.analyzer.results
        for result_id in self.expected.keys():
            result = results[result_id]
            self.assertEquals(result.data_object.value,
                              self.expected[result_id])
        #print results
        #print results.to_yaml()
        #print results.to_json()
        #print results.to_xml()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
