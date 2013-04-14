from timeside.core import *
from timeside.decoder import *
from timeside.analyzer import *
from timeside.encoder import *
from timeside.api import *
from timeside.component import *

from unit_timeside import *

import os.path

class TestTranscodingFromWav(TestCase):
    "Test transcoding from wav"

    def tmpTarget(self):
        import tempfile
        self.tmpfile = tempfile.NamedTemporaryFile(delete=True)
        self.target = self.tmpfile.name
        self.tmpfile.close()

    def setUp(self):
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")

    def testToWav(self):
        "Test conversion to wav"
        self.tmpTarget()
        self.encoder = WavEncoder(self.target)

    def testToMp3(self):
        "Test conversion to mp3"
        self.tmpTarget()
        self.encoder = Mp3Encoder(self.target)

    def testToOgg(self):
        "Test conversion to ogg"
        self.tmpTarget()
        self.encoder = VorbisEncoder(self.target)

    # def testToWebM(self):
    #     "Test conversion to webm"
    #     self.tmpTarget()
    #     self.encoder = WebMEncoder(self.target)

    # def testToM4a(self):
    #     "Test conversion to m4a"
    #     self.tmpTarget()
    #     self.encoder = AacEncoder(self.target)

    def setUpDecoder(self):
        self.decoder = FileDecoder(self.source)
        self.decoder.setup()
        self.channels  = self.decoder.channels()
        self.samplerate = self.decoder.samplerate()

    def setUpEncoder(self):
        self.encoder.setup(channels = self.channels, samplerate = self.samplerate)

    def tearDown(self):
        self.setUpDecoder()
        self.setUpEncoder()

        totalframes = 0
        while True:
            frames, eod = self.decoder.process()
            self.encoder.process(frames, eod)
            totalframes += frames.shape[0]
            if eod or self.encoder.eod: break


        #print self.channels, self.samplerate, totalframes

        self.encoder.release()

        decoder = FileDecoder(self.target)
        decoder.setup()
        written_frames = 0
        while True:
            frames, eod = decoder.process()
            written_frames += frames.shape[0]
            if eod: break

        #print decoder.channels(), decoder.samplerate(), written_frames

        self.assertEquals(self.channels, decoder.channels())
        self.assertEquals(self.samplerate, decoder.samplerate())
        self.assertTrue(written_frames - totalframes >= 0)

        import os
        os.unlink(self.target)

class TestTranscodingFromAnotherWav(TestTranscodingFromWav):
    "Test transcoding from another wav"

    def setUp(self):
        self.source = os.path.join (os.path.dirname(__file__),  "samples/guitar.wav")

class TestTranscodingFromMp3(TestTranscodingFromWav):
    "Test transcoding from mp3"

    def setUp(self):
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")

class TestTranscodingFromFlac(TestTranscodingFromWav):
    "Test transcoding from flac"

    def setUp(self):
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")

class TestTranscodingFromOgg(TestTranscodingFromWav):
    "Test transcoding from ogg"

    def setUp(self):
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")

class TestTranscodingFromMonoWav(TestTranscodingFromWav):
    "Test transcoding from a mono wav"

    def setUp(self):
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep_mono.wav")

class TestTranscodingFrom32kHzWav(TestTranscodingFromWav):
    "Test transcoding from a 32kHz wav"

    def setUp(self):
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep_32000.wav")

class TestTranscodingFromMissingFile(TestTranscodingFromWav):
    "Test transcoding from a missing file"

    def setUp(self):
        self.source = os.path.join (os.path.dirname(__file__),  "samples/unexisting.wav")

    def tearDown(self):
        self.assertRaises(IOError, self.setUpDecoder)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
