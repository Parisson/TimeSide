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
from __future__ import absolute_import

from timeside.analyzer.utils import segmentFromValues
from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from timeside.api import IAnalyzer
from aubio import pitch
import numpy


class IRITMonopoly(Analyzer):
    implements(IAnalyzer)
    '''
    Segmentor MOnophony/Polyphony based on the analalysis of yin confidence.

    Properties:
    '''

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(IRITMonopoly, self).setup(channels,
                                        samplerate,
                                        blocksize,
                                        totalframes)
        self.aubio_pitch = pitch(
            "default", self.input_blocksize, self.input_stepsize,
            samplerate)
        self.aubio_pitch.set_unit("freq")
        self.block_read = 0
        self.pitches = []
        self.pitch_confidences = []

    @staticmethod
    @interfacedoc
    def id():
        return "irit_monopoly"

    @staticmethod
    @interfacedoc
    def name():
        return "IRIT Monophony / Polyphony classification"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def __str__(self):
        return "Labeled Monophonic/Polyphonic segments"

    def process(self, frames, eod=False):
        self.decisionLen = 1.0
        # in seconds
        pf = self.aubio_pitch(frames.T[0])
        self.pitches += [pf[0]]
        self.pitch_confidences += [self.aubio_pitch.get_confidence()]
        self.block_read += 1
        return frames, eod

    def post_process(self):
        '''

        '''
        frameLenModulation = int(
            self.decisionLen * self.samplerate() / self.blocksize())
        epsilon = numpy.spacing(self.pitch_confidences[0])

        w = int(self.decisionLen * self.samplerate() / (self.blocksize() * 2))
        is_mono = []
        for i in range(w, len(self.pitch_confidences) - w, frameLenModulation):
            d = self.pitch_confidences[i - w:i + w]
            conf_mean = numpy.mean(d)
            conf_var = numpy.var(d + epsilon)
            if self.monoLikelihood(conf_mean, conf_var) > self.polyLikelihood(conf_mean, conf_var):
                is_mono += [True]
            else:
                is_mono += [False]

        conf = self.new_result(data_mode='value', time_mode='framewise')
        conf = self.new_result(data_mode='value', time_mode='framewise')
        conf.id_metadata.id += '.' + 'yin_confidence'
        conf.id_metadata.name += ' ' + 'Yin Confidence'
        conf.data_object.value = self.pitch_confidences

        self.process_pipe.results.add(conf)

        convert = {False: 0, True: 1}
        label = {0: 'Poly', 1: 'Mono'}
        segList = segmentFromValues(is_mono)
        segs = self.new_result(data_mode='label', time_mode='segment')
        segs.id_metadata.id += '.' + 'segments'
        segs.id_metadata.name += ' ' + 'Segments'

        segs.label_metadata.label = label

        segs.data_object.label = [convert[s[2]] for s in segList]
        segs.data_object.time = [(float(s[0]) * self.blocksize() /
                                  self.samplerate())
                                 for s in segList]
        segs.data_object.duration = [(float(s[1] - s[0]) * self.blocksize() /
                                      self.samplerate())
                                     for s in segList]
        self.process_pipe.results.add(segs)

    def monoLikelihood(self, m, v):

        theta1 = 0.1007
        theta2 = 0.0029
        beta1 = 0.5955
        beta2 = 0.2821
        delta = 0.848
        return self.weibullLikelihood(m, v, theta1, theta2, beta1, beta2, delta)

    def polyLikelihood(self, m, v):
        theta1 = 0.3224
        theta2 = 0.0121
        beta1 = 1.889
        beta2 = 0.8705
        delta = 0.644
        return self.weibullLikelihood(m, v, theta1, theta2, beta1, beta2, delta)

    def weibullLikelihood(self, m, v, theta1, theta2, beta1, beta2, delta):
        m = numpy.array(m)
        v = numpy.array(v)

        c0 = numpy.log(beta1 * beta2 / (theta1 * theta2))
        a1 = m / theta1
        b1 = a1 ** (beta1 / delta)
        c1 = numpy.log(a1)
        a2 = v / theta2
        b2 = a2 ** (beta2 / delta)
        c2 = numpy.log(a2)
        somme1 = (b1 + b2) ** delta
        Pxy = c0 + (beta1 / delta - 1) * c1 + (beta2 / delta - 1) * c2 + (delta - 2) * \
            numpy.log(b1 + b2) + numpy.log(somme1 + 1 / delta - 1) - somme1

        return numpy.mean(Pxy)
