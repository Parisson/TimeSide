# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Paul Brossier <piem@piem.org>

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
#  Paul Brossier <piem@piem.org>
#  Thomas Fillon <thomas@parisson.com>

from __future__ import absolute_import

from timeside.core import implements, interfacedoc
from timeside.core.analyzer import Analyzer
from timeside.core.api import IAnalyzer
from timeside.core.preprocessors import downmix_to_mono, frames_adapter
from aubio import filterbank, pvoc


class AubioMelEnergy(Analyzer):

    """Aubio Mel Energy analyzer"""
    implements(IAnalyzer)

    def __init__(self):
        super(AubioMelEnergy, self).__init__()
        self.input_blocksize = 1024
        self.input_stepsize = self.input_blocksize / 4

        # Aubio Melenergy Initialisation
        self.n_filters = 40
        self.n_coeffs = 13
        self.pvoc = pvoc(self.input_blocksize, self.input_stepsize)
        self.melenergy = filterbank(self.n_filters, self.input_blocksize)
        self.block_read = 0
        self.melenergy_results = []

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(AubioMelEnergy, self).setup(channels, samplerate,
                                          blocksize, totalframes)

        self.melenergy.set_mel_coeffs_slaney(samplerate)

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_melenergy"

    @staticmethod
    @interfacedoc
    def name():
        return "Mel Energy (aubio)"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    @downmix_to_mono
    @frames_adapter
    def process(self, frames, eod=False):

        # WARNING : All Aubio analyzer process functions manages frames reconstruction by themself
        #           from small stepsize input blocksize
        #           i.e. Aubio process functions should receive non overlapping input blocksize
        #           of length stepsize.
        #           This is achieve through  @frames_adapter that handles Aubio Analyzer specifically (blocksize=stepsize).

        fftgrain = self.pvoc(frames)
        self.melenergy_results.append(self.melenergy(fftgrain))
        self.block_read += 1
        return frames, eod

    def post_process(self):
        melenergy = self.new_result(data_mode='value', time_mode='framewise')
        melenergy.parameters = dict(n_filters=self.n_filters,
                                    n_coeffs=self.n_coeffs)
        melenergy.data_object.value = self.melenergy_results
        self.add_result(melenergy)
