# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Thomas Fillon <thomas@parisson.com>
# Copyright (C) 2014-2015 Elio Quinton

# This file is part of TimeSide.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Authors:
#
# Thomas Fillon <thomas@parisson.com>
# Elio Quinton

from timeside.core import implements, interfacedoc
from timeside.core.analyzer import Analyzer
from timeside.core.api import IAnalyzer
from timeside.core.tools.parameters import HasTraits
from timeside.core.preprocessors import downmix_to_mono, frames_adapter

import numpy as np
import numpy as np
from scipy.signal import lfilter as lfilter
import warnings
#from timeside.core.tools.parameters import store_parameters


class LoudnessITU(Analyzer):

    """ Measure of audio loudness using standard ITU-R BS.1770-3

    WARNING: Sampling frequencies other that 44100Hz and 48000Hz are not fully supported

    Outputs: 
    Gated Loudness
    Relative Threshold
    Block Loudness    
    """

    implements(IAnalyzer)

    class _Param(HasTraits):
        pass

    _schema = {'$schema': 'http://json-schema.org/schema#',
               'properties': {},
               'type': 'object'}

    #@store_parameters
    def __init__(self):
        super(LoudnessITU, self).__init__()

        self.absoluteThreshold = -70   # in dB LKFS
        self.relativeThreshold = -10   # in dB LKFS
        self.weights = np.array([1.0, 1.0, 1.0, 1.41, 1.41])

        self.l = []
        self.z = None

        # filter coefficients
        self.B1 = None
        self.A1 = None
        self.B2 = None
        self.A2 = None

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(LoudnessITU, self).setup(
            channels, samplerate, blocksize, totalframes)

        self.input_blocksize = int(round(0.4 * self.input_samplerate))  # return a 400ms block
        self.input_stepsize = int(round(0.1 * self.input_samplerate))  # 75% overlap <=> 25% step
        self.z = [[] for x in xrange(self.input_channels)]  # generate empty list of list which dimensionality matches the number of channels

        # Setting filters coefficients according to sampling frequency
        if self.input_samplerate == 44100:
            self.B1 = np.array([1.53093728623786, -2.65120001232265, 1.16732946528280])
            self.A1 = np.array([1.0, -1.66410930225081, 0.711176041448821])
            self.B2 = np.array([0.994975383507587, -1.98995076701517, 0.994975383507587])
            self.A2 = np.array([1, -1.98992552008493, 0.989976013945421])
        elif self.input_samplerate == 48000:
            self.B1 = np.array([1.53512485958697, -2.69169618940638, 1.19839281085285])
            self.A1 = np.array([1.0, -1.69065929318241, 0.73248077421585])
            self.B2 = np.array([1.0, -2.0, 1.0])
            self.A2 = np.array([1.0, -1.99004745483398, 0.99007225036621])
        else:
            warnings.warn("Sample frequency is neither 44100Hz nor 48000Hz, using filter coeficients optimised for 48000Hz")
            self.B1 = np.array([1.53512485958697, -2.69169618940638, 1.19839281085285])
            self.A1 = np.array([1.0, -1.69065929318241, 0.73248077421585])
            self.B2 = np.array([1.0, -2.0, 1.0])
            self.A2 = np.array([1.0, -1.99004745483398, 0.99007225036621])

    @staticmethod
    @interfacedoc
    def id():
        return "loudness_itu"

    @staticmethod
    @interfacedoc
    def name():
        return "Loudness ITU"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    @frames_adapter
    def process(self, frames, eod=False):

        SumTerm = 0
        for n in range(0, self.input_channels):
            y = lfilter(self.B2, self.A2,
                        lfilter(self.B1, self.A1, frames[n]))
            zj = sum(y**2) / self.input_blocksize   # Mean square
            
            self.z[n].append(zj)
            SumTerm += self.weights[n] * zj

        SumTerm = max(SumTerm, 1e-10)  # dummy value to avoid division by zero in log10
        lj = -0.691 + 10 * np.log10(SumTerm)
        self.l.append(lj)

        return frames, eod

    def post_process(self):

        # remove last block in case it has been filled with zeros by the host, according to the standard specification
        self.z = np.array(self.z)  # self.z was a list, make it a numpy array.
        self.z = self.z[:, :-1]
        self.l = self.l[:-1]

        # Absolute Gating
        Jg = np.greater(self.l, self.absoluteThreshold)
        SumTerm = 0
        for n in range(0, self.input_channels):
            zi = np.array(self.z[n])
            zi_Jg = zi * Jg  # These two lines could be compressed in one : zi_Jg = zi[Jg]
            zi_Jg = zi_Jg[zi_Jg > 0]
            if len(zi_Jg):
                SumTerm += self.weights[n] * sum(zi_Jg) / len(zi_Jg)
        SumTerm = max(SumTerm, 1e-10)  # avoid division by zero in log10
        Gamma_r = -0.691 + 10 * np.log10(SumTerm) + self.relativeThreshold

        # Relative Gating
        Jg = np.greater(self.l, Gamma_r)
        SumTerm = 0
        for n in range(0, self.input_channels):
            zi = np.array(self.z[n])
            zi_Jg = zi * Jg
            zi_Jg = zi_Jg[zi_Jg > 0]
            if len(zi_Jg):
                SumTerm += self.weights[n] * sum(zi_Jg) / len(zi_Jg)

        SumTerm = max (SumTerm, 1e-10)  # avoid division by zero in log10
        GatedLoudness = -0.691 + 10 * np.log10(SumTerm)

        # Output result

        gated_loudness = self.new_result(data_mode='value', time_mode='global')
        gated_loudness.data_object.value = GatedLoudness
        gated_loudness.id_metadata.id += '.gated_loudness'
        gated_loudness.id_metadata.name += 'Gated Loudness'
        self.add_result(gated_loudness)

        relative_threshold = self.new_result(data_mode='value', time_mode='global')
        relative_threshold.data_object.value = Gamma_r
        relative_threshold.id_metadata.id += '.relative_threshold'
        relative_threshold.id_metadata.name += 'Relative Threshold'
        self.add_result(relative_threshold)

        block_loudness = self.new_result(data_mode='value', time_mode='framewise')
        block_loudness.data_object.value = self.l
        block_loudness.id_metadata.id += '.block_loudness'
        block_loudness.id_metadata.name += ' Block Loudness'
        self.add_result(block_loudness)


# Generate Grapher for Loudness ITU
from timeside.core.grapher import DisplayAnalyzer

DisplayLoudnessITU = DisplayAnalyzer.create(
    analyzer=LoudnessITU,
    result_id='loudness_itu.block_loudness',
    grapher_id='grapher_loudness_itu',
    grapher_name='Loudness ITU',
    staging=False)
