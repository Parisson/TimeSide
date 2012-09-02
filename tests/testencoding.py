from math import pi
from numpy import arange, sin, zeros
from unit_timeside import *

from timeside.encoder.gstutils import get_loop_thread

import os.path

class TestEncoding(TestCase):
    "Test the low level streaming features"

    def setUp(self):
        self.channels = 1
        self.samplerate = 44100
        import tempfile
        self.tmpfile = tempfile.NamedTemporaryFile(delete=True)
        self.sink = self.tmpfile.name

    def testWav(self):
        "Test wav encoding"
        from timeside.encoder.wav import WavEncoder
        self.encoder = WavEncoder(self.sink)

    def testVorbis(self):
        "Test vorbis encoding"
        from timeside.encoder.ogg import VorbisEncoder
        self.encoder = VorbisEncoder(self.sink)

    def testMp3(self):
        "Test mp3 encoding"
        from timeside.encoder.mp3 import Mp3Encoder
        self.encoder = Mp3Encoder(self.sink)

    def testAac(self):
        "Test aac encoding"
        from timeside.encoder.m4a import AacEncoder
        self.encoder = AacEncoder(self.sink)

    def testFlac(self):
        "Test flac encoding"
        from timeside.encoder.flac import FlacEncoder
        self.encoder = FlacEncoder(self.sink)

    def testWebm(self):
        "Test webm encoding"
        from timeside.encoder.webm import WebMEncoder
        self.encoder = WebMEncoder(self.sink)

    def tearDown(self):

        self.encoder.setup(channels = self.channels, samplerate = self.samplerate)

        written_frames, eod = 0, False
        total_frames = 3. * self.samplerate
        block_size = 1024
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
            frames = .75 * sin( omega * (arange(write_length) + written_frames) )
            # process encoder, writing to file
            self.encoder.process(frames, eod)
            written_frames += frames.shape[0]
            if eod:
                self.assertEquals(self.encoder.eod, eod)
                break

        self.assertEquals(written_frames, total_frames)
        self.tmpfile.close()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())

