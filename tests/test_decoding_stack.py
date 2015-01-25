#! /usr/bin/env python

from __future__ import division

from timeside.plugins.decoder.file import FileDecoder
from timeside.plugins.analyzer.level import Level
from timeside.core.processor import ProcessPipe
from unit_timeside import unittest, TestRunner
from timeside.core.tools.test_samples import samples

#from glib import GError as GST_IOError
# HINT : to use later with Gnonlin only


class TestDecodingFromStack(unittest.TestCase):
    "Test decoder stack"

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = None, None, None
        self.start = 0
        self.duration = None

        self.expected_samplerate = 44100
        self.expected_channels = 2
        self.expected_totalframes = 352800
        self.test_exact_duration = True
        self.source_duration = 8
        self.expected_mime_type = 'audio/x-wav'
        self.source = samples["sweep.wav"]

    def testProcess(self):
        "Test decoder stack: test process"
        decoder = FileDecoder(uri=self.source,
                              start=self.start,
                              duration=self.duration,
                              stack=True)
        self.assertTrue(decoder.stack)
        self.assertFalse(decoder.from_stack)

        pipe = ProcessPipe(decoder)

        pipe.run()

        self.assertFalse(decoder.stack)
        self.assertTrue(decoder.from_stack)

        self.assertEqual(len(pipe.frames_stack), 44)

        pipe.run()

    def testResults(self):
        "Test decoder stack: test frames content"

        decoder = FileDecoder(uri=self.source,
                              start=self.start,
                              duration=self.duration,
                              stack=True)
        level = Level()
        pipe = (decoder | level)

        pipe.run()

        self.assertIsInstance(pipe.frames_stack, list)

        results_on_file = level.results['level.rms'].data.copy()

        # If the pipe is used for a second run, the processed frames stored
        # in the stack are passed to the other processors
        # without decoding the audio source again.

        pipe.results = {}  # to be sure the previous results are deleted
        pipe.run()

        # to assert that the frames passed to the two analyzers are the same,
        # we check that the results of these analyzers are equivalent:
        results_on_stack = level.results['level.rms'].data

        self.assertEqual(results_on_stack,
                         results_on_file)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
