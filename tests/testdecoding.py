from timeside.decoder.core import FileDecoder
from unit_timeside import *

import os.path

class TestDecoding(TestCase):
    "Test decoding features"

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = None, None, None

    def testWav(self):
        "Test wav decoding"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")

        self.expected_channels = 2
        self.expected_samplerate = 44100

    def testWavMono(self):
        "Test mono wav decoding"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep_mono.wav")

        self.expected_channels = 1
        self.expected_samplerate = 44100

    def testWav32k(self):
        "Test 32kHz wav decoding"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep_32000.wav")

        self.expected_channels = 2
        self.expected_samplerate = 32000

    def testFlac(self):
        "Test flac decoding"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")

        self.expected_channels = 2
        self.expected_samplerate = 44100

    def testOgg(self):
        "Test ogg decoding"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")

        self.expected_channels = 2
        self.expected_samplerate = 44100

    def testMp3(self):
        "Test mp3 decoding"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")

        self.expected_channels = 2
        self.expected_samplerate = 44100

    def tearDown(self):
        decoder = FileDecoder(self.source)

        decoder.setup(samplerate = self.samplerate, channels = self.channels, blocksize = self.blocksize)

        totalframes = 0.

        while True:
            frames, eod = decoder.process()
            totalframes += frames.shape[0]
            if eod or decoder.eod: break
            self.assertEquals(frames.shape[0], decoder.blocksize() )
            self.assertEquals(frames.shape[1], decoder.channels() )

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

        # FIXME compute actual number of frames from file
        if ratio == 1:
            if os.path.splitext(self.source)[-1].lower() == '.mp3':
                self.assertEquals(totalframes, 353664)
            elif os.path.splitext(self.source)[-1].lower() == '.ogg':
                self.assertEquals(totalframes, 352832)
            else:
                if '_32000.wav' in self.source:
                    self.assertEquals(totalframes, 256000)
                else:
                    self.assertEquals(totalframes, 352800)

class TestDecodingStereo(TestDecoding):

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = None, 2, None

class TestDecodingMonoUpsampling(TestDecoding):

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = 48000, None, None

class TestDecodingMonoDownsampling(TestDecoding):

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = 16000, None, None

class TestDecodingStereoDownsampling(TestDecoding):

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = 32000, 2, None

class TestDecodingStereoUpsampling(TestDecoding):

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = 96000, 2, None

class TestDecodingShortBlock(TestDecoding):

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = None, None, 256

class TestDecodingLongBlock(TestDecoding):

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = None, None, 1024*8*2

class TestDecodingWrongFiles(TestCase):
    "Test decoding features"

    def testMissingFile(self):
        "Test decoding missing file"
        self.source = os.path.join (os.path.dirname(__file__),  "a_missing_file_blahblah.wav")
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
