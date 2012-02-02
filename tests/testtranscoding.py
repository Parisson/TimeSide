from timeside.core import *
from timeside.decoder import *
from timeside.analyzer import *
from timeside.encoder import *
from timeside.api import *
from timeside.component import *

from unit_timeside import *

import os.path

__all__ = ['TestTranscoding']

class TestTranscoding(TestCase):
    "Test the low level streaming features"

    def setUp(self):
        pass

    def testWav2Mp3(self):
        "Test wav to mp3 conversion"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")

        dest1 = "/tmp/test_wav_filesink.mp3"
        dest2 = "/tmp/test_wav_appsink.mp3"
        self.f = open(dest2,'w')

        self.streaming=True
        self.encoder = Mp3Encoder(dest1, streaming=True)

    def testFlac2Mp3(self):
        "Test flac to mp3 conversion"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")

        dest1 = "/tmp/test_flac_filesink.mp3"
        dest2 = "/tmp/test_flac_appsink.mp3"
        self.f = open(dest2,'w')

        self.streaming=True
        self.encoder = Mp3Encoder(dest1, streaming=True)


    #def testFlac2Ogg(self):
        #"Test flac to ogg conversion"
        #self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.flac")

        #dest1 = "/tmp/test_flac_filesink.ogg"
        #dest2 = "/tmp/test_flac_appsink.ogg"
        #self.f = open(dest2,'w')

        #self.streaming=True

        #encoder = VorbisEncoder(dest1, streaming=True)
        #self.encoder = encoder

#    def testWav2Ogg(self):
#        "Test wav to ogg conversion"
#        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")
#
#        dest1 = "/tmp/test_wav_filesink.ogg"
#        dest2 = "/tmp/test_wav_appsink.ogg"
#        self.f = open(dest2,'w')
#
#        self.streaming=True
#        self.encoder = VorbisEncoder(dest1, streaming=True)

    #def testWav2Flac(self):
        #"Test wav to flac conversion"
        #self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")

        #dest1 = "/tmp/test_wav_filesink.flac"
        #dest2 = "/tmp/test_wav_appsink.flac"
        #self.f = open(dest2,'w')

        #self.streaming=True

        #encoder = FlacEncoder(dest1, streaming=True)
        #self.encoder = encoder

    def testWav2Webm(self):
        "Test wav to webm conversion"
        self.source = os.path.join (os.path.dirname(__file__),  "samples/sweep.wav")

        dest1 = "/tmp/test_wav_filesink.webm"
        dest2 = "/tmp/test_wav_appsink.webm"
        self.f = open(dest2,'w')

        self.streaming=True
        self.encoder = WebMEncoder(dest1, streaming=True)

    def setUpDecoder(self):
        self.decoder = FileDecoder(self.source)
        self.decoder.setup()
        self.channels  = self.decoder.channels()
        self.samplerate = self.decoder.samplerate()

    def setUpEncoder(self):
        self.encoder.setup(channels = self.channels, samplerate = self.samplerate)

    def tearDown(self):
        self.setUpDecoder()
        self.setUpEncoder()

        #print "decoder pipe:\n", decoder.pipe
        #print "encoder pipe:\n", encoder.pipe
        totalframes = 0.

        while True:
            frames, eod = self.decoder.process()
            #print frames.shape[0]
            totalframes += frames.shape[0]
            self.encoder.process(frames, eod)
            if self.streaming:
                self.f.write(self.encoder.chunk)
            if eod:
                break
            if self.encoder.eod :
                break
        self.f.close()

        # FIXME compute actual number of frames from file
#        self.assertEquals(totalframes, 352801)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())

