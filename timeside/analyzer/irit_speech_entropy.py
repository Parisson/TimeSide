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

from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from timeside.analyzer.utils import entropy, computeModulation
from timeside.analyzer.utils import segmentFromValues
from timeside.api import IAnalyzer
from numpy import array
from scipy.ndimage.morphology import binary_opening


class IRITSpeechEntropy(Analyzer):

    """Speech Segmentor based on Entropy analysis."""

    implements(IAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None,
              totalframes=None):
        super(IRITSpeechEntropy, self).setup(
            channels, samplerate, blocksize, totalframes)
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
        return "IRIT Speech entropy"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def __str__(self):
        return "Speech confidences indexes"

    def process(self, frames, eod=False):
        self.entropyValue.append(entropy(frames))
        return frames, eod

    def post_process(self):

        entropyValue = array(self.entropyValue)
        w = self.modulLen * self.samplerate() / self.blocksize()
        modulentropy = computeModulation(entropyValue, w, False)
        confEntropy = array(modulentropy - self.threshold) / self.threshold
        confEntropy[confEntropy > 1] = 1

        conf = self.new_result(data_mode='value', time_mode='framewise')

        conf.id_metadata.id += '.' + 'confidence'
        conf.id_metadata.name += ' ' + 'Confidence'

        conf.data_object.value = confEntropy
        self.process_pipe.results.add(conf)

        # Binary Entropy
        binaryEntropy = modulentropy > self.threshold
        binaryEntropy = binary_opening(
            binaryEntropy, [1] * (self.smoothLen * 2))

        convert = {False: 0, True: 1}
        label = {0: 'NonSpeech', 1: 'Speech'}
        segList = segmentFromValues(binaryEntropy)

        segs = self.new_result(data_mode='label', time_mode='segment')
        segs.id_metadata.id += '.' + 'segments'
        segs.id_metadata.name += ' ' + 'Segments'

        segs.label_metadata.label = label

        segs.data_object.label = [convert[s[2]] for s in segList]
        segs.data_object.time = [(float(s[0]) * self.blocksize() /
                                 self.samplerate())
                                 for s in segList]
        segs.data_object.duration = [(float(s[1] - s[0] + 1) * self.blocksize() /
                                     self.samplerate())
                                     for s in segList]

        self.process_pipe.results.add(segs)

        return
