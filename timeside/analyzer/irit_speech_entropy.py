# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Maxime Le Coz <lecoz@irit.fr>

# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

# Author: Maxime Le Coz <lecoz@irit.fr>

from timeside.core import Processor, implements, interfacedoc, FixedSizeInputAdapter
from timeside.analyzer.core import *
from timeside.api import IValueAnalyzer
from numpy import array
from scipy.ndimage.morphology import binary_opening
from matplotlib import pylab

class IRITSpeechEntropy(Processor):
    implements(IValueAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(IRITSpeechEntropy, self).setup(channels, samplerate, blocksize, totalframes)
        self.entropyValue = []
        self.threshold = 0.4
        self.smoothLen = 5
        self.modulLen = 2

    @staticmethod
    @interfacedoc
    def id():
        return "irit_speech_entropy"

    @staticmethod
    @interfacedoc
    def name():
        return "Speech entropy (IRIT)"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def __str__(self):
        return "Speech confidences indexes"

    def process(self, frames, eod=False):
        self.entropyValue.append(entropy(frames))
        return frames, eod

    def results(self):

        entropyValue = numpy.array(self.entropyValue)
        w = self.modulLen*self.samplerate()/self.blocksize()
        modulentropy = computeModulation(entropyValue,w,False)
        confEntropy=  array(modulentropy-self.threshold)/self.threshold
        confEntropy[confEntropy>1] = 1

        conf = AnalyzerResult(id = "irit_entropy_confidence", name = "entropy (IRIT)", unit = "?")
        conf.value = confEntropy

        binaryEntropy = modulentropy > self.threshold
        binaryEntropy = binary_opening(binaryEntropy,[1]*(self.smoothLen*2))

        convert = {False:'NonSpeech',True:'Speech'}
        segList = segmentFromValues(binaryEntropy)

        segmentsEntropy =[]
        for s in segList :
            segmentsEntropy.append((numpy.float(s[0])*self.blocksize()/self.samplerate(),
                                    numpy.float(s[1])*self.blocksize()/self.samplerate(),
                                    convert[s[2]]))

        segs = AnalyzerResult(id="irit_entropy_segments", name="seg entropy (IRIT)", unit="s")
        segs.value = segmentsEntropy

        return AnalyzerResultContainer([conf, segs])
