
from timeside.core import *
from timeside.decoder import *
from timeside.analyzer import *
from timeside.encoder import *
from timeside.grapher import *
from timeside.api import *

from timeside.component import *
from timeside.tests import TestCase, TestRunner
import unittest

import os.path

__all__ = ['TestGraphers']

class TestGraphers(TestCase):
    "Test all graphers with various input media formats"

    def setUp(self):
        pass
    
    # WAVEFORMS
    def testWav2Waveform(self):
        "Test WAV to Waveform"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveform_sweep_wav.png"
        self.grapher = Waveform(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testFlac2Waveform(self):
        "Test FLAC to Waveform"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")
        self.image = "/tmp/test_waveform_sweep_flac.png"
        self.grapher = Waveform(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')
    
    def testMp32Waveform(self):
        "Test MP3 to Waveform"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")
        self.image = "/tmp/test_waveform_sweep_mp3.png"
        self.grapher = Waveform(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')
    
    def testOgg2Waveform(self):
        "Test OGG to Waveform"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")
        self.image = "/tmp/test_waveform_sweep_ogg.png"
        self.grapher = Waveform(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')
    
    # WAVEFORMS JOYDIV
    def testWav2WaveformJoyDiv(self):
        "Test WAV to WaveformJoyDiv"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_waveformjoydiv_sweep_wav.png"
        self.grapher = WaveformJoyDiv(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')

    def testFlac2WaveformJoyDiv(self):
        "Test FLAC to WaveformJoyDiv"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")
        self.image = "/tmp/test_waveformjoydiv_sweep_flac.png"
        self.grapher = WaveformJoyDiv(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')
    
    def testMp32WaveformJoyDiv(self):
        "Test MP3 to WaveformJoyDiv"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")
        self.image = "/tmp/test_waveformjoydiv_sweep_mp3.png"
        self.grapher = WaveformJoyDiv(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')
    
    def testOgg2WaveformJoyDiv(self):
        "Test OGG to WaveformJoyDiv"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")
        self.image = "/tmp/test_waveformjoydiv_sweep_ogg.png"
        self.grapher = WaveformJoyDiv(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')
        
    # SPECTROGRAMS
    def testWav2Spectrogram(self):
        "Test WAV to Spectrogram"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
        self.image = "/tmp/test_spectrogram_sweep_wav.png"
        self.grapher = Spectrogram(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')
    
    def testMp32Spectrogram(self):
        "Test MP3 to Spectrogram"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.mp3")
        self.image = "/tmp/test_spectrogram_sweep_mp3.png"
        self.grapher = Spectrogram(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')
    
    def testFlac2Spectrogram(self):
        "Test FLAC to Spectrogram"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")
        self.image = "/tmp/test_spectrogram_sweep_flac.png"
        self.grapher = Spectrogram(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')
    
    def testOgg2Spectrogram(self):
        "Test OGG to Spectrogram"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.ogg")
        self.image = "/tmp/test_spectrogram_sweep_ogg.png"
        self.grapher = Spectrogram(width=1024, height=256, bg_color=(0,0,0), color_scheme='default')
     
    def tearDown(self):
        decoder = FileDecoder(self.source)
        (decoder | self.grapher).run()
        self.grapher.render(self.image)
        
if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())

