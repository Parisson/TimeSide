#! /usr/bin/env python

from __future__ import division
from unit_timeside import unittest, TestRunner

from timeside.core.processor import ProcessPipe
from timeside.plugins.decoder.file import FileDecoder

from timeside.core.tools.test_samples import samples

import os.path

#from glib import GError as GST_IOError
# HINT : to use later with Gnonlin only


class TestDecoding(unittest.TestCase):

    "Test decoding features"

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = None, None, None
        self.start = 0
        self.duration = None

        self.expected_samplerate = 44100
        self.expected_channels = 2
        self.test_exact_duration = True
        self.source_duration = 8
        self.expected_mime_type = 'audio/x-wav'

    def testWav(self):
        "Test wav decoding"
        self.source = samples["sweep.wav"]

    def testWavMono(self):
        "Test mono wav decoding"
        self.source = samples["sweep_mono.wav"]

        self.expected_channels = 1

    def testWav32k(self):
        "Test 32kHz wav decoding"
        self.source = samples["sweep_32000.wav"]

        self.expected_samplerate = 32000

    def testFlac(self):
        "Test flac decoding"
        self.source = samples["sweep.flac"]
        self.expected_mime_type = 'audio/x-flac'

    def testOgg(self):
        "Test ogg decoding"
        self.source = samples["sweep.ogg"]

        self.expected_mime_type = 'audio/ogg'
        self.test_exact_duration = False

    def testMp3(self):
        "Test mp3 decoding"
        self.source = samples["sweep.mp3"]

        self.expected_mime_type = 'audio/mpeg'
        self.test_exact_duration = False

    def tearDown(self):
        decoder = FileDecoder(uri=self.source,
                              start=self.start,
                              duration=self.duration)

        decoder.setup(samplerate=self.samplerate, channels=self.channels,
                      blocksize=self.blocksize)

        totalframes = 0

        while True:
            frames, eod = decoder.process()
            totalframes += frames.shape[0]
            if eod or decoder.eod:
                break
            self.assertEqual(frames.shape[0], decoder.blocksize())
            self.assertEqual(frames.shape[1], decoder.channels())

        ratio = decoder.output_samplerate / decoder.input_samplerate
        if 0:
            print("input / output_samplerate:", decoder.input_samplerate, '/', decoder.output_samplerate,)
            print("ratio:", ratio)
            print("input / output_channels:", decoder.input_channels, decoder.output_channels)
            print("input_duration:", decoder.input_duration)
            print("input_totalframes:", decoder.input_totalframes)
            print("mime_type", decoder.mime_type())

        if self.channels:
            # when specified, check that the channels are the ones requested
            self.assertEqual(self.channels, decoder.output_channels)
        else:
            # otherwise check that the channels are preserved, if not specified
            self.assertEqual(decoder.input_channels, decoder.output_channels)
            # and if we know the expected channels, check the output match
            if self.expected_channels:
                self.assertEqual(
                    self.expected_channels, decoder.output_channels)
        # do the same with the sampling rate
        if self.samplerate:
            self.assertEqual(self.samplerate, decoder.output_samplerate)
        else:
            self.assertEqual(
                decoder.input_samplerate, decoder.output_samplerate)
            if self.expected_samplerate:
                self.assertEqual(
                    self.expected_samplerate, decoder.output_samplerate)

        self.assertEqual(decoder.mime_type(), self.expected_mime_type)

        expected_totalframes = int(decoder.input_duration *
                                   decoder.output_samplerate)

        input_duration = decoder.input_totalframes / decoder.input_samplerate
        output_duration = decoder.totalframes() / decoder.output_samplerate

        if self.test_exact_duration:
            self.assertEqual(input_duration, output_duration)
            self.assertEqual(input_duration, decoder.uri_duration)
            self.assertEqual(self.source_duration, decoder.uri_duration)
            self.assertEqual(totalframes, expected_totalframes)
        else:
            self.assertAlmostEqual(input_duration, output_duration,
                    places=5)
            self.assertAlmostEqual(input_duration, decoder.uri_duration,
                    places=3)
            self.assertAlmostEqual(self.source_duration, decoder.uri_duration,
                    delta=.08)
            self.assertAlmostEqual(totalframes, expected_totalframes, delta=69)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
