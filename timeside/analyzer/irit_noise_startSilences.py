# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2014 Maxime Le Coz <lecoz@irit.fr>

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

from __future__ import absolute_import

import timeside
from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from timeside.analyzer.preprocessors import frames_adapter
from timeside.api import IAnalyzer
from timeside.analyzer.utils import MACHINE_EPSILON
from timeside.tools.buffering import BufferTable

import numpy
from scipy.signal import firwin, lfilter, lfiltic
from scipy.ndimage.morphology import binary_opening, binary_closing
import os


class IRITStartSeg(Analyzer):
    '''
    Segmentation of recording sessions into 'start' and 'session' segments

    Properties:
    '''
    implements(IAnalyzer)

    @interfacedoc
    def __init__(self):
        super(IRITStartSeg, self).__init__()

        self._buffer = BufferTable()

        # self.energy = []

        self.max_energy = 0.002*2
        self.min_overlap = 20
        self.threshold = 0.12

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):

        super(IRITStartSeg, self).setup(channels,
                                        samplerate,
                                        blocksize,
                                        totalframes)

        self.input_blocksize = int(0.02 * samplerate)
        self.input_stepsize = int(0.008 * samplerate)


        sr = float(samplerate)
        lowFreq = 100.0
        highFreq = sr / 5
        f1 = lowFreq / sr
        f2 = highFreq / sr
        numtaps = 10
        self.filtre = firwin(numtaps=numtaps, cutoff=[f1, f2], pass_zero=False)
        self.filtre_z = lfiltic(b=self.filtre, a=1, y=0)  # Initial conditions

    @staticmethod
    @interfacedoc
    def id():
        return "irit_startseg"

    @staticmethod
    @interfacedoc
    def name():
        return "IRIT Start/Session segmentation"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def __str__(self):
        return "Labeled Start/session segments"

    @frames_adapter
    def process(self, frames, eod=False):
        '''

        '''

        #self.energy += [numpy.sqrt(numpy.mean(lfilter(self.filtre,
        #                                              1.0,
        #                                              frames.T[0]) ** 2))]
        # Compute energy
        env, self.filtre_z = lfilter(b=self.filtre, a=1.0, axis=0,
                                     x=frames[:, 0],
                                     zi=self.filtre_z)
        self._buffer.append('energy', numpy.sqrt(numpy.mean(env ** 2)))

        return frames, eod

    def post_process(self):
        '''

        '''
        # Normalize energy
        self.energy = self._buffer['energy'][:]
        if self.energy.max():
            self.energy = self.energy / self.energy.max()

        silences = [1 if e < self.max_energy else 0 for e in self.energy]
        step = float(self.input_stepsize) / float(self.samplerate())

        models_dir = os.path.join(timeside.__path__[0],
                                  'analyzer', 'trained_models')
        prototype1_file = os.path.join(models_dir,
                                       'irit_noise_startSilences_proto1.dat')
        prototype2_file = os.path.join(models_dir,
                                       'irit_noise_startSilences_proto2.dat')

        prototype = numpy.load(prototype1_file)
        prototype2 = numpy.load(prototype2_file)

        # Lissage pour éliminer les petits segments dans un sens ou l'autre
        struct = [1] * len(prototype)
        silences = binary_closing(silences, struct)
        silences = binary_opening(silences, struct)

        seg = [0, -1, silences[0]]
        silencesList = []
        for i, v in enumerate(silences):
            if not (v == seg[2]):
                seg[1] = i
                silencesList.append(tuple(seg))
                seg = [i, -1, v]
        seg[1] = i
        silencesList.append(tuple(seg))
        selected_segs = []
        candidates = []

        for s in silencesList:
            if s[2] == 1:
                shape = numpy.array(self.energy[s[0]:s[1]])

                d1, _ = computeDist2(prototype, shape)
                d2, _ = computeDist2(prototype2, shape)
                dist = min([d1, d2])

                candidates.append((s[0], s[1], dist))
                if dist < self.threshold:
                    selected_segs.append(s)

        label = {0: 'Start', 1: 'Session'}

        segs = self.new_result(data_mode='label', time_mode='segment')
        segs.id_metadata.id += '.' + 'segments'
        segs.id_metadata.name += ' ' + 'Segments'
        segs.data_object.label_metadata.label = label
        segs.data_object.label = [s[2] for s in selected_segs]
        segs.data_object.time = [(float(s[0]) * step)
                                 for s in selected_segs]
        segs.data_object.duration = [(float(s[1] - s[0]) * step)
                                     for s in selected_segs]
        self.add_result(segs)

    def release(self):
        self._buffer.close()


def computeDist2(proto, serie):
    l = len(proto)
    r = range(len(serie))
    serie = numpy.array(list(serie) + [0] * (l - 1))
    v = [numpy.mean(numpy.abs((serie[i:i + l] /
                               max([numpy.max(serie[i:i + l]),
                                    MACHINE_EPSILON])) -
                              proto))
         for i in r]
    return numpy.min(v), numpy.argmin(v)


def computeDist(v1, v2, min_overlap):
    '''

    '''
    m1 = numpy.argmax(v1)
    m2 = numpy.argmax(v2)
    l1 = len(v1)
    l2 = len(v2)
    decal = numpy.abs(m1 - m2)

    if m1 >= m2:
        fin = numpy.min([l1 - decal, l2])
        if fin - decal > min_overlap:

            v1_out = numpy.array(v1[decal:decal + fin])
            v2_out = numpy.array(v2[:fin])
            d = numpy.mean(numpy.abs(v1_out - v2_out))
        else:
            v1_out = [0]
            v2_out = [1]
            d = 1
    else:
        return computeDist(v2, v1, min_overlap)

    return d, v1_out, v2_out
