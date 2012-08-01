from timeside.decoder import *
from unit_timeside import *

import os.path

class TestDecoding(TestCase):
    "Test the low level streaming features"

    def setUp(self):
        self.samplerate, self.channels, self.nframes = None, None, None
   
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

        decoder.setup(samplerate = self.samplerate, channels = self.channels, nframes = self.nframes)

        totalframes = 0.

        while True:
            frames, eod = decoder.process()
            totalframes += frames.shape[0]
            if eod or decoder.eod: break

        decoder.release()

        if 0:
          print "input / output_samplerate:",   decoder.input_samplerate, '/', decoder.output_samplerate,
          ratio = decoder.output_samplerate / float(decoder.input_samplerate)
          print "ratio:",             ratio
          print "input / output_channels:",   decoder.input_channels, decoder.output_channels
          print "input_duration:",     decoder.input_duration
          print "input_total_frames:", decoder.input_total_frames

        """
        # FIXME compute actual number of frames from file
        if os.path.splitext(self.source)[-1].lower() == '.mp3':
            self.assertEquals(totalframes, ratio * 355969 )
        elif os.path.splitext(self.source)[-1].lower() == '.ogg':
            self.assertEquals(totalframes, ratio * 352833)
        else:
            self.assertEquals(totalframes, ratio * 352801)
        """

class TestDecodingStereo(TestDecoding):

    def setUp(self):
        self.samplerate, self.channels, self.nframes = None, 2, None

class TestDecodingResampling(TestDecoding):

    def setUp(self):
        self.samplerate, self.channels, self.nframes = 16000, None, None

class TestDecodingStereoResampling(TestDecoding):

    def setUp(self):
        self.samplerate, self.channels, self.nframes = 32000, 2, None

class TestDecodingStereoUpsampling(TestDecoding):

    def setUp(self):
        self.samplerate, self.channels, self.nframes = 96000, 2, None

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
