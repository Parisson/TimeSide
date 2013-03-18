#! /usr/bin/env python

from unittest import TestCase
from timeside.decoder import *
from timeside.analyzer.aubio_pitch import AubioPitch

class TestAubioPitch(TestCase):

    def setUp(self):
        self.analyzer = AubioPitch()

    def testOnSweep(self):
        "runs on sweep"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "sweep.wav")

    def testOnGuitar(self):
        "runs on guitar"
        self.source = os.path.join (os.path.dirname(__file__),  "samples", "guitar.wav")

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.analyzer).run()
        #print "result:", self.analyzer.result()

if __name__ == '__main__':
    from unittest import main
    main()
