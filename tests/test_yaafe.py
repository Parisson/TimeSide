#! /usr/bin/env python

from unit_timeside import *
from timeside.decoder import *
from timeside.analyzer import Yaafe
from yaafelib import DataFlow,FeaturePlan

class TestYaafe(TestCase):

    def setUp(self):
        self.sample_rate = 16000

    def testOnSweepWithFeaturePlan(self):
        "runs on sweep and define feature plan manually"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "sweep.wav")

        # Setup Yaafe Analyzer
        # Define Yaafe Feature Plan
        fp = FeaturePlan(sample_rate=self.sample_rate)
        # add feature definitions manually
        fp.addFeature('mfcc: MFCC blockSize=512 stepSize=256')
        fp.addFeature('mfcc_d1: MFCC blockSize=512 stepSize=256 > Derivate DOrder=1')
        fp.addFeature('mfcc_d2: MFCC blockSize=512 stepSize=256 > Derivate DOrder=2')

        # Setup a new Yaafe TimeSide analyzer
        # from FeaturePlan
        self.analyzer = Yaafe(fp)

        # Expected Results
        self.result_length = 3

    def testOnGuitarWithFeaturePlanFromFile(self):
        "runs on guitar and load Yaafe feature plan from file"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "guitar.wav")
        # Setup Yaafe Analyzer
        # Load Yaafe Feature Plan
        fp = FeaturePlan(sample_rate=self.sample_rate)
        fp_file = os.path.join (os.path.dirname(__file__),  "yaafe_config", "yaafeFeaturePlan")

        fp.loadFeaturePlan(fp_file)
        # Setup a new Yaafe TimeSide analyzer
        # from FeaturePlan
        self.analyzer = Yaafe(fp)

        # Expected Results
        self.result_length = 3

    def testOnGuitarWithDataFlow(self):
        "runs on guitar and load Yaafe dataflow from file"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "guitar.wav")
        # Setup Yaafe Analyzer
        # Load DataFlow from file
        df = DataFlow()
        df_file = os.path.join (os.path.dirname(__file__),  "yaafe_config", "yaafeDataFlow")
        df.load(df_file)

        # Setup a new Yaafe TimeSide analyzer
        # from DataFlow
        self.analyzer = Yaafe(df)

        # Expected Results
        self.result_length = 5

    def tearDown(self):
        decoder = FileDecoder(self.source)
        decoder.output_samplerate = self.sample_rate
        (decoder | self.analyzer).run()
        results = self.analyzer.results
        self.assertEquals(self.result_length, len(results))
        #print results
        #print results.to_yaml()
        #print results.to_json()
        #print results.to_xml()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
