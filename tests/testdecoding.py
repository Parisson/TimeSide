from timeside.decoder.core import FileDecoder
from unit_timeside import *

import os.path

class TestDecoding(TestCase):
    "Test the low level streaming features"

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = None, None, None

    def testWav(self):
        "Test wav decoding"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")

    def testFlac(self):
        "Test flac decoding"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")

    def testOgg(self):
        "Test ogg decoding"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")

    def testMp3(self):
        "Test mp3 decoding"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")

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

        # FIXME compute actual number of frames from file
        if ratio == 1:
            if os.path.splitext(self.source)[-1].lower() == '.mp3':
                self.assertEquals(totalframes, 353664)
            elif os.path.splitext(self.source)[-1].lower() == '.ogg':
                self.assertEquals(totalframes, 352832)
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

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
