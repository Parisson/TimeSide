#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
import os
from timeside.plugins.decoder.file import FileDecoder
from timeside.core import get_processor
from timeside.core.processor import Processor
from timeside.core.api import IProcessor
from timeside.core.component import implements, interfacedoc

from timeside.core.tools.test_samples import samples

SAMPLE_RATE_FORCED = 16000
OTHER_SAMPLE_RATE = 32000


class TestForceSampleRate(unittest.TestCase):

    class Dummy_Processor(Processor):
        implements(IProcessor)

        @staticmethod
        @interfacedoc
        def id():
            return 'dummy_proc'

    class Dummy_Processor_withSampleRate(Dummy_Processor):
        implements(IProcessor)

        @staticmethod
        @interfacedoc
        def id():
            return 'dummy_proc_samplerate'

        @property
        def force_samplerate(self):
            return SAMPLE_RATE_FORCED

    class Dummy_Processor_withSampleRate2(Dummy_Processor):
        implements(IProcessor)

        @staticmethod
        @interfacedoc
        def id():
            return 'dummy_proc_samplerate_2'

        @property
        def force_samplerate(self):
            return OTHER_SAMPLE_RATE

    def setUp(self):
        self.source = samples['sweep.wav']
        self.source_samplerate = 44100
        self.decoder = FileDecoder(uri=self.source)

    def testWithoutForceSampleRate(self):
        "Processor not overwritting source SampleRate"
        processor = self.Dummy_Processor()
        pipe = (self.decoder | processor)
        pipe.run()

    def testWithForceSampleRate(self):
        "Processor overwritting source SampleRate"
        processor = self.Dummy_Processor_withSampleRate()
        pipe = (self.decoder | processor)
        pipe.run()
        self.assertEqual(self.decoder.samplerate(), SAMPLE_RATE_FORCED)

    def testWithForceSampleRatePipe(self):
        "Processor overwritting pipe SampleRate"
        processor = self.Dummy_Processor_withSampleRate()
        pipe = (self.decoder | processor)
        self.assertRaises(ValueError, pipe.run, [],
                          {'samplerate': OTHER_SAMPLE_RATE})

    def testWithForceSampleRateTwoProc(self):
        "Two Processors overwritting source SampleRate"
        processor1 = self.Dummy_Processor_withSampleRate()
        processor2 = self.Dummy_Processor_withSampleRate2()

        pipe = (self.decoder | processor1 | processor2)
        self.assertRaises(ValueError, pipe.run)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
