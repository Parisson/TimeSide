import unittest
from unit_timeside import TestRunner
from test_encoding import TestEncoding

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
        super(TestEncodingToDevNull, self).setUp()
        self.sink = '/dev/null'
        self.encode_to_file = False


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


class TestEncodingOverwriteFails(unittest.TestCase):
    "Test encoding features"

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = 44100, 1, 1024
        self.overwrite = False

    def tearDown(self):
        self.assertRaises(IOError, self.encoder_function, self.sink)


class TestEncodingOverwriteForced(unittest.TestCase):
    "Test encoding features"

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = 44100, 1, 1024
        import tempfile
        self.tmpfile = tempfile.NamedTemporaryFile(delete=True)
        self.sink = self.tmpfile.name
        self.overwrite = True

    def tearDown(self):
        super(TestEncodingOverwriteForced, self).tearDown()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
