#! /usr/bin/env python

from timeside.plugins.decoder.file import FileDecoder
from unit_timeside import unittest, TestRunner
from timeside.core.tools.test_samples import samples

import tempfile
import os.path

__all__ = ['TestGraphing']


class TestGraphing(unittest.TestCase):

    "Test all graphers with WAV input media format"

    def setUp(self):
        pass

    # WAVEFORMS
    def testWav2Waveform(self):
        "Test WAV to Waveform"
        from timeside.plugins.grapher.waveform_simple import Waveform
        self.source = samples["sweep.wav"]
        self.image = tempfile.NamedTemporaryFile(suffix="waveform.png",
                                                 delete=True)
        self.grapher = Waveform(width=1024, height=256,
                                bg_color=(255, 255, 255),
                                color_scheme='default')

    # WAVEFORM CENTROID
    def testWav2WaveformCentroid(self):
        "Test WAV to WaveformCentroid"
        from timeside.plugins.grapher.waveform_centroid import WaveformCentroid
        self.source = samples["sweep.wav"]
        self.image = tempfile.NamedTemporaryFile(suffix="waveform_centr.png",
                                                 delete=True)
        self.grapher = WaveformCentroid(width=1024, height=256,
                                        bg_color=(0, 0, 0),
                                        color_scheme='default')

    # WAVEFORMS TRANSPARENT
    def testWav2WaveformTransparent(self):
        "Test WAV to WaveformTransparent"
        from timeside.plugins.grapher.waveform_transparent import WaveformTransparent
        self.source = samples["sweep.wav"]
        self.image = tempfile.NamedTemporaryFile(suffix="waveform_trans.png",
                                                 delete=True)
        self.grapher = WaveformTransparent(width=1024, height=256,
                                           bg_color=None,
                                           color_scheme='default')

    # WAVEFORMS CONTOUR BLACK
    def testWav2WaveformContourBlack(self):
        "Test WAV to WaveformContourBlack"
        from timeside.plugins.grapher.waveform_contour import WaveformContourBlack
        self.source = samples["sweep.wav"]
        self.image = tempfile.NamedTemporaryFile(suffix="waveform_cont_bk.png",
                                                 delete=True)
        self.grapher = WaveformContourBlack(
            width=1024, height=256, bg_color=(0, 0, 0), color_scheme='default')

    # WAVEFORMS CONTOUR WHITE
    def testWav2WaveformContourWhite(self):
        "Test WAV to WaveformContourWhite"
        from timeside.plugins.grapher.waveform_contour import WaveformContourWhite
        self.source = samples["sweep.wav"]
        self.image = tempfile.NamedTemporaryFile(suffix="waveform_cont_wh.png",
                                                 delete=True)
        self.grapher = WaveformContourWhite(width=1024, height=256,
                                            bg_color=(255, 255, 255),
                                            color_scheme='default')

    # LOG SPECTROGRAMS
    def testWav2SpectrogramLog(self):
        "Test WAV to Spectrogram"
        from timeside.plugins.grapher.spectrogram_log import SpectrogramLog
        self.source = samples["sweep.wav"]
        self.image = tempfile.NamedTemporaryFile(suffix="spectrogram_log.png",
                                                 delete=True)
        self.grapher = SpectrogramLog(width=1024, height=256,
                                      bg_color=(0, 0, 0),
                                      color_scheme='default')

    # LIN SPECTROGRAMS
    def testWav2SpectrogramLin(self):
        "Test WAV to SpectrogramLinear"
        from timeside.plugins.grapher.spectrogram_lin import SpectrogramLinear
        self.source = samples["sweep.wav"]
        self.image = tempfile.NamedTemporaryFile(suffix="spectrogram_lin.png",
                                                 delete=True)
        self.grapher = SpectrogramLinear(width=1024, height=256,
                                         bg_color=(0, 0, 0),
                                         color_scheme='default')

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.grapher).run()
        self.grapher.render(self.image)
        self.assertGreater(os.path.getsize(self.image.name), 0)
        self.image.close()

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
