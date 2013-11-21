#! /usr/bin/env python

from math import pi
from numpy import arange, sin
from unit_timeside import *

from os import unlink


class TestEncoding(TestCase):
    "Test encoding features"

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = 44100, 1, 1024
        import tempfile
        self.tmpfile = tempfile.NamedTemporaryFile(delete=True)
        self.sink = self.tmpfile.name
        self.tmpfile.close()
        self.overwrite = False

    def testWav(self):
        "Test wav encoding"
        from timeside.encoder.wav import WavEncoder
        self.encoder_function = WavEncoder

    def testVorbis(self):
        "Test vorbis encoding"
        from timeside.encoder.ogg import VorbisEncoder
        self.encoder_function = VorbisEncoder

    def testMp3(self):
        "Test mp3 encoding"
        from timeside.encoder.mp3 import Mp3Encoder
        self.encoder_function = Mp3Encoder

    def testAac(self):
        "Test aac encoding"
        from timeside.encoder.m4a import AacEncoder
        self.encoder_function = AacEncoder

    def testFlac(self):
        "Test flac encoding"
        from timeside.encoder.flac import FlacEncoder
        self.encoder_function = FlacEncoder

    def testWebm(self):
        "Test webm encoding"
        from timeside.encoder.webm import WebMEncoder
        self.encoder_function = WebMEncoder

    def tearDown(self):
        self.encoder = self.encoder_function(self.sink,
                                             overwrite=self.overwrite)
        self.encoder.setup(channels=self.channels,
                           samplerate=self.samplerate)

        written_frames, eod = 0, False
        total_frames = 3. * self.samplerate
        block_size = self.blocksize
        f0 = 800.
        omega = 2. * pi * f0 / float(self.samplerate)

        while True:
            remaining = total_frames - written_frames
            if remaining >= block_size:
                write_length = block_size
            else:
                write_length = remaining
                eod = True
            # build a sinusoid
            frames = .75 * sin(omega * (arange(write_length) + written_frames))
            # process encoder, writing to file
            self.encoder.process(frames, eod)
            written_frames += frames.shape[0]
            if eod:
                self.assertEquals(self.encoder.eod, True)
                break

        self.encoder.release()

        if 0:
            import commands
            print commands.getoutput('sndfile-info ' + self.sink)

        self.assertEquals(written_frames, total_frames)

        if hasattr(self, 'tmpfile'):
            unlink(self.sink)


class TestEncodingLongBlock(TestEncoding):
    "Test encoding features with longer blocksize"

    def setUp(self):
        super(TestEncodingLongBlock, self).setUp()
        self.blocksize *= 8


class TestEncodingShortBlock(TestEncoding):
    "Test encoding features with short blocksize"

    def setUp(self):
        super(TestEncodingShortBlock, self).setUp()
        self.blocksize = 64


class TestEncodingLowSamplerate(TestEncoding):
    "Test encoding features with low samplerate"

    def setUp(self):
        super(TestEncodingLowSamplerate, self).setUp()
        self.samplerate = 8000


class TestEncodingHighSamplerate(TestEncoding):
    "Test encoding features with high samplerate"

    def setUp(self):
        super(TestEncodingHighSamplerate, self).setUp()
        self.samplerate = 48000


# class TestEncodingTooManyChannels(TestEncoding):
#     "Test encoding features with high samplerate"

#     def setUp(self):
#         super(TestEncodingTooManyChannels, self).setUp()
#         self.samplerate = 192000 * 2
#         self.channels = 128

#     def tearDown(self):
#         self.encoder.setup(channels = self.channels,
#                            samplerate = self.samplerate)
#         self.assertRaises(IOError, self.encoder.release)
#         unlink(self.sink)


class TestEncodingStereo(TestEncoding):
    "Test encoding features with stereo"

    def setUp(self):
        super(TestEncodingStereo, self).setUp()
        self.channels = 2


class TestEncodingToDevNull(TestEncoding):
    "Test encoding features with /dev/null"

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = 44100, 1, 1024
        self.sink = '/dev/null'
        self.overwrite = False


class TestEncodingToDirectory(TestEncoding):
    "Test encoding features to a directory"

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = 44100, 1, 1024
        import tempfile
        self.sink = tempfile.mkdtemp()
        self.overwrite = False

    def tearDown(self):
        from os import rmdir
        self.assertRaises(IOError, self.encoder_function, self.sink)
        rmdir(self.sink)


class TestEncodingOverwriteFails(TestCase):
    "Test encoding features"

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = 44100, 1, 1024
        import tempfile
        self.tmpfile = tempfile.NamedTemporaryFile(delete=True)
        self.sink = self.tmpfile.name
        self.overwrite = False

    def tearDown(self):
        self.assertRaises(IOError, self.encoder_function, self.sink)
        self.tmpfile.close()


class TestEncodingOverwriteForced(TestCase):
    "Test encoding features"

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = 44100, 1, 1024
        import tempfile
        self.tmpfile = tempfile.NamedTemporaryFile(delete=True)
        self.sink = self.tmpfile.name
        self.overwrite = True


    def tearDown(self):
        super(TestEncodingOverwriteForced, self).tearDown()
        self.tmpfile.close()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
