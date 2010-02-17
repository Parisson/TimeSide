# -*- coding: utf-8 -*-
from timeside.core import Processor, implements, interfacedoc, FixedSizeInputAdapter
from timeside.api import *
from timeside.graph import *
from timeside import Metadata
from scikits import audiolab
import numpy

class FileDecoder(Processor):
    """A simple audiolab-based example decoder"""
    implements(IDecoder)

    @staticmethod
    @interfacedoc
    def id():
        return "test_audiolabdec"

    @interfacedoc
    def __init__(self, filename):
        self.filename = filename
        # The file has to be opened here so that nframes(), samplerate(),
        # etc.. work before setup() is called.
        self.file     = audiolab.Sndfile(self.filename, 'r')
        self.position = 0

    @interfacedoc
    def setup(self):
        super(FileDecoder, self).setup()
        if self.position != 0:
            self.file.seek(0);
            self.position = 0

    def release(self):
        super(FileDecoder, self).release()
        if self.file:
            self.file.close()
            self.file = None

    @interfacedoc
    def channels(self):
        return self.file.channels

    @interfacedoc
    def samplerate(self):
        return self.file.samplerate

    @interfacedoc
    def nframes(self):
        return self.file.nframes

    @interfacedoc
    def format(self):
        return self.file.file_format

    @interfacedoc
    def encoding(self):
        return self.file.encoding
    @interfacedoc
    def resolution(self):
        resolution = None
        encoding = self.file.encoding

        if encoding == "pcm8":
            resolution = 8

        elif encoding == "pcm16":
            resolution = 16
        elif encoding == "pcm32":
            resolution = 32

        return resolution

    @interfacedoc
    def metadata(self):
        #TODO
        return Metadata()

    @interfacedoc
    def process(self, frames=None, eod=False):
        if frames:
            raise Exception("Decoder doesn't accept input frames")

        buffersize = 0x10000

        # Need this because audiolab raises a bogus exception when asked
        # to read passed the end of the file
        toread = self.nframes() - self.position
        if toread > buffersize:
            toread = buffersize

        frames         = self.file.read_frames(toread)
        eod            = (toread < buffersize)
        self.position += toread

        # audiolab returns a 1D array for 1 channel, need to reshape to 2D: 
        if self.file.channels == 1:
            frames = frames.reshape(len(frames), 1)

        return frames, eod

class MaxLevel(Processor):
    implements(IValueAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, nframes=None):
        super(MaxLevel, self).setup(channels, samplerate, nframes)
        self.max_value = 0

    @staticmethod
    @interfacedoc
    def id():
        return "test_maxlevel"

    @staticmethod
    @interfacedoc
    def name():
        return "Max level test analyzer"

    @staticmethod
    @interfacedoc
    def unit():
        # power? amplitude?
        return ""

    def process(self, frames, eod=False):
        max = frames.max()
        if max > self.max_value:
            self.max_value = max

        return frames, eod

    def result(self):
        return self.max_value

class Gain(Processor):
    implements(IEffect)

    @interfacedoc
    def __init__(self, gain=1.0):
        self.gain = gain

    @staticmethod
    @interfacedoc
    def id():
        return "test_gain"

    @staticmethod
    @interfacedoc
    def name():
        return "Gain test effect"

    def process(self, frames, eod=False):
        return numpy.multiply(frames, self.gain), eod

class WavEncoder(Processor):
    implements(IEncoder)

    def __init__(self, output):
        self.file = None
        if isinstance(output, basestring):
            self.filename = output
        else:
            raise Exception("Streaming not supported")

    @interfacedoc
    def setup(self, channels=None, samplerate=None, nframes=None):
        super(WavEncoder, self).setup(channels, samplerate, nframes)
        if self.file:
            self.file.close()

        format = audiolab.Format("wav", "pcm16")
        self.file = audiolab.Sndfile(self.filename, 'w', format=format, channels=channels,
                                     samplerate=samplerate)

    @staticmethod
    @interfacedoc
    def id():
        return "test_wavenc"

    @staticmethod
    @interfacedoc
    def description():
        return "Hackish wave encoder"

    @staticmethod
    @interfacedoc
    def file_extension():
        return "wav"

    @staticmethod
    @interfacedoc
    def mime_type():
        return "audio/x-wav"

    @interfacedoc
    def set_metadata(self, metadata):
        #TODO
        pass

    @interfacedoc
    def process(self, frames, eod=False):
        self.file.write_frames(frames)
        if eod:
            self.file.close()
            self.file = None

        return frames, eod


class Waveform(Processor):
    implements(IGrapher)

    @interfacedoc
    def __init__(self, width, height, nframes, output=None):
        self.nframes = nframes
        self.filename = output
        self.image = None
        if width:
            self.width = width
        else:
            self.width = 1500
        if height:
            self.height = height
        else:
            self.height = 200
        #if isinstance(output, basestring):
            #self.filename = output
        #else:
            #raise Exception("Streaming not supported")
        self.bg_color = None
        self.color_scheme = None

    @staticmethod
    @interfacedoc
    def id():
        return "test_waveform"

    @staticmethod
    @interfacedoc
    def name():
        return "Waveform test"

    @interfacedoc
    def set_colors(self, background, scheme):
        self.bg_color = background
        self.color_scheme = scheme

    @interfacedoc
    def setup(self, channels=None, samplerate=None, nframes=None):
        super(Waveform, self).setup(channels, samplerate, nframes)
        if self.image:
            self.image.close()
        self.image = WaveformImage(self.width, self.height, self.nframes)

    @interfacedoc
    def process(self, frames, eod=False):
        pass
        #self.image.process(frames)
        #if eod:
            #self.image.close()
            #self.image = None
        #return frames, eod

    @interfacedoc
    def render(self):
        pass
        #self.image.process()
        #if self.filename:
            #self.image.save()
        #return self.image

class Duration(Processor):
    """A rather useless duration analyzer. Its only purpose is to test the
       nframes characteristic."""
    implements(IValueAnalyzer)

    @interfacedoc
    def setup(self, channels, samplerate, nframes):
        if not nframes:
            raise Exception("nframes argument required")
        super(Duration, self).setup(channels, samplerate, nframes)

    @staticmethod
    @interfacedoc
    def id():
        return "test_duration"

    @staticmethod
    @interfacedoc
    def name():
        return "Duration analyzer"

    @staticmethod
    @interfacedoc
    def unit():
        return "seconds"

    def result(self):
        return self.input_nframes / float(self.input_samplerate)

class FixedInputProcessor(Processor):
    """Processor which does absolutely nothing except illustrating the use
    of the FixedInputSizeAdapter. It also tests things a bit."""

    implements(IProcessor)

    BUFFER_SIZE = 1024

    @staticmethod
    @interfacedoc
    def id():
        return "test_fixed"

    @interfacedoc
    def setup(self, channels, samplerate, nframes):
        super(FixedInputProcessor, self).setup(channels, samplerate, nframes)
        self.adapter = FixedSizeInputAdapter(self.BUFFER_SIZE, channels, pad=True)

    @interfacedoc        
    def nframes(self):
        return self.adapter.nframes(self.input_nframes)

    @interfacedoc
    def process(self, frames, eod=False):
        try:
            for buffer, end in self.adapter.process(frames, eod):
                # Test that the adapter is actually doing the job:
                if len(buffer) != self.BUFFER_SIZE:
                    raise Exception("Bad buffer size from adapter")
        except ValueError:
            print len(frames)
            raise

        return frames, eod                    



            

