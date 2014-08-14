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
from timeside.analyzer.utils import melFilterBank, computeModulation
from timeside.analyzer.utils import segmentFromValues
from timeside.analyzer.irit_diverg import IRITDiverg
from timeside.api import IAnalyzer
from numpy import logical_and, array, hamming, dot, mean, float, arange, nonzero
from numpy.fft import rfft
from scipy.signal import firwin, lfilter
from pylab import plot, show


class IRITMusicLDN(Analyzer):
    implements(IAnalyzer)

    def __init__(self, blocksize=1024, stepsize=None):
        super(IRITMusicLDN, self).__init__()
        self.parents.append(IRITDiverg())
        self.wLen = 1.0
        self.wStep = 0.1
        self.threshold = 20

    @staticmethod
    @interfacedoc
    def id():
        return "irit_music_ldn"

    @staticmethod
    @interfacedoc
    def name():
        return "IRIT Music Detector - Segment Length"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def __str__(self):
        return "Music confidence indexes"

    def process(self, frames, eod=False):
        return frames, eod

    def post_process(self):
        '''
        '''

        segList = self.process_pipe.resultsget_result_by_id('irit_diverg.segments').time
        w = self.wLen / 2
        end = segList[-1]
        tLine = arange(0, end, self.wStep)

        segLen = array([0] * len(tLine))

        for i, t in enumerate(tLine):
            idx = nonzero(logical_and(segList > (t - w), segList < (t + w)))[0]
            segLen[i] = len(idx)

        plot(tLine, segLen)
        show()
        # Confidence Index
        conf = array(segLen - self.threshold) / self.threshold
        conf[conf > 1] = 1

        segLenRes = self.new_result(data_mode='value', time_mode='framewise')
        segLenRes.id_metadata.id += '.' + 'energy_confidence'
        segLenRes.id_metadata.name += ' ' + 'Energy Confidence'

        segLenRes.data_object.value = segLen

        self.process_pipe.results.add(segLenRes)

        # Segment
        convert = {False: 0, True: 1}
        label = {0: 'nonMusic', 1: 'Music'}

        segList = segmentFromValues(segLen > self.threshold)
        # Hint : Median filtering could imrove smoothness of the result
        # from scipy.signal import medfilt
        # segList = segmentFromValues(medfilt(modEnergyValue > self.threshold, 31))

        segs = self.new_result(data_mode='label', time_mode='segment')
        segs.id_metadata.id += '.' + 'segments'
        segs.id_metadata.name += ' ' + 'Segments'

        segs.label_metadata.label = label

        segs.data_object.label = [convert[s[2]] for s in segList]
        segs.data_object.time = [tLine[s[0]] for s in segList]
        segs.data_object.duration = [tLine[s[1]] - tLine[s[0]]
                                     for s in segList]

        self.process_pipe.results.add(segs)
        return
