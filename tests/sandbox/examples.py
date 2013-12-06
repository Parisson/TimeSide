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
