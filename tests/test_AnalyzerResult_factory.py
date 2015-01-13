#! /usr/bin/env python
from __future__ import division

from unit_timeside import unittest, TestRunner
from timeside.core.analyzer import AnalyzerResult
import numpy as np


class TestAnalyzerResult_factory(unittest.TestCase):
    """ test AnalyzerResult factory"""

    def setUp(self):
        pass

    def test_factory(self):
        time_mode_list = ['global', 'event', 'segment', 'framewise']
        data_mode_list = ['value', 'label']

        for time_mode in time_mode_list:
            for data_mode in data_mode_list:
                result = AnalyzerResult(data_mode, time_mode)
                self.assertEqual(result.data_mode, data_mode)
                self.assertEqual(result.time_mode, time_mode)
                self.assertEqual(result.keys(), ['id_metadata',
                                                 'data_object',
                                                 'audio_metadata',
                                                 'parameters'])


class TestAnalyzerResult_classes(unittest.TestCase):
    """ test AnalyzerResult factory for all AnalyzerResult classes"""

    def test_GlobalValueResult(self):
        "Data structure for Global & Value Result"
        self.time_mode = 'global'
        self.data_mode = 'value'
        self.data_object_keys = ['value', 'y_value']

    def test_GlobalLabelResult(self):
        "Data structure for Global & Label Result"
        self.time_mode = 'global'
        self.data_mode = 'label'
        self.data_object_keys = ['label', 'label_metadata']

    def test_FrameValueResult(self):
        "Data structure for Framewise & Value Result"
        self.time_mode = 'framewise'
        self.data_mode = 'value'
        self.data_object_keys = ['value', 'y_value',
                                 'frame_metadata']

    def test_FrameLabelResult(self):
        "Data structure for Framewise & Label Result"
        self.time_mode = 'framewise'
        self.data_mode = 'label'
        self.data_object_keys = ['label', 'label_metadata', 'frame_metadata']

    def test_EventValueResult(self):
        "Data structure for Event & Value Result"
        self.time_mode = 'event'
        self.data_mode = 'value'
        self.data_object_keys = ['value', 'y_value', 'time']

    def test_EventLabelResult(self):
        "Data structure for Event & Label Result"
        self.time_mode = 'event'
        self.data_mode = 'label'
        self.data_object_keys = ['label', 'label_metadata', 'time']

    def test_SegmentValueResult(self):
        "Data structure for Segment & Value Result"
        self.time_mode = 'segment'
        self.data_mode = 'value'
        self.data_object_keys = ['value', 'y_value',
                                 'time', 'duration']

    def test_SegmentLabelResult(self):
        "Data structure for Segment & Label Result"
        self.time_mode = 'segment'
        self.data_mode = 'label'
        self.data_object_keys = ['label', 'label_metadata', 'time', 'duration']

    def tearDown(self):
        result = AnalyzerResult(self.data_mode, self.time_mode)
        self.assertEqual(self.data_object_keys, result.data_object.keys())


class TestAnalyzerResult_Data_Methods(unittest.TestCase):
    """ test AnalyzerResult factory for all AnalyzerResult classes"""

    def test_GlobalValueResult(self):
        "Data methods for Global & Value Result"
        self.time_mode = 'global'
        self.data_mode = 'value'
        self.result = AnalyzerResult(self.data_mode, self.time_mode)
        # Audio
        self.audio_start = np.random.rand(1) * 50
        self.audio_duration = np.random.rand(1) * 500
        # Expected data
        self.data = np.random.rand(1)
        self.time = 0
        self.duration = self.audio_duration
        # Set data in result
        self.result.data_object.value = self.data
        self.result.audio_metadata.start = self.audio_start
        self.result.audio_metadata.duration = self.audio_duration

    def test_GlobalLabelResult(self):
        "Data methods for Global & Label Result"
        self.time_mode = 'global'
        self.data_mode = 'label'
        self.result = AnalyzerResult(self.data_mode, self.time_mode)
        # Audio
        self.audio_start = np.random.rand(1) * 50
        self.audio_duration = np.random.rand(1) * 500
        # Expected data
        self.data = np.random.randint(10)
        self.time = 0
        self.duration = self.audio_duration
        # Set data in result
        self.result.data_object.label = self.data
        self.result.audio_metadata.start = self.audio_start
        self.result.audio_metadata.duration = self.audio_duration

    def test_FrameValueResult(self):
        "Data methods for Framewise & Value Result"
        self.time_mode = 'framewise'
        self.data_mode = 'value'
        self.result = AnalyzerResult(self.data_mode, self.time_mode)
        # Audio
        self.audio_start = np.random.rand(1) * 50
        # Expected data
        nb_frames = 200
        blocksize = 1024
        stepsize = 512
        samplerate = 44100
        self.data = np.random.rand(nb_frames, 1)
        self.duration = blocksize / samplerate * np.ones(nb_frames)
        self.time = np.arange(0, nb_frames*stepsize, stepsize) / samplerate
        # Set data in result
        self.result.data_object.value = self.data
        self.result.data_object.frame_metadata.blocksize = blocksize
        self.result.data_object.frame_metadata.stepsize = stepsize
        self.result.data_object.frame_metadata.samplerate = samplerate
        self.result.audio_metadata.start = self.audio_start

    def test_FrameLabelResult(self):
        "Data methods for Framewise & Label Result"
        self.time_mode = 'framewise'
        self.data_mode = 'label'
        self.result = AnalyzerResult(self.data_mode, self.time_mode)
        # Audio
        self.audio_start = np.random.rand(1) * 50
        # Expected data
        nb_frames = 200
        blocksize = 1024
        stepsize = 512
        samplerate = 44100
        self.data = np.random.randint(10, size=nb_frames)
        self.duration = blocksize / samplerate * np.ones(nb_frames)
        self.time = np.arange(0, nb_frames*stepsize, stepsize) / samplerate
        # Set data in result
        self.result.data_object.label = self.data
        self.result.data_object.frame_metadata.blocksize = blocksize
        self.result.data_object.frame_metadata.stepsize = stepsize
        self.result.data_object.frame_metadata.samplerate = samplerate
        self.result.audio_metadata.start = self.audio_start

    def test_EventValueResult(self):
        "Data methods for Event & Value Result"
        self.time_mode = 'event'
        self.data_mode = 'value'
        self.result = AnalyzerResult(self.data_mode, self.time_mode)
        # Audio
        self.audio_start = np.random.rand(1) * 50
        # Expected data
        nb_val = 200
        self.data = np.random.randn(nb_val, 4)
        self.time = np.random.rand(1, nb_val) * 500
        self.duration = np.zeros(nb_val)
        # Set data in result
        self.result.data_object.value = self.data
        self.result.data_object.time = self.time
        self.result.audio_metadata.start = self.audio_start

    def test_EventLabelResult(self):
        "Data methods for Event & Label Result"
        self.time_mode = 'event'
        self.data_mode = 'label'
        self.result = AnalyzerResult(self.data_mode, self.time_mode)
        # Audio
        self.audio_start = np.random.rand(1) * 50
        # Expected data
        nb_val = 200
        self.data = np.random.randint(10, size=nb_val)
        self.time = np.random.rand(1, nb_val) * 500
        self.duration = np.zeros(nb_val)
        # Set data in result
        self.result.data_object.label = self.data
        self.result.data_object.time = self.time
        self.result.audio_metadata.start = self.audio_start

    def test_SegmentValueResult(self):
        "Data methods for Segment & Value Result"
        self.time_mode = 'segment'
        self.data_mode = 'value'
        self.result = AnalyzerResult(self.data_mode, self.time_mode)
        # Audio
        self.audio_start = np.random.rand(1) * 50
        # Expected data
        nb_val = 200
        self.data = np.random.randn(nb_val, 4)
        self.time = np.random.rand(1, nb_val) * 500
        self.duration = np.random.rand(1, nb_val) * 50
        # Set data in result
        self.result.data_object.value = self.data
        self.result.data_object.time = self.time
        self.result.data_object.duration = self.duration
        self.result.audio_metadata.start = self.audio_start
        self.result.audio_metadata.duration = self.duration

    def test_SegmentLabelResult(self):
        "Data methods for Segment & Label Result"
        self.time_mode = 'segment'
        self.data_mode = 'label'
        self.result = AnalyzerResult(self.data_mode, self.time_mode)
        # Audio
        self.audio_start = np.random.rand(1) * 50
        # Expected data
        nb_val = 200
        self.data = np.random.randint(10, size=nb_val)
        self.time = np.random.rand(1, nb_val) * 500
        self.duration = np.random.rand(1, nb_val) * 50
        # Set data in result
        self.result.data_object.label = self.data
        self.result.data_object.time = self.time
        self.result.data_object.duration = self.duration
        self.result.audio_metadata.start = self.audio_start

    def tearDown(self):
        np.testing.assert_array_equal(self.result.data, self.data)
        np.testing.assert_array_equal(self.result.time,
                                      self.time + self.audio_start)
        np.testing.assert_array_equal(self.result.duration, self.duration)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
