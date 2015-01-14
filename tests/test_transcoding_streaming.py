#! /usr/bin/env python

from __future__ import division

from timeside.core.processor import get_processor, ProcessPipe
from timeside.plugins.decoder.file import FileDecoder

from unit_timeside import unittest, TestRunner
from tools import tmp_file_sink
from timeside.core.tools.test_samples import samples


class TestTranscodingStreaming(unittest.TestCase):
    "Test transcoding and streaming"

    def setUp(self):
        self.source = samples["sweep.wav"]
        self.test_duration = True
        self.test_channels = True
        self.filesize_delta = None
        self.expected_sample_rate = None

    def testMp3(self):
        "Test conversion to mp3"
        self.encoder_id = 'mp3_encoder'
        self.filesize_delta = 156

    def testOgg(self):
        "Test conversion to ogg"
        self.encoder_id = 'vorbis_encoder'

    def testOpus(self):
        "Test conversion to opus"
        self.encoder_id = 'opus_encoder'
        self.expected_sample_rate = 48000

    def testWebM(self):
        "Test conversion to webm"
        self.encoder_id = 'webm_encoder'
        self.test_duration = False  # webmmux encoder with streamable=true
                                    # does not return a valid duration

    def tearDown(self):
        decoder = FileDecoder(self.source)
        encoder_cls = get_processor(self.encoder_id)

        file_extension = '.' + encoder_cls.file_extension()

        self.target_filesink = tmp_file_sink(prefix=self.__class__.__name__,
                                             suffix=file_extension)

        self.target_appsink = tmp_file_sink(prefix=self.__class__.__name__,
                                            suffix=file_extension)

        encoder = encoder_cls(self.target_filesink, streaming=True)
        pipe = (decoder | encoder)

        with open(self.target_appsink, 'w') as f:
            for chunk in pipe.stream():
                f.write(chunk)

        decoder_encoded = FileDecoder(self.target_filesink)

        pipe2 = ProcessPipe(decoder_encoded)
        pipe2.run()

        import os
        filesink_size = os.path.getsize(self.target_filesink)
        appsink_size = os.path.getsize(self.target_appsink)

        os.unlink(self.target_filesink)
        os.unlink(self.target_appsink)
        #print decoder.channels(), decoder.samplerate(), written_frames
        #print media_channels

        if self.test_channels:
            self.assertEqual(decoder.channels(), decoder_encoded.channels())
        else:
            self.assertEqual(2, decoder_encoded.channels())  # voaacenc bug ?

        if not self.expected_sample_rate:
            self.expected_sample_rate = decoder.samplerate()
        self.assertEqual(self.expected_sample_rate,
                         decoder_encoded.samplerate())

        if self.test_duration:
            self.assertAlmostEqual(decoder.input_duration,
                                   decoder_encoded.input_duration,
                                   delta=0.2)
        self.assertAlmostEqual(filesink_size, appsink_size,
                               delta=self.filesize_delta)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
