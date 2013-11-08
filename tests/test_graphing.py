#! /usr/bin/env python

from timeside.decoder.core import FileDecoder
from unit_timeside import *

import os.path

__all__ = ['TestGraphing']

class TestGraphing(TestCase):
    "Test all graphers with various input media formats"

    def setUp(self):
        pass

    # WAVEFORMS
    def testWav2Waveform(self):
        "Test WAV to Waveform"
        from timeside.grapher.waveform_simple import Waveform
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_sweep_wav.png"
        self.grapher = Waveform(width=1024, height=256, bg_color=(255,255,255), color_scheme='default')

    def testFlac2Waveform(self):
        "Test FLAC to Waveform"
        from timeside.grapher.waveform_simple import Waveform
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")
        self.image = "/tmp/test_waveform_sweep_flac.png"
        self.grapher = Waveform(width=1024, height=256, bg_color=(255,255,255), color_scheme='default')

    def testMp32Waveform(self):
        "Test MP3 to Waveform"
        from timeside.grapher.waveform_simple import Waveform
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")
        self.image = "/tmp/test_waveform_sweep_mp3.png"
        self.grapher = Waveform(width=1024, height=256, bg_color=(255,255,255), color_scheme='default')

    def testOgg2Waveform(self):
        "Test OGG to Waveform"
        from timeside.grapher.waveform_simple import Waveform
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")
        self.image = "/tmp/test_waveform_sweep_ogg.png"
        self.grapher = Waveform(width=1024, height=256, bg_color=(255,255,255), color_scheme='default')

    # WAVEFORM CENTROID
    def testWav2WaveformCentroid(self):
        "Test WAV to WaveformCentroid"
        from timeside.grapher.waveform_centroid import WaveformCentroid
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_centroid_sweep_wav.png"
        self.grapher = WaveformCentroid(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testFlac2WaveformCentroid(self):
        "Test FLAC to WaveformCentroid"
        from timeside.grapher.waveform_centroid import WaveformCentroid
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_centroid_sweep_wav.png"
        self.grapher = WaveformCentroid(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testMp32WaveformCentroid(self):
        "Test MP3 to WaveformCentroid"
        from timeside.grapher.waveform_centroid import WaveformCentroid
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_centroid_sweep_wav.png"
        self.grapher = WaveformCentroid(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testOgg2WaveformCentroid(self):
        "Test OGG to WaveformCentroid"
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

    def testFlac2WaveformContourWhite(self):
        "Test FLAC to WaveformTransparent"
        from timeside.grapher.waveform_transparent import WaveformTransparent
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")
        self.image = "/tmp/test_waveform_transparent_sweep_flac.png"
        self.grapher = WaveformTransparent(width=1024, height=256, bg_color=None, color_scheme='default')

    def testMp32WaveformTransparent(self):
        "Test MP3 to WaveformTransparent"
        from timeside.grapher.waveform_transparent import WaveformTransparent
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")
        self.image = "/tmp/test_waveform_transparent_sweep_mp3.png"
        self.grapher = WaveformTransparent(width=1024, height=256, bg_color=None, color_scheme='default')

    def testOggWaveformTransparent(self):
        "Test OGG to WaveformTransparent"
        from timeside.grapher.waveform_transparent import WaveformTransparent
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")
        self.image = "/tmp/test_waveform_transparent_sweep_ogg.png"
        self.grapher = WaveformTransparent(width=1024, height=256, bg_color=None, color_scheme='default')

    # WAVEFORMS CONTOUR BLACK
    def testWav2WaveformContourBlack(self):
        "Test WAV to WaveformContourBlack"
        from timeside.grapher.waveform_contour import WaveformContourBlack
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_contour_bk_sweep_wav.png"
        self.grapher = WaveformContourBlack(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testFlac2WaveformContourBlack(self):
        "Test FLAC to WaveformContourBlack"
        from timeside.grapher.waveform_contour import WaveformContourBlack
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")
        self.image = "/tmp/test_waveform_contour_bk_sweep_flac.png"
        self.grapher = WaveformContourBlack(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testMp32WaveformContourBlack(self):
        "Test MP3 to WaveformContourBlack"
        from timeside.grapher.waveform_contour import WaveformContourBlack
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")
        self.image = "/tmp/test_waveform_contour_bk_sweep_mp3.png"
        self.grapher = WaveformContourBlack(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testOgg2WaveformContourBlack(self):
        "Test OGG to WaveformContourBlack"
        from timeside.grapher.waveform_contour import WaveformContourBlack
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")
        self.image = "/tmp/test_waveform_contour_bk_sweep_ogg.png"
        self.grapher = WaveformContourBlack(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    # WAVEFORMS CONTOUR WHITE
    def testWav2WaveformContourWhite(self):
        "Test WAV to WaveformContourWhite"
        from timeside.grapher.waveform_contour import WaveformContourWhite
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_contour_wh_sweep_wav.png"
        self.grapher = WaveformContourWhite(width=1024, height=256, bg_color=(255,255,255), color_scheme='default')

    def testFlac2WaveformContourWhite(self):
        "Test FLAC to WaveformContourWhite"
        from timeside.grapher.waveform_contour import WaveformContourWhite
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")
        self.image = "/tmp/test_waveform_contour_wh_sweep_flac.png"
        self.grapher = WaveformContourWhite(width=1024, height=256, bg_color=(255,255,255), color_scheme='default')

    def testMp32WaveformContourWhite(self):
        "Test MP3 to WaveformContourWhite"
        from timeside.grapher.waveform_contour import WaveformContourWhite
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")
        self.image = "/tmp/test_waveform_contour_wh_sweep_mp3.png"
        self.grapher = WaveformContourWhite(width=1024, height=256, bg_color=(255,255,255), color_scheme='default')

    def testOggWaveformContourWhite(self):
        "Test OGG to WaveformContourWhite"
        from timeside.grapher.waveform_contour import WaveformContourWhite
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")
        self.image = "/tmp/test_waveform_contour_wh_sweep_ogg.png"
        self.grapher = WaveformContourWhite(width=1024, height=256, bg_color=(255,255,255), color_scheme='default')

    # LOG SPECTROGRAMS
    def testWav2Spectrogram(self):
        "Test WAV to Spectrogram"
        from timeside.grapher.spectrogram_log import SpectrogramLog
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_spectrogram_log_sweep_wav.png"
        self.grapher = SpectrogramLog(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testMp32SpectrogramLog(self):
        "Test MP3 to SpectrogramLog"
        from timeside.grapher.spectrogram_log import SpectrogramLog
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")
        self.image = "/tmp/test_spectrogram_log_sweep_mp3.png"
        self.grapher = SpectrogramLog(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testFlac2SpectrogramLog(self):
        "Test FLAC to SpectrogramLog"
        from timeside.grapher.spectrogram_log import SpectrogramLog
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")
        self.image = "/tmp/test_spectrogram_log_sweep_flac.png"
        self.grapher = SpectrogramLog(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testOgg2SpectrogramLog(self):
        "Test OGG to SpectrogramLog"
        from timeside.grapher.spectrogram_log import SpectrogramLog
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")
        self.image = "/tmp/test_spectrogram_log_sweep_ogg.png"
        self.grapher = SpectrogramLog(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    # LIN SPECTROGRAMS
    def testWav2Spectrogram(self):
        "Test WAV to SpectrogramLinear"
        from timeside.grapher.spectrogram_lin import SpectrogramLinear
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_spectrogram_lin_sweep_wav.png"
        self.grapher = SpectrogramLinear(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testMp32SpectrogramLinear(self):
        "Test MP3 to SpectrogramLinear"
        from timeside.grapher.spectrogram_lin import SpectrogramLinear
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")
        self.image = "/tmp/test_spectrogram_lin_sweep_mp3.png"
        self.grapher = SpectrogramLinear(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testFlac2SpectrogramLinear(self):
        "Test FLAC to SpectrogramLinear"
        from timeside.grapher.spectrogram_lin import SpectrogramLinear
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")
        self.image = "/tmp/test_spectrogram_lin_sweep_flac.png"
        self.grapher = SpectrogramLinear(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testOgg2SpectrogramLinear(self):
        "Test OGG to SpectrogramLinear"
        from timeside.grapher.spectrogram_lin import SpectrogramLinear
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")
        self.image = "/tmp/test_spectrogram_lin_sweep_ogg.png"
        self.grapher = SpectrogramLinear(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.grapher).run()
        self.grapher.render(self.image)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())

