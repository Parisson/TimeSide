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

        max_level_value = -6.021
        rms_level_value = -9.856

        self.expected = {'level.max':max_level_value , 'level.rms':rms_level_value }

    def testOnGuitar(self):
        "runs on guitar"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "guitar.wav")

        max_level_value = -4.258
        rms_level_value = -21.945

        self.expected = {'level.max':max_level_value , 'level.rms':rms_level_value }


    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        results = self.analyzer.results
        for key in self.expected.keys():
            self.assertEquals(results[key].data_object.value, self.expected[key])
        #print results
        #print results.to_yaml()
        #print results.to_json()
        #print results.to_xml()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
