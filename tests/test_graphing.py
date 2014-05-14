#! /usr/bin/env python

from timeside.decoder.file import FileDecoder
from unit_timeside import *

import os.path

__all__ = ['TestGraphing']


class TestGraphing(unittest.TestCase):
    "Test all graphers with WAV input media format"

    def setUp(self):
        pass

    # WAVEFORMS
    def testWav2Waveform(self):
        "Test WAV to Waveform"
        from timeside.grapher.waveform_simple import Waveform
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_sweep_wav.png"
        self.grapher = Waveform(width=1024, height=256, bg_color=(255,255,255), color_scheme='default')

    # WAVEFORM CENTROID
    def testWav2WaveformCentroid(self):
        "Test WAV to WaveformCentroid"
        from timeside.grapher.waveform_centroid import WaveformCentroid
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_centroid_sweep_wav.png"
        self.grapher = WaveformCentroid(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    # WAVEFORMS TRANSPARENT
    def testWav2WaveformTransparent(self):
        "Test WAV to WaveformTransparent"
        from timeside.grapher.waveform_transparent import WaveformTransparent
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_transparent_sweep_wav.png"
        self.grapher = WaveformTransparent(width=1024, height=256, bg_color=None, color_scheme='default')

    # WAVEFORMS CONTOUR BLACK
    def testWav2WaveformContourBlack(self):
        "Test WAV to WaveformContourBlack"
        from timeside.grapher.waveform_contour import WaveformContourBlack
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_contour_bk_sweep_wav.png"
        self.grapher = WaveformContourBlack(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    # WAVEFORMS CONTOUR WHITE
    def testWav2WaveformContourWhite(self):
        "Test WAV to WaveformContourWhite"
        from timeside.grapher.waveform_contour import WaveformContourWhite
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_contour_wh_sweep_wav.png"
        self.grapher = WaveformContourWhite(width=1024, height=256, bg_color=(255,255,255), color_scheme='default')

    # LOG SPECTROGRAMS
    def testWav2Spectrogram(self):
        "Test WAV to Spectrogram"
        from timeside.grapher.spectrogram_log import SpectrogramLog
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_spectrogram_log_sweep_wav.png"
        self.grapher = SpectrogramLog(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    # LIN SPECTROGRAMS
    def testWav2Spectrogram(self):
        "Test WAV to SpectrogramLinear"
        from timeside.grapher.spectrogram_lin import SpectrogramLinear
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_spectrogram_lin_sweep_wav.png"
        self.grapher = SpectrogramLinear(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.grapher).run()
        self.grapher.render(self.image)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())

