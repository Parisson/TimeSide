#! /usr/bin/env python

from timeside.decoder.core import FileDecoder
from unit_timeside import *

import os.path

#from glib import GError as GST_IOError
# HINT : to use later with Gnonlin only

class TestDecoding(TestCase):
    "Test decoding features"

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = None, None, None
        self.start = 0
        self.duration = None

        self.expected_samplerate = 44100
        self.expected_channels = 2
        self.expected_totalframes = 352800

    def testWav(self):
        "Test wav decoding"
        self.source = os.path.join(os.path.dirname(__file__),
                                    "samples/sweep.wav")


    def testWavMono(self):
        "Test mono wav decoding"
        self.source = os.path.join(os.path.dirname(__file__),
                                   "samples/sweep_mono.wav")

        self.expected_channels = 1

    def testWav32k(self):
        "Test 32kHz wav decoding"
        self.source = os.path.join(os.path.dirname(__file__),
                                   "samples/sweep_32000.wav")

        expected_samplerate = 32000
        ratio = expected_samplerate/float(self.expected_samplerate)

        self.expected_totalframes = int(self.expected_totalframes * ratio)
        self.expected_samplerate = expected_samplerate

    def testFlac(self):
        "Test flac decoding"
        self.source = os.path.join(os.path.dirname(__file__),
                                   "samples/sweep.flac")

    def testOgg(self):
        "Test ogg decoding"
        self.source = os.path.join(os.path.dirname(__file__),
                                   "samples/sweep.ogg")

        self.expected_totalframes = 352832

    def testMp3(self):
        "Test mp3 decoding"
        self.source = os.path.join(os.path.dirname(__file__),
                                   "samples/sweep.mp3")

        self.expected_totalframes = 353664

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
            self.assertEquals(frames.shape[0], decoder.blocksize())
            self.assertEquals(frames.shape[1], decoder.channels())

        ratio = decoder.output_samplerate / float(decoder.input_samplerate)
        if 0:
            print "input / output_samplerate:", decoder.input_samplerate, '/', decoder.output_samplerate,
            print "ratio:", ratio
            print "input / output_channels:", decoder.input_channels, decoder.output_channels
            print "input_duration:", decoder.input_duration
            print "input_totalframes:", decoder.input_totalframes

        if self.channels:
            # when specified, check that the channels are the ones requested
            self.assertEquals(self.channels, decoder.output_channels)
        else:
            # otherwise check that the channels are preserved, if not specified
            self.assertEquals(decoder.input_channels, decoder.output_channels)
            # and if we know the expected channels, check the output match
            if self.expected_channels:
                self.assertEquals(self.expected_channels, decoder.output_channels)
        # do the same with the sampling rate
        if self.samplerate:
            self.assertEquals(self.samplerate, decoder.output_samplerate)
        else:
            self.assertEquals(decoder.input_samplerate, decoder.output_samplerate)
            if self.expected_samplerate:
                self.assertEquals(self.expected_samplerate, decoder.output_samplerate)

        self.assertEquals(totalframes, self.expected_totalframes)


class TestDecodingSegment(TestDecoding):

    def setUp(self):
        super(TestDecodingSegment, self).setUp()
        self.start = 1
        self.duration = 3

        self.expected_totalframes = self.duration * self.expected_samplerate


    def testMp3(self):
        "Test mp3 decoding"
        super(TestDecodingSegment, self).testMp3()
        self.expected_totalframes = self.duration * self.expected_samplerate + 1

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
        self.expected_totalframes = self.duration * self.expected_samplerate

    def testMp3(self):
        "Test mp3 decoding"
        super(TestDecodingSegmentDefaultStart, self).testMp3()
        self.expected_totalframes = self.duration * self.expected_samplerate + 1


class TestDecodingSegmentDefaultDuration(TestDecodingSegment):

    def setUp(self):
        super(TestDecodingSegment, self).setUp()
        self.start = 1
        self.expected_totalframes = self.expected_totalframes - self.start * self.expected_samplerate

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
        self.expected_totalframes = 310715#308701


class TestDecodingStereo(TestDecoding):

    def setUp(self):
        super(TestDecodingStereo, self).setUp()
        self.samplerate, self.channels, self.blocksize = None, 2, None


class TestDecodingMonoUpsampling(TestDecoding):

    def setUp(self):
        super(TestDecodingMonoUpsampling, self).setUp()
        self.samplerate, self.channels, self.blocksize = 48000, None, None
        self.expected_totalframes = 384000

    def testMp3(self):
        "Test mp3 decoding"
        super(TestDecodingMonoUpsampling, self).testMp3()
        self.expected_totalframes = 384941

    def testWav(self):
        "Test wav decoding"
        super(TestDecodingMonoUpsampling, self).testWav()

    def testWavMono(self):
        "Test mono wav decoding"
        super(TestDecodingMonoUpsampling, self).testWavMono()

    def testWav32k(self):
        "Test 32kHz wav decoding"
        super(TestDecodingMonoUpsampling, self).testWav32k()
        self.expected_totalframes = 384000

    def testFlac(self):
        "Test flac decoding"
        super(TestDecodingMonoUpsampling, self).testFlac()

    def testOgg(self):
        "Test ogg decoding"
        super(TestDecodingMonoUpsampling, self).testOgg()
        self.expected_totalframes = 384000


class TestDecodingMonoDownsampling(TestDecoding):

    def setUp(self):
        super(TestDecodingMonoDownsampling, self).setUp()
        self.samplerate, self.channels, self.blocksize = 16000, None, None

        self.expected_totalframes = 128000

    def testWav32k(self):
        "Test 32kHz wav decoding"
        super(TestDecodingMonoDownsampling, self).testWav32k()
        self.expected_totalframes = 128000

    def testOgg(self):
        "Test ogg decoding"
        super(TestDecodingMonoDownsampling, self).testOgg()
        self.expected_totalframes = 127980

    def testMp3(self):
        "Test mp3 decoding"
        super(TestDecodingMonoDownsampling, self).testMp3()
        self.expected_totalframes = 128314

class TestDecodingStereoDownsampling(TestDecoding):

    def setUp(self):
        super(TestDecodingStereoDownsampling, self).setUp()
        self.samplerate, self.channels, self.blocksize = 32000, 2, None

        self.expected_totalframes = 256000

    def testWav32k(self):
        "Test 32kHz wav decoding"
        super(TestDecodingStereoDownsampling, self).testWav32k()
        self.expected_totalframes = 256000

    def testOgg(self):
        "Test ogg decoding"
        super(TestDecodingStereoDownsampling, self).testOgg()
        self.expected_totalframes = 255992

    def testMp3(self):
        "Test mp3 decoding"
        super(TestDecodingStereoDownsampling, self).testMp3()
        self.expected_totalframes = 256627


class TestDecodingStereoUpsampling(TestDecoding):

    def setUp(self):
        super(TestDecodingStereoUpsampling, self).setUp()
        self.samplerate, self.channels, self.blocksize = 96000, 2, None

        self.expected_totalframes = 768000

    def testWav32k(self):
        "Test 32kHz wav decoding"
        super(TestDecodingStereoUpsampling, self).testWav32k()
        self.expected_totalframes = 768000

    def testOgg(self):
        "Test ogg decoding"
        super(TestDecodingStereoUpsampling, self).testOgg()
        self.expected_totalframes = 768000

    def testMp3(self):
        "Test mp3 decoding"
        super(TestDecodingStereoUpsampling, self).testMp3()
        self.expected_totalframes = 769881


class TestDecodingShortBlock(TestDecoding):

    def setUp(self):
        super(TestDecodingShortBlock, self).setUp()
        self.samplerate, self.channels, self.blocksize = None, None, 256


class TestDecodingLongBlock(TestDecoding):

    def setUp(self):
        super(TestDecodingLongBlock, self).setUp()
        self.samplerate, self.channels, self.blocksize = None, None, 1024*8*2


class TestDecodingWrongFiles(TestCase):
    "Test decoding features"

    def testMissingFile(self):
        "Test decoding missing file"
        self.source = os.path.join(os.path.dirname(__file__),
                                    "a_missing_file_blahblah.wav")

        self.assertRaises(IOError, FileDecoder, self.source)

    def testDevNull(self):
        "Test decoding dev null"
        self.source = "/dev/null"
        decoder = FileDecoder(self.source)
        self.assertRaises(IOError, FileDecoder.setup, decoder)

    def testNoAudioStream(self):
        "Test decoding file withouth audio stream"
        self.source = __file__
        decoder = FileDecoder(self.source)
        self.assertRaises(IOError, FileDecoder.setup, decoder)

    def testEmptyFile(self):
        "Test decoding empty file"
        import tempfile
        self.tmpfile = tempfile.NamedTemporaryFile(delete=True)
        self.source = self.tmpfile.name
        decoder = FileDecoder(self.source)
        self.assertRaises(IOError, FileDecoder.setup, decoder)
        self.tmpfile.close()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
