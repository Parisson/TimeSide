#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Thomas fillon <thomas@parisson.com>

from unit_timeside import *
from timeside.decoder import *
from timeside.analyzer.preprocessors import downmix_to_mono, frames_adapter
import numpy as np

BLOCKSIZE = 1024
STEPSIZE = 256

class FakeAnalyzer(object):
    def __init__(self, blocksize=BLOCKSIZE, stepsize=STEPSIZE):
        self.frames = []  # Container for the frame as viewed by process
        self.input_blocksize = blocksize
        self.input_stepsize= stepsize

    def process(self, frames, eod):
        self.frames.append(frames)
        return frames, eod


class TestAnalyzerPreProcessors(unittest.TestCase):

    def tearDown(self):

        analyzer = FakeAnalyzer()

        process_output = []
        for frames, eod in zip(self.input_frames, self.input_eod):
            process_output.append(analyzer.decorated_process(frames, eod))

        output_frames = np.asarray([frames for frames, _ in process_output])
        output_eod = [eod for _, eod in process_output]

        self.assertEqual(self.input_frames.tolist(), output_frames.tolist())
        self.assertEqual(self.input_eod, output_eod)
        self.assertEqual(self.process_frames.tolist(),
                         np.asarray(analyzer.frames).tolist())


class TestDownmixToMono(TestAnalyzerPreProcessors):

    def setUp(self):
        self.decorator = downmix_to_mono
        # Decorate the process
        FakeAnalyzer.decorated_process = self.decorator(FakeAnalyzer.process)

    def test_on_mono(self):
        "Run on stereo, eod = False"
        self.input_frames = np.random.randn(30, 4096)
        self.input_eod = np.repeat(False, 30).tolist()
        self.process_frames = self.input_frames

    def test_on_stereo(self):
        "Run on stereo, eod = False"
        self.input_frames = np.random.randn(30, 4096, 2)
        self.input_eod = np.repeat(False, 30).tolist()
        self.process_frames = self.input_frames.mean(axis=-1)

    def test_on_multichannel(self):
        "Run on multi-channel, eod = False"
        self.input_frames = np.random.randn(30, 4096, 6)
        self.input_eod = np.repeat(False, 30).tolist()
        self.process_frames = self.input_frames.mean(axis=-1)

    def test_on_mono_eod_true(self):
        "Run on mono, last eod = True"
        self.input_frames = np.random.randn(30, 4096)
        self.input_eod = np.repeat(False, 30).tolist()
        self.input_eod[-1] = True
        self.process_frames = self.input_frames

    def test_on_stereo_eod_true(self):
        "Run on stereo, last eod = True"
        self.input_frames = np.random.randn(30, 4096, 2)
        self.input_eod = np.repeat(False, 30).tolist()
        self.input_eod[-1] = True
        self.process_frames = self.input_frames.mean(axis=-1)

    def test_on_multichannel_eod_true(self):
        "Run on multi-channel, last eod = True"
        self.input_frames = np.random.randn(30, 4096, 6)
        self.input_eod = np.repeat(False, 30).tolist()
        self.input_eod[-1] = True
        self.process_frames = self.input_frames.mean(axis=-1)

class TestFramesAdapter(TestAnalyzerPreProcessors, unittest.TestCase):

    def setUp(self):
        self.decorator = frames_adapter
        # Decorate the process
        FakeAnalyzer.decorated_process = self.decorator(FakeAnalyzer.process)

    def test_on_mono(self):
        "Run on mono"
        self.input_frames = np.arange(0, 2500).reshape(5, -1)
        self.input_eod = [False, False, False, False, False]

        self.process_frames = np.asarray([range(0, 1024),
                                          range(256, 1280),
                                          range(512, 1536),
                                          range(768, 1792),
                                          range(1024, 2048),
                                          range(1280, 2304)])

    def test_on_stereo(self):
        "Run on stereo"
        self.input_frames = np.arange(0, 5000).reshape(5, -1, 2)
        self.input_eod = [False, False, False, False, False]

        self.process_frames = np.asarray([np.arange(0, 2048).reshape(-1, 2),
                                          np.arange(512, 2560).reshape(-1, 2),
                                          np.arange(1024, 3072).reshape(-1, 2),
                                          np.arange(1536, 3584).reshape(-1, 2),
                                          np.arange(2048, 4096).reshape(-1, 2),
                                          np.arange(2560, 4608).reshape(-1, 2)])
    def test_on_mono_eod_true(self):
        "Run on mono, last eod = True"
        self.input_frames = np.arange(0, 2500).reshape(5, -1)
        self.input_eod = [False, False, False, False, True]
        last_frames = range(1536, 2500)
        last_frames.extend([0]*60)
        self.process_frames = np.asarray([range(0, 1024),
                                          range(256, 1280),
                                          range(512, 1536),
                                          range(768, 1792),
                                          range(1024, 2048),
                                          range(1280, 2304),
                                          last_frames])

    def test_on_stereo_eod_true(self):
        "Run on stereo, last eod = True"
        self.input_frames = np.arange(0, 5000).reshape(5, -1, 2)
        self.input_eod = [False, False, False, False, True]
        last_frames = np.hstack([np.arange(3072, 5000),
                                 np.zeros((120,))]).reshape(-1, 2)
        self.process_frames = np.asarray([np.arange(0, 2048).reshape(-1, 2),
                                          np.arange(512, 2560).reshape(-1, 2),
                                          np.arange(1024, 3072).reshape(-1, 2),
                                          np.arange(1536, 3584).reshape(-1, 2),
                                          np.arange(2048, 4096).reshape(-1, 2),
                                          np.arange(2560, 4608).reshape(-1, 2),
                                          last_frames])

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
