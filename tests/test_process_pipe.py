#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author : Thomas Fillon <thomas@parisson.com>

from unit_timeside import unittest, TestRunner
import timeside
from timeside.plugins.decoder.file import FileDecoder
from timeside.core.tools.test_samples import samples


class TestProcessPipe(unittest.TestCase):
    """Test process pipe"""

    def test_Pipe(self):
        """Test process pipe (Quick and dirty)"""
        # TODO clean up and complete

        source = samples["sweep.wav"]

        pipe = timeside.core.processor.ProcessPipe()
        dec = FileDecoder(source)
        pipe.append_processor(dec)
        self.assertRaises(TypeError, pipe.append_processor, object())
        dec2 = FileDecoder(source)
        self.assertRaises(ValueError, pipe.append_processor, dec2)

        odf = timeside.plugins.analyzer.odf.OnsetDetectionFunction()
        odf2 = timeside.plugins.analyzer.odf.OnsetDetectionFunction()

        spectro2 = timeside.plugins.analyzer.spectrogram.Spectrogram()
        pipe2 = (dec | odf | spectro2 | odf2)

        self.assertEqual(pipe2, odf.process_pipe)
        self.assertEqual(pipe2, odf2.process_pipe)
        self.assertEqual(pipe2, spectro2.process_pipe)

        self.assertEqual(len(pipe2.processors), 4)
        # Release temporary buffers in Spectrogram
        for proc in pipe2.processors:
            proc.release()
        #pipe2.draw_graph()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
