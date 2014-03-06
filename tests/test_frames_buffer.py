#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
from timeside.decoder.utils import frames_buffer
import numpy as np

from numpy.testing import assert_array_equal


class Test_frames_buffer(unittest.TestCase):
    "Test frames_buffer class from decoder.utils"
    def setUp(self):
        self.blocksize = 1024
        self.channels = 1
        self.data_size = 5000

    def testScenario(self):
        "perform test scenario on frames_buffer"
        #gst_block =
        data = np.arange(self.data_size, dtype='float32')
        data = data.reshape((-1, self.channels))

        f_buf = frames_buffer(self.blocksize, self.channels)

        self.assertEqual(f_buf.current(), 0)
        self.assertEqual(f_buf._empty, self.blocksize)
        #self.assertEqual(f_buf._buffer, np.zeros((self.blocksize, self.channels)))
        frames = f_buf.append(data[0:256])

        self.assertEqual(f_buf.current(), 256)
        self.assertEqual(f_buf.current(), 256)
        self.assertEqual(frames, [])

        assert_array_equal(f_buf._buffer[0:256], data[0:256])

        frames = f_buf.append(data[256:512])
        self.assertEqual(f_buf.current(), 512)
        self.assertEqual(frames, [])
        assert_array_equal(f_buf._buffer[0:512], data[0:512])

        frames = f_buf.append(data[512:1024])
        self.assertEqual(f_buf.current(), 0)
        assert_array_equal(frames, [data[0:1024]])

        frames = f_buf.append(data[1024:2040])
        self.assertEqual(f_buf.current(), 1016)
        self.assertEqual(frames, [])

        frames = f_buf.append(data[2040:4000])
        self.assertEqual(f_buf.current(), 928)
        assert_array_equal(frames,
                           [data[1024:2048], data[2048:3072]])

        frames = f_buf.append(data[4000:4000])
        self.assertEqual(frames, [])

        frames = f_buf.append(data[4000:5000])
        assert_array_equal(frames, [data[3072:4096]])
        assert_array_equal(f_buf.flush(), data[4096:5000])

    def testScenarioStereo(self):
        "perform test scenario on frames_buffer Stereo"
        self.channels = 2
        self.data_size = 5000*2
        self.testScenario()


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
