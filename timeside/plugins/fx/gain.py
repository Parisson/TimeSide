# -*- coding: utf-8 -*-

from timeside.core import Processor, implements, interfacedoc
from timeside.core.api import IEffect
import numpy


class Gain(Processor):
    """Gain effect processor"""

    implements(IEffect)

    @interfacedoc
    def __init__(self, gain=1.0):
        super(Gain, self).__init__()
        self.gain = gain

    @staticmethod
    @interfacedoc
    def id():
        return "fx_gain"

    @staticmethod
    @interfacedoc
    def name():
        return "Gain effect"

    def process(self, frames, eod=False):
        return numpy.multiply(frames, self.gain), eod
