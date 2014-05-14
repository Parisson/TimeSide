# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Paul Brossier <piem@piem.org>

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

# Author: Paul Brossier <piem@piem.org>
from __future__ import absolute_import

from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from timeside.api import IAnalyzer
from timeside.analyzer.preprocessors import downmix_to_mono, frames_adapter

from aubio import specdesc, pvoc


class AubioSpecdesc(Analyzer):

    """Aubio Spectral Descriptors collection analyzer"""
    implements(IAnalyzer)

    def __init__(self):
        super(AubioSpecdesc, self).__init__()
        self.input_blocksize = 1024
        self.input_stepsize = self.input_blocksize / 4

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(
            AubioSpecdesc,
            self).setup(
            channels,
            samplerate,
            blocksize,
            totalframes)
        self.block_read = 0
        self.pvoc = pvoc(self.input_blocksize, self.input_stepsize)
        self.methods = [
            'default', 'energy', 'hfc', 'complex', 'phase', 'specdiff', 'kl',
            'mkl', 'specflux', 'centroid', 'slope', 'rolloff', 'spread', 'skewness',
            'kurtosis', 'decrease']
        self.specdesc = {}
        self.specdesc_results = {}
        for method in self.methods:
            self.specdesc[method] = specdesc(method, self.input_blocksize)
            self.specdesc_results[method] = []

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_specdesc"

    @staticmethod
    @interfacedoc
    def name():
        return "Spectral Descriptor (aubio)"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    @downmix_to_mono
    @frames_adapter
    def process(self, frames, eod=False):
        fftgrain = self.pvoc(frames)
        for method in self.methods:
            self.specdesc_results[method] += [
                self.specdesc[method](fftgrain)[0]]
        return frames, eod

    def post_process(self):

        # For each method store results in container
        for method in self.methods:
            res_specdesc = self.new_result(data_mode='value',
                                           time_mode='framewise')
            # Set metadata
            res_specdesc.id_metadata.id += '.' + method
            res_specdesc.id_metadata.name = ' ' + method
            res_specdesc.data_object.value = self.specdesc_results[method]

            self.process_pipe.results.add(res_specdesc)
