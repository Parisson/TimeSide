#! /usr/bin/env python
from __future__ import division

from timeside.plugins.decoder.array import ArrayDecoder
from unit_timeside import *

import numpy as np


class TestDecoding(unittest.TestCase):

    "Test decoding for ArrayDecoder"

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = None, None, None
        self.start = 0
        self.duration = None
        self.array_duration = 8
        self.expected_duration = self.array_duration
        self.expected_is_segment = False

    def test1DArray(self):
        "Test 1D Array decoding"
        self.source_samplerate = 44100
        self.source = np.random.randn(
            self.array_duration * self.source_samplerate,)
        self.source_channels = 1

    def test2DArrayMono(self):
        "Test 2D Array mono decoding"
        self.source_samplerate = 32000
        self.source = np.random.randn(
            self.array_duration * self.source_samplerate, 1)
        self.source_channels = 1

    def test2DArrayStereo(self):
        "Test 2D Array stereo decoding"
        self.source_samplerate = 22050
        self.source = np.random.randn(
            self.array_duration * self.source_samplerate, 2)
        self.source_channels = 2

    def test2DArrayMultiChannel(self):
        "Test 2D Array multi-channel decoding"
        self.source_samplerate = 16000
        self.source = np.random.randn(
            self.array_duration * self.source_samplerate, 5)
        self.source_channels = 5

    def tearDown(self):
        decoder = ArrayDecoder(samples=self.source,
                               samplerate=self.source_samplerate,
                               start=self.start,
                               duration=self.duration)

        decoder.setup(samplerate=self.samplerate, channels=self.channels,
                      blocksize=self.blocksize)

        # Check input
        self.assertEqual(self.source_samplerate, decoder.input_samplerate)
        self.assertEqual(self.expected_is_segment, decoder.is_segment)
        self.assertEqual(self.expected_duration, decoder.input_duration)
        self.assertEqual(self.source_channels, decoder.input_channels)
        # Check output
        self.assertEqual(self.source_samplerate, decoder.samplerate())
        self.assertEqual(self.source_channels, decoder.channels())

        # Check Idecoder interface
        self.assertIsInstance(decoder.mediainfo(), dict)
        self.assertIsInstance(decoder.format(), str)
        self.assertIsInstance(decoder.encoding(), str)
        self.assertIsInstance(decoder.resolution(), int)
        self.assertIsNone(decoder.metadata())

        totalframes = 0

        while True:
            frames, eod = decoder.process()
            totalframes += frames.shape[0]
            if eod:
                break
            self.assertEqual(frames.shape[0], decoder.blocksize())
            self.assertEqual(frames.shape[1], decoder.channels())

        if self.channels:
            # when specified, check that the channels are the ones requested
            self.assertEqual(self.channels, decoder.output_channels)
        else:
            # otherwise check that the channels are preserved, if not specified
            self.assertEqual(decoder.input_channels, decoder.output_channels)
            # and if we know the expected channels, check the output match
            if self.source_channels:
                self.assertEqual(
                    self.source_channels, decoder.output_channels)
        # do the same with the sampling rate
        if self.samplerate:
            self.assertEqual(self.samplerate, decoder.output_samplerate)
        else:
            self.assertEqual(
                decoder.input_samplerate, decoder.output_samplerate)

        self.assertEqual(totalframes,
                         self.expected_duration * decoder.output_samplerate)
        self.assertEquals(totalframes, decoder.totalframes())


class TestDecodingSegment(TestDecoding):

    def setUp(self):
        super(TestDecodingSegment, self).setUp()
        self.start = 1
        self.duration = 3
        self.expected_is_segment = True
        self.expected_duration = self.duration


class TestDecodingSegmentDefaultStart(TestDecodingSegment):

    def setUp(self):
        super(TestDecodingSegmentDefaultStart, self).setUp()
        self.start = 0
        self.duration = 1
        self.expected_duration = self.duration


class TestDecodingSegmentDefaultDuration(TestDecodingSegment):

    def setUp(self):
        super(TestDecodingSegmentDefaultDuration, self).setUp()
        self.start = 1
        self.duration = None
        self.expected_duration = self.array_duration - self.start


class TestDecodingShortBlock(TestDecoding):

    def setUp(self):
        super(TestDecodingShortBlock, self).setUp()
        self.blocksize = 256


class TestDecodingLongBlock(TestDecoding):

    def setUp(self):
        super(TestDecodingLongBlock, self).setUp()
        self.blocksize = 1024 * 8 * 2


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
