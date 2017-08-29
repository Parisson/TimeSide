#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Thomas fillon <thomas@parisson.com>

from unit_timeside import unittest, TestRunner
from timeside.core.preprocessors import downmix_to_mono, frames_adapter
import numpy as np
from numpy.testing import assert_array_equal


class FakeAnalyzer(object):

    def __init__(self, blocksize=1024, stepsize=512):
        self.frames = []  # Container for the frame as viewed by process
        self.input_blocksize = blocksize
        self.input_stepsize = stepsize

    def process(self, frames, eod):
        self.frames.append(frames)
        return frames, eod

    @staticmethod
    def id():
        return 'fake_analyzer'


def get_frames(signal, blocksize=2048, stepsize=None, zeropad=False):
    if stepsize is None:
        stepsize = blocksize
    if stepsize > blocksize:
        raise ValueError('Stepsize must be lower or equal to blocksize')
    start = 0
    signal_length = len(signal)
    eod = False
    while not eod:
        end = start + blocksize
        eod = end >= signal_length
        if eod & zeropad:
            new_shape = list(signal.shape)
            new_shape[0] = blocksize
            frame = signal[start:end].copy()
            frame.resize(tuple(new_shape))
            yield frame, eod
        else:
            yield signal[start:end], eod
        start += stepsize

def assertEqualListOfArrays(list1, list2):
    for ar1, ar2 in zip(list1, list2):
        assert_array_equal(ar1, ar2)
    

class TestAnalyzerPreProcessors(unittest.TestCase):


                
    def tearDown(self):

        analyzer = FakeAnalyzer(blocksize=self.blocksize,
                                stepsize=self.stepsize)
        
        input_frames_eod = [(frames, eod) for frames, eod
                            in get_frames(signal=self.input_signal)]
        input_frames, input_eod = zip(*input_frames_eod)

        process_output = []
        for frames, eod in input_frames_eod:
            process_output.append(analyzer.decorated_process(frames, eod))
        output_frames, output_eod = zip(*process_output)

        # Check incoming frames = outgoing frames outside the process
        self.assertTupleEqual(input_frames, output_frames)
        self.assertTupleEqual(input_eod, output_eod)
        # Check frames at process level
        assertEqualListOfArrays(list(self.process_frames),
                                analyzer.frames)

class TestDownmixToMono(TestAnalyzerPreProcessors):

    def setUp(self):
        self.decorator = downmix_to_mono
        # Decorate the process
        FakeAnalyzer.decorated_process = self.decorator(FakeAnalyzer.process)
        self.blocksize = 1024
        self.stepsize = 256

    def test_on_mono(self):
        "Run on mono"
        self.input_signal = np.random.randn(2*44100,)
        self.process_signal = self.input_signal
        process_frames_eod = [(frames, eod) for frames, eod
                              in get_frames(signal=self.input_signal)]
        self.process_frames, process_eod = zip(*process_frames_eod)

    def test_on_stereo(self):
        "Run on stereo"
        self.input_signal = np.random.randn(3*44100, 2)

        self.process_signal = self.input_signal.mean(axis=1)
        process_frames_eod = [(frames, eod) for frames, eod
                              in get_frames(signal=self.process_signal)]
        self.process_frames, process_eod = zip(*process_frames_eod)

    def test_on_multichannel(self):
        "Run on multi-channel"
        self.input_signal = np.random.randn(2*44100, 5)
        self.process_signal = self.input_signal.mean(axis=1)
        process_frames_eod = [(frames, eod) for frames, eod
                              in get_frames(signal=self.process_signal)]
        self.process_frames, process_eod = zip(*process_frames_eod)
        

class TestFramesAdapter(TestAnalyzerPreProcessors, unittest.TestCase):

    def setUp(self):
        self.decorator = frames_adapter
        # Decorate the process
        FakeAnalyzer.decorated_process = self.decorator(FakeAnalyzer.process)
        self.blocksize = 1024
        self.stepsize = 256
        
    def test_on_mono(self):
        "Run on mono"
        self.input_signal = np.random.randn(2500,)
        process_frames_eod = [(frames, eod) for frames, eod
                              in get_frames(signal=self.input_signal,
                                            blocksize=self.blocksize,
                                            stepsize=self.stepsize,
                                            zeropad=True)]
        self.process_frames, process_eod = zip(*process_frames_eod)
        

    def test_on_stereo(self):
        "Run on stereo"
        self.input_signal = np.random.randn(2500,2)
        
        process_frames_eod = [(frames, eod) for frames, eod
                              in get_frames(signal=self.input_signal,
                                            blocksize=self.blocksize,
                                            stepsize=self.stepsize,
                                            zeropad=True)]
        self.process_frames, process_eod = zip(*process_frames_eod)
        
    def test_on_stereo_4096(self):
        "Run on stereo, blocksize=4096"
        self.blocksize = 4096
        self.stepsize = 4096
        self.input_signal = np.random.randn(20*4096,2)
        process_frames_eod = [(frames, eod) for frames, eod
                              in get_frames(signal=self.input_signal,
                                            blocksize=self.blocksize,
                                            stepsize=self.stepsize,
                                            zeropad=True)]
        self.process_frames, process_eod = zip(*process_frames_eod)
 
        
if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
