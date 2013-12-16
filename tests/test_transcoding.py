#! /usr/bin/env python

from __future__ import division

from timeside.core import *
from timeside.decoder import *
from timeside.analyzer import *
from timeside.encoder import *
from timeside.component import *

from unit_timeside import *
from tools import tmp_file_sink
import os.path


class TestTranscodingFromWav(unittest.TestCase):
    "Test transcoding from wav"

    def setUp(self):
        self.source = os.path.join(os.path.dirname(__file__),
                                   "samples/sweep.wav")
        self.test_duration = True
        self.test_channels = True

    def testWav(self):
        "Test conversion to wav"
        self.encoder_function = WavEncoder

    def testMp3(self):
        "Test conversion to mp3"
        self.encoder_function = Mp3Encoder

    def testOgg(self):
        "Test conversion to ogg"
        self.encoder_function = VorbisEncoder

    def testWebM(self):
        "Test conversion to webm"
        self.encoder_function = WebMEncoder
        self.test_duration = False  # webmmux encoder with streamable=true
                                    # does not return a valid duration

    def testM4a(self):
        "Test conversion to m4a"
        self.encoder_function = AacEncoder

    def tearDown(self):
        decoder = FileDecoder(self.source)



        file_extension = '.' + self.encoder_function.file_extension()

        self.target = tmp_file_sink(prefix=self.__class__.__name__,
                                  suffix=file_extension)
        encoder = self.encoder_function(self.target)
        (decoder | encoder).run()

        decoder_encoded = FileDecoder(self.target)

        from timeside.analyzer import Waveform
        a = Waveform()  # Arbitrary analyzer for running the next pipe
        (decoder_encoded | a).run()

        import os
        os.unlink(self.target)

        #print decoder.channels(), decoder.samplerate(), written_frames
        #print media_channels

        if self.test_channels:
            self.assertEqual(decoder.channels(), decoder_encoded.channels())
        else:
            self.assertEqual(2, decoder_encoded.channels())  # voaacenc bug ?

        self.assertEqual(decoder.samplerate(),
                         decoder_encoded.samplerate())

        if self.test_duration:
            self.assertAlmostEqual(decoder.input_duration,
                                   decoder_encoded.input_duration,
                                   delta=0.2)

class TestTranscodingFromMonoWav(TestTranscodingFromWav):
    "Test transcoding from a mono wav"

    def setUp(self):
        super(TestTranscodingFromMonoWav, self).setUp()
        self.source = os.path.join(os.path.dirname(__file__),
                                   "samples/sweep_mono.wav")

    def testM4a(self):
        "Test conversion to m4a"
        super(TestTranscodingFromMonoWav, self).testM4a()
        self.test_channels = False  # voaacenc bug ? : always encode stereo


class TestTranscodingFromAnotherWav(TestTranscodingFromMonoWav):
    "Test transcoding from another wav"

    def setUp(self):
        super(TestTranscodingFromAnotherWav, self).setUp()
        self.source = os.path.join(os.path.dirname(__file__),
                                   "samples/guitar.wav")  # Mono


class TestTranscodingFromMp3(TestTranscodingFromWav):
    "Test transcoding from mp3"

    def setUp(self):
        super(TestTranscodingFromMp3, self).setUp()
        self.source = os.path.join(os.path.dirname(__file__),
                                   "samples/sweep.mp3")


class TestTranscodingFromFlac(TestTranscodingFromWav):
    "Test transcoding from flac"

    def setUp(self):
        super(TestTranscodingFromFlac, self).setUp()
        self.source = os.path.join(os.path.dirname(__file__),
                                   "samples/sweep.flac")


class TestTranscodingFromOgg(TestTranscodingFromWav):
    "Test transcoding from ogg"

    def setUp(self):
        super(TestTranscodingFromOgg, self).setUp()
        self.source = os.path.join(os.path.dirname(__file__),
                                   "samples/sweep.ogg")





class TestTranscodingFrom32kHzWav(TestTranscodingFromWav):
    "Test transcoding from a 32kHz wav"

    def setUp(self):
        super(TestTranscodingFrom32kHzWav, self).setUp()
        self.source = os.path.join(os.path.dirname(__file__),
                                   "samples/sweep_32000.wav")


class TestTranscodingFromMissingFile(TestTranscodingFromWav):
    "Test transcoding from a missing file"

    def setUp(self):
        self.source = os.path.join(os.path.dirname(__file__),
                                   "samples/unexisting.wav")

    def tearDown(self):
        decoder = FileDecoder
        self.assertRaises(IOError, decoder, self.source)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
