# -*- coding: utf-8 -*-

from timeside.core import Processor, implements, interfacedoc, FixedSizeInputAdapter
from timeside.api import *
import numpy


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
    def process(self, frames, eod=False):
        for buffer, end in self.adapter.process(frames, eod):
            # Test that the adapter is actually doing the job:
            if len(buffer) != self.BUFFER_SIZE:
                raise Exception("Bad buffer size from adapter")

        return frames, eod





