import os.path
import unittest
from unit_timeside import TestRunner
from test_decoding import TestDecoding, samples
from timeside.core.processor import ProcessPipe
from timeside.plugins.decoder.file import FileDecoder

class TestDecodingSegment(TestDecoding):

    def setUp(self):
        super(TestDecodingSegment, self).setUp()
        self.start = 1
        self.duration = 3
        self.source_duration = self.duration

    """
    @unittest.skip("Flac not supported until bug fix is GST Gnonlin")
    def testFlac(self):
        "Test flac decoding"

    @unittest.skip("Ogg not supported until bug fix is GST Gnonlin")
    def testOgg(self):
        "Test ogg decoding"
    """


class TestDecodingSegmentDefaultStart(TestDecodingSegment):

    def setUp(self):
        super(TestDecodingSegmentDefaultStart, self).setUp()
        self.duration = 1
        self.source_duration = self.duration


class TestDecodingSegmentDefaultDuration(TestDecodingSegment):

    def setUp(self):
        super(TestDecodingSegment, self).setUp()
        self.start = 1
        self.source_duration -= self.start


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


class TestDecodingMonoDownsampling(TestDecoding):

    def setUp(self):
        super(TestDecodingMonoDownsampling, self).setUp()
        self.samplerate, self.channels, self.blocksize = 16000, None, None


class TestDecodingStereoDownsampling(TestDecoding):

    def setUp(self):
        super(TestDecodingStereoDownsampling, self).setUp()
        self.samplerate, self.channels, self.blocksize = 32000, 2, None


class TestDecodingStereoUpsampling(TestDecoding):

    def setUp(self):
        super(TestDecodingStereoUpsampling, self).setUp()
        self.samplerate, self.channels, self.blocksize = 96000, 2, None


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
