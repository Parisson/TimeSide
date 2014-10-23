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
import numpy
from timeside.analyzer.preprocessors import frames_adapter
from timeside.analyzer.externals.aubio_pitch import AubioPitch


class IRITMonopoly(Analyzer):
    """
    Segmentor Monophony/Polyphony based on the analysis of yin confidence.

    Properties:
    """
    implements(IAnalyzer)

    @interfacedoc
    def __init__(self):
        super(IRITMonopoly, self).__init__()

        # Irit Monopoly parameters
        self.decisionLen = 1.0
        self.wLen = 0.1
        self.wStep = 0.05

        self._aubio_pitch_analyzer = AubioPitch(blocksize_s=self.wLen,
                                                stepsize_s=self.wStep)
        self.parents['aubio_pitch'] = self._aubio_pitch_analyzer

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(IRITMonopoly, self).setup(channels,
                                        samplerate,
                                        blocksize,
                                        totalframes)

        self.input_blocksize = self._aubio_pitch_analyzer.input_blocksize
        self.input_stepsize = self._aubio_pitch_analyzer.input_stepsize

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

    @frames_adapter
    def process(self, frames, eod=False):
        return frames, eod

    def post_process(self):
        '''

        '''
        aubio_res_id = 'aubio_pitch.pitch_confidence'
        aubio_uuid = self.parents['aubio_pitch'].uuid()
        aubio_results = self.process_pipe.results[aubio_uuid]

        pitch_confidences = aubio_results[aubio_res_id].data

        nb_frameDecision = int(self.decisionLen / self.wStep)
        epsilon = numpy.spacing(pitch_confidences[0])
        w = int(nb_frameDecision/2)

        is_mono = []
        for i in range(w, len(pitch_confidences) - w, nb_frameDecision):
            d = pitch_confidences[i - w:i + w]
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
        conf.data_object.value = pitch_confidences

        self.add_result(conf)

        convert = {False: 0, True: 1}
        label = {0: 'Poly', 1: 'Mono'}
        segList = segmentFromValues(is_mono)
        segs = self.new_result(data_mode='label', time_mode='segment')
        segs.id_metadata.id += '.' + 'segments'
        segs.id_metadata.name += ' ' + 'Segments'

        segs.data_object.label_metadata.label = label
        segs.data_object.label = [convert[s[2]] for s in segList]
        segs.data_object.time = [(float(s[0]+0.5) * self.decisionLen)
                                 for s in segList]

        segs.data_object.duration = [(float(s[1] - s[0]+1) * self.decisionLen)
                                     for s in segList]
        self.add_result(segs)
        return

    def monoLikelihood(self, m, v):

        theta1 = 0.1007
        theta2 = 0.0029
        beta1 = 0.5955
        beta2 = 0.2821
        delta = 0.848
        return self.weibullLikelihood(m, v, theta1, theta2, beta1, beta2,
                                      delta)

    def polyLikelihood(self, m, v):
        theta1 = 0.3224
        theta2 = 0.0121
        beta1 = 1.889
        beta2 = 0.8705
        delta = 0.644
        return self.weibullLikelihood(m, v, theta1, theta2, beta1, beta2,
                                      delta)

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
        Pxy = c0 + (beta1 / delta - 1) * c1 + (beta2 / delta - 1) * c2 +\
            (delta - 2) * numpy.log(b1 + b2) +\
            numpy.log(somme1 + 1 / delta - 1) - somme1

        return numpy.mean(Pxy)
