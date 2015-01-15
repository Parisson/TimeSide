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

        self.expected_mime_type = 'application/ogg'
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
            print "input / output_samplerate:", decoder.input_samplerate, '/', decoder.output_samplerate,
            print "ratio:", ratio
            print "input / output_channels:", decoder.input_channels, decoder.output_channels
            print "input_duration:", decoder.input_duration
            print "input_totalframes:", decoder.input_totalframes
            print "mime_type", decoder.mime_type()

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
            self.assertEqual(input_duration,
                             decoder.uri_duration)
            self.assertEqual(self.source_duration,
                             decoder.uri_duration)
            self.assertEqual(totalframes, expected_totalframes)

        else:
            self.assertAlmostEqual(input_duration, output_duration,
                                   places=1)
            self.assertAlmostEqual(input_duration,
                                   decoder.uri_duration,
                                   places=1)
            self.assertAlmostEqual(self.source_duration,
                                   decoder.uri_duration,
                                   places=1)
            self.assertAlmostEqual(totalframes, expected_totalframes, delta=69)


class TestDecodingSegment(TestDecoding):

    def setUp(self):
        super(TestDecodingSegment, self).setUp()
        self.start = 1
        self.duration = 3
        self.source_duration = self.duration

    def testMp3(self):
        "Test mp3 decoding"
        super(TestDecodingSegment, self).testMp3()

    def testWav(self):
        "Test wav decoding"
        super(TestDecodingSegment, self).testWav()

    def testWavMono(self):
        "Test mono wav decoding"
        super(TestDecodingSegment, self).testWavMono()

    def testWav32k(self):
        "Test 32kHz wav decoding"
        super(TestDecodingSegment, self).testWav32k()

    @unittest.skip("Flac not supported until bug fix is GST Gnonlin")
    def testFlac(self):
        "Test flac decoding"

    @unittest.skip("Ogg not supported until bug fix is GST Gnonlin")
    def testOgg(self):
        "Test ogg decoding"


class TestDecodingSegmentDefaultStart(TestDecodingSegment):

    def setUp(self):
        super(TestDecodingSegmentDefaultStart, self).setUp()
        self.duration = 1
        self.source_duration = self.duration

    def testMp3(self):
        "Test mp3 decoding"
        super(TestDecodingSegmentDefaultStart, self).testMp3()


class TestDecodingSegmentDefaultDuration(TestDecodingSegment):

    def setUp(self):
        super(TestDecodingSegment, self).setUp()
        self.start = 1
        self.source_duration -= self.start

    def testWav(self):
        "Test wav decoding"
        super(TestDecodingSegment, self).testWav()

    def testWavMono(self):
        "Test mono wav decoding"
        super(TestDecodingSegment, self).testWavMono()

    def testWav32k(self):
        "Test 32kHz wav decoding"
        super(TestDecodingSegment, self).testWav32k()

    def testMp3(self):
        "Test mp3 decoding"
        super(TestDecodingSegment, self).testMp3()


class TestDecodingSegmentBadParameters(unittest.TestCase):

    def setUp(self):
        self.source = samples["sweep.wav"]

    def test_bad_start_value(self):
        "Test decoding segment with start value exceeding the media duration"
        decoder = FileDecoder(self.source, start=10)
        pipe = ProcessPipe(decoder)
        self.assertRaises(ValueError, pipe.run)

    def test_bad_duration_value(self):
        "Test decoding segment with a too large duration value argument"
        decoder = FileDecoder(self.source, duration=10)
        pipe = ProcessPipe(decoder)
        self.assertRaises(ValueError, pipe.run)


class TestDecodingStereo(TestDecoding):

    def setUp(self):
        super(TestDecodingStereo, self).setUp()
        self.samplerate, self.channels, self.blocksize = None, 2, None


class TestDecodingMonoUpsampling(TestDecoding):

    def setUp(self):
        super(TestDecodingMonoUpsampling, self).setUp()
        self.samplerate, self.channels, self.blocksize = 48000, None, None

    def testMp3(self):
        "Test mp3 decoding"
        super(TestDecodingMonoUpsampling, self).testMp3()

    def testWav(self):
        "Test wav decoding"
        super(TestDecodingMonoUpsampling, self).testWav()

    def testWavMono(self):
        "Test mono wav decoding"
        super(TestDecodingMonoUpsampling, self).testWavMono()

    def testWav32k(self):
        "Test 32kHz wav decoding"
        super(TestDecodingMonoUpsampling, self).testWav32k()

    def testFlac(self):
        "Test flac decoding"
        super(TestDecodingMonoUpsampling, self).testFlac()

    def testOgg(self):
        "Test ogg decoding"
        super(TestDecodingMonoUpsampling, self).testOgg()


class TestDecodingMonoDownsampling(TestDecoding):

    def setUp(self):
        super(TestDecodingMonoDownsampling, self).setUp()
        self.samplerate, self.channels, self.blocksize = 16000, None, None

    def testWav32k(self):
        "Test 32kHz wav decoding"
        super(TestDecodingMonoDownsampling, self).testWav32k()

    def testOgg(self):
        "Test ogg decoding"
        super(TestDecodingMonoDownsampling, self).testOgg()

    def testMp3(self):
        "Test mp3 decoding"
        super(TestDecodingMonoDownsampling, self).testMp3()


class TestDecodingStereoDownsampling(TestDecoding):

    def setUp(self):
        super(TestDecodingStereoDownsampling, self).setUp()
        self.samplerate, self.channels, self.blocksize = 32000, 2, None

    def testWav32k(self):
        "Test 32kHz wav decoding"
        super(TestDecodingStereoDownsampling, self).testWav32k()

    def testOgg(self):
        "Test ogg decoding"
        super(TestDecodingStereoDownsampling, self).testOgg()

    def testMp3(self):
        "Test mp3 decoding"
        super(TestDecodingStereoDownsampling, self).testMp3()


class TestDecodingStereoUpsampling(TestDecoding):

    def setUp(self):
        super(TestDecodingStereoUpsampling, self).setUp()
        self.samplerate, self.channels, self.blocksize = 96000, 2, None

    def testWav32k(self):
        "Test 32kHz wav decoding"
        super(TestDecodingStereoUpsampling, self).testWav32k()

    def testOgg(self):
        "Test ogg decoding"
        super(TestDecodingStereoUpsampling, self).testOgg()

    def testMp3(self):
        "Test mp3 decoding"
        super(TestDecodingStereoUpsampling, self).testMp3()


class TestDecodingShortBlock(TestDecoding):

    def setUp(self):
        super(TestDecodingShortBlock, self).setUp()
        self.samplerate, self.channels, self.blocksize = None, None, 256


class TestDecodingLongBlock(TestDecoding):

    def setUp(self):
        super(TestDecodingLongBlock, self).setUp()
        self.samplerate, self.channels, self.blocksize = None, None, 1024 * \
            8 * 2


class TestDecodingWrongFiles(unittest.TestCase):

    "Test decoding features"

    def testMissingFile(self):
        "Test decoding missing file"
        self.source = os.path.join(os.path.dirname(__file__),
                                   "a_missing_file.wav")
        self.assertRaises(IOError, FileDecoder, self.source)

    def testDevNull(self):
        "Test decoding dev null"
        self.source = "/dev/null"
        with self.assertRaises(IOError):
            FileDecoder(self.source)

    def testNoAudioStream(self):
        "Test decoding file withouth audio stream"
        self.source = __file__
        with self.assertRaises(IOError):
            FileDecoder(self.source)

    def testEmptyFile(self):
        "Test decoding empty file"
        import tempfile
        self.tmpfile = tempfile.NamedTemporaryFile(delete=True)
        self.source = self.tmpfile.name
        with self.assertRaises(IOError):
            FileDecoder(self.source)

        self.tmpfile.close()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
