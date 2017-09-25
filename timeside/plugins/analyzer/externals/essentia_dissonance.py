# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Thomas Fillon <thomas@parisson.com>

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

# Author: Thomas Fillon <thomas@parisson.com>

from timeside.core import implements, interfacedoc
from timeside.core.analyzer import Analyzer
from timeside.core.api import IAnalyzer
from timeside.core.tools.parameters import HasTraits, Int
from timeside.core.preprocessors import downmix_to_mono, frames_adapter

import numpy as np
from timeside.core.tools.parameters import store_parameters

import essentia
import essentia.standard
from essentia.standard import Spectrum
from essentia.standard import SpectralPeaks
from essentia.standard import Dissonance
from essentia.standard import Windowing


class Essentia_Dissonance(Analyzer):

    """Dissonance from Essentia"""

    implements(IAnalyzer)

    class _Param(HasTraits):
        input_blocksize = Int()
        input_stepsize = Int()

    _schema = {'$schema': 'http://json-schema.org/schema#',
               'properties': {
                   "input_blocksize": {"type": "integer"},
                   "input_stepsize": {"type": "integer"},
               },
               'type': 'object'}

    @store_parameters
    def __init__(self, input_blocksize=1024, input_stepsize=512):
        super(Essentia_Dissonance, self).__init__()

        self.input_blocksize = input_blocksize
        self.input_stepsize = min(input_stepsize, self.input_blocksize)
        self.windower = Windowing(type='blackmanharris62')
        self.spec_alg = None
        self.spec_peaks_alg = None
        self.dissonance_alg = Dissonance()

        self.dissonance = []

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(Essentia_Dissonance, self).setup(
            channels, samplerate, blocksize, totalframes)
        self.spec_alg = Spectrum(size=self.input_blocksize)
        self.spec_peaks_alg = SpectralPeaks(
            sampleRate=self.input_samplerate,
            maxFrequency=self.input_samplerate / 2,
            minFrequency=0,
            orderBy='frequency')

    @staticmethod
    @interfacedoc
    def id():
        return "essentia_dissonance"

    @staticmethod
    @interfacedoc
    def name():
        return "Dissonance from Essentia"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    @downmix_to_mono
    @frames_adapter
    def process(self, frames, eod=False):
        if not eod:
            w_frame = self.windower(essentia.array(frames.squeeze()))
            spectrum = self.spec_alg(w_frame)
            spec, mags = self.spec_peaks_alg(spectrum)
            self.dissonance.append(self.dissonance_alg(spec, mags))
        return frames, eod

    def post_process(self):

        dissonance = self.new_result(data_mode='value', time_mode='framewise')
        dissonance.data_object.value = self.dissonance
        self.add_result(dissonance)

# Generate Grapher for Essentia dissonance
from timeside.core.grapher import DisplayAnalyzer

DisplayDissonance = DisplayAnalyzer.create(
    analyzer=Essentia_Dissonance,
    result_id='essentia_dissonance',
    grapher_id='grapher_dissonance',
    grapher_name='Dissonance',
    staging=False)
