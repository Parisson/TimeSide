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
        from timeside.grapher.waveform import Waveform
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_sweep_wav.png"
        self.grapher = Waveform(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testFlac2Waveform(self):
        "Test FLAC to Waveform"
        from timeside.grapher.waveform import Waveform
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")
        self.image = "/tmp/test_waveform_sweep_flac.png"
        self.grapher = Waveform(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testMp32Waveform(self):
        "Test MP3 to Waveform"
        from timeside.grapher.waveform import Waveform
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")
        self.image = "/tmp/test_waveform_sweep_mp3.png"
        self.grapher = Waveform(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testOgg2Waveform(self):
        "Test OGG to Waveform"
        from timeside.grapher.waveform import Waveform
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")
        self.image = "/tmp/test_waveform_sweep_ogg.png"
        self.grapher = Waveform(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    # WAVEFORM SIMPLE
    def testWav2WaveformSimple(self):
        "Test WAV to WaveformSimple"
        from timeside.grapher.waveform_simple import WaveformSimple
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_simple_sweep_wav.png"
        self.grapher = WaveformSimple(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    # WAVEFORMS CONTOUR BLACK
    def testWav2WaveformContourBlack(self):
        "Test WAV to WaveformContourBlack"
        from timeside.grapher.waveform_contour_bk import WaveformContourBlack
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_contour_bk_sweep_wav.png"
        self.grapher = WaveformContourBlack(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testFlac2WaveformContourBlack(self):
        "Test FLAC to WaveformContourBlack"
        from timeside.grapher.waveform_contour_bk import WaveformContourBlack
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")
        self.image = "/tmp/test_waveform_contour_bk_sweep_flac.png"
        self.grapher = WaveformContourBlack(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testMp32WaveformContourBlack(self):
        "Test MP3 to WaveformContourBlack"
        from timeside.grapher.waveform_contour_bk import WaveformContourBlack
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")
        self.image = "/tmp/test_waveform_contour_bk_sweep_mp3.png"
        self.grapher = WaveformContourBlack(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testOgg2WaveformContourBlack(self):
        "Test OGG to WaveformContourBlack"
        from timeside.grapher.waveform_contour_bk import WaveformContourBlack
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")
        self.image = "/tmp/test_waveform_contour_bk_sweep_ogg.png"
        self.grapher = WaveformContourBlack(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    # WAVEFORMS CONTOUR WHITE
    def testWav2WaveformContourWhite(self):
        "Test WAV to WaveformContourWhite"
        from timeside.grapher.waveform_contour_wh import WaveformContourWhite
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_contour_wh_sweep_wav.png"
        self.grapher = WaveformContourWhite(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testFlac2WaveformContourWhite(self):
        "Test FLAC to WaveformContourWhite"
        from timeside.grapher.waveform_contour_wh import WaveformContourWhite
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")
        self.image = "/tmp/test_waveform_contour_wh_sweep_flac.png"
        self.grapher = WaveformContourWhite(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testMp32WaveformContourWhite(self):
        "Test MP3 to WaveformContourWhite"
        from timeside.grapher.waveform_contour_wh import WaveformContourWhite
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")
        self.image = "/tmp/test_waveform_contour_wh_sweep_mp3.png"
        self.grapher = WaveformContourWhite(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testOggWaveformContourWhite(self):
        "Test OGG to WaveformContourWhite"
        from timeside.grapher.waveform_contour_wh import WaveformContourWhite
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")
        self.image = "/tmp/test_waveform_contour_wh_sweep_ogg.png"
        self.grapher = WaveformContourWhite(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')


    # SPECTROGRAMS
    def testWav2Spectrogram(self):
        "Test WAV to Spectrogram"
        from timeside.grapher.spectrogram import Spectrogram
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_spectrogram_sweep_wav.png"
        self.grapher = Spectrogram(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testMp32Spectrogram(self):
        "Test MP3 to Spectrogram"
        from timeside.grapher.spectrogram import Spectrogram
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")
        self.image = "/tmp/test_spectrogram_sweep_mp3.png"
        self.grapher = Spectrogram(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testFlac2Spectrogram(self):
        "Test FLAC to Spectrogram"
        from timeside.grapher.spectrogram import Spectrogram
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")
        self.image = "/tmp/test_spectrogram_sweep_flac.png"
        self.grapher = Spectrogram(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testOgg2Spectrogram(self):
        "Test OGG to Spectrogram"
        from timeside.grapher.spectrogram import Spectrogram
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")
        self.image = "/tmp/test_spectrogram_sweep_ogg.png"
        self.grapher = Spectrogram(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.grapher).run()
        self.grapher.render(self.image)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())

