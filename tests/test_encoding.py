#! /usr/bin/env python

from __future__ import division

from math import pi
import numpy as np
from unit_timeside import *
from timeside.plugins.decoder.utils import get_uri, get_media_uri_info
from timeside.plugins.decoder.array import ArrayDecoder
import os
from tools import tmp_file_sink


class TestEncoding(unittest.TestCase):
    "Test encoding features"

    def generate_source(self):
        self.expected_total_frames = np.ceil(self.source_duration * self.samplerate).astype(np.int)

        f0 = 440.
        f = f0 * np.logspace(0, 4 / 12 * (self.channels - 1), self.channels, base=2)
        omega = 2. * pi * f / self.samplerate
        samples = np.empty((self.expected_total_frames, self.channels))
        for n in range(self.channels):
            samples[:, n] = .75 * np.sin(omega[n] *
                                         np.arange(self.expected_total_frames))
        return samples

    def setUp(self):
        self.samplerate, self.channels, self.blocksize = 44100, 1, 1024
        self.overwrite = False
        self.encode_to_file = True
        self.test_duration = True
        self.test_channels = True

        # Source
        self.source_duration = 10.

    def testWav(self):
        "Test wav encoding"
        from timeside.plugins.encoder.wav import WavEncoder
        self.encoder_function = WavEncoder
        self.delta = 0

    def testVorbis(self):
        "Test vorbis encoding"
        from timeside.plugins.encoder.ogg import VorbisEncoder
        self.encoder_function = VorbisEncoder
        self.delta = 0.3

    def testMp3(self):
        "Test mp3 encoding"
        from timeside.plugins.encoder.mp3 import Mp3Encoder
        self.encoder_function = Mp3Encoder
        self.delta = 0.2

    def testAac(self):
        "Test aac encoding"
        from timeside.plugins.encoder.m4a import AacEncoder
        self.encoder_function = AacEncoder
        self.test_channels = False
        self.delta = 0.3

    def testFlac(self):
        "Test flac encoding"
        from timeside.plugins.encoder.flac import FlacEncoder
        self.encoder_function = FlacEncoder
        self.delta = 0

    def testWebM(self):
        "Test webm encoding, audio only"
        from timeside.plugins.encoder.webm import WebMEncoder
        self.encoder_function = WebMEncoder
        self.test_duration = False  # webmmux encoder with streamable=true
        # does not return a valid duration

    def testWebMVideo(self):
        "Test webm encoding, video"
        from timeside.plugins.encoder.webm import WebMEncoder
        self.encoder_function = WebMEncoder
        self.test_duration = False  # webmmux encoder with streamable=true
        # does not return a valid duration
        if not hasattr(self, 'sink'):
            file_extension = '.' + self.encoder_function.file_extension()
            self.sink = tmp_file_sink(prefix=self.__class__.__name__,
                                      suffix=file_extension)
            self.encoder = self.encoder_function(self.sink,
                                                 overwrite=self.overwrite,
                                                 video=True)

    def testOpus(self):
        "Test opus encoding"
        from timeside.plugins.encoder.opus import OpusEncoder
        self.encoder_function = OpusEncoder
        self.delta = 0.1
        self.samplerate = 48000  # 44100 is not supported by opusenc

    def testWavAubio(self):
        "Test aubio wav encoding"
        from timeside.plugins.encoder.aubio_wav import WavEncoder
        self.encoder_function = WavEncoder
        self.delta = 0

    def testFlacAubio(self):
        "Test flac encoding with aubio"
        from timeside.plugins.encoder.aubio_flac import FlacEncoder
        self.encoder_function = FlacEncoder
        self.delta = 0.1
        self.samplerate = 44100

    def testVorbisAubio(self):
        "Test vorbis encoding with aubio"
        from timeside.plugins.encoder.aubio_ogg import VorbisEncoder
        self.encoder_function = VorbisEncoder
        self.delta = 0.3

    def tearDown(self):

        # Source through ArrayDecoder

        decoder = ArrayDecoder(self.generate_source(),
                               samplerate=self.samplerate)
        # Encoder
        if not hasattr(self, 'sink'):
            file_extension = '.' + self.encoder_function.file_extension()
            self.sink = tmp_file_sink(prefix=self.__class__.__name__,
                                      suffix=file_extension)

        if not hasattr(self, 'encoder'):
            self.encoder = self.encoder_function(self.sink,
                                                 overwrite=self.overwrite)

        # Run Pipe
        (decoder | self.encoder).run()

        if self.encode_to_file:
            media_info = get_media_uri_info(get_uri(self.sink))
            media_duration = media_info['duration']
            media_channels = media_info['streams'][0]['channels']
            media_samplerate = media_info['streams'][0]['samplerate']

            os.unlink(self.sink)

            if self.test_duration:
                self.assertAlmostEqual(self.source_duration,
                                       media_duration,
                                       delta=self.delta)
            if self.test_channels:
                self.assertEqual(self.channels, media_channels)
            else:
                self.assertEqual(2, media_channels)   # voaacenc bug ?
            self.assertEqual(media_samplerate, self.samplerate)

        if 0:
            import commands
            print(commands.getoutput('sndfile-info ' + self.sink))

        self.assertEqual(self.expected_total_frames, self.encoder.num_samples)
        self.assertEqual(self.channels, self.encoder.channels())
        self.assertEqual(self.samplerate, self.encoder.samplerate())
        self.assertEqual(self.source_duration,
                         self.encoder.num_samples / self.encoder.samplerate())



if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
