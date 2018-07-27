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
from aubio import pitch as aubio_pitch
import numpy as np
from timeside.plugins.analyzer.utils import nextpow2

from timeside.core.tools.parameters import store_parameters, Float, HasTraits


class AubioPitch(Analyzer):

    """Aubio Pitch estimation analyzer"""
    implements(IAnalyzer)  # TODO check if needed with inheritance

    # Define Parameters
    class _Param(HasTraits):
        blocksize_s = Float
        stepsize_s = Float

    _schema = {'$schema': 'http://json-schema.org/schema#',
               'properties': {'blocksize_s': {'default': 2048 / 44100.,
                                              'type': 'number'},
                              'stepsize_s': {'default': 1024 / 44100.,
                                             'type': 'number'}},
               'type': 'object'}

    @store_parameters
    def __init__(self, blocksize_s=None, stepsize_s=None):

        super(AubioPitch, self).__init__()

        self._blocksize_s = blocksize_s
        self._stepsize_s = stepsize_s

        # Aubio Pitch Initialisation
        self.aubio_pitch = None
        self.block_read = 0
        self.pitches = []
        self.pitch_confidences = []

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        # Frame parameters setup
        if self._blocksize_s:
            self.input_blocksize = nextpow2(self._blocksize_s * samplerate)
        else:
            self.input_blocksize = 2048

        if self._stepsize_s:
            self.input_stepsize = int(np.round(self._stepsize_s * samplerate))
        else:
            self.input_stepsize = self.input_blocksize / 2

        # Now that frames size metadata are properly set, we can do the set-up
        super(AubioPitch, self).setup(channels,
                                      samplerate,
                                      blocksize,
                                      totalframes)

        # Aubio Pitch set-up
        self.aubio_pitch = aubio_pitch("default", self.input_blocksize,
                                       self.input_stepsize, samplerate)
        self.aubio_pitch.set_unit("freq")

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_pitch"

    @staticmethod
    @interfacedoc
    def name():
        return "f0 (aubio)"

    @staticmethod
    @interfacedoc
    def unit():
        return "Hz"

    def __str__(self):
        return "pitch values"

    @downmix_to_mono
    @frames_adapter
    def process(self, frames, eod=False):

        #time = self.block_read * self.input_stepsize * 1. / self.samplerate()

        # WARNING : All Aubio analyzer process functions manages frames reconstruction by themself
        #           from small stepsize input blocksize
        #           i.e. Aubio process functions should receive non overlapping input blocksize
        #           of length stepsize.
        #           This is achieve through  @frames_adapter that handles Aubio Analyzer specifically (blocksize=stepsize).

        self.pitches += [self.aubio_pitch(frames)[0]]
        self.pitch_confidences += [self.aubio_pitch.get_confidence()]
        self.block_read += 1
        return frames, eod

    def post_process(self):
        pitch = self.new_result(data_mode='value', time_mode='framewise')

        # parameters : None # TODO check with Piem "default" and "freq" in
        # setup

        pitch.id_metadata.id += '.' + "pitch"
        pitch.id_metadata.name += ' ' + "pitch"
        pitch.id_metadata.unit = "Hz"
        pitch.data_object.value = self.pitches
        self.add_result(pitch)

        pitch_confidence = self.new_result(
            data_mode='value', time_mode='framewise')
        pitch_confidence.id_metadata.id += '.' + "pitch_confidence"
        pitch_confidence.id_metadata.name += ' ' + "pitch confidence"
        pitch_confidence.id_metadata.unit = None
        pitch_confidence.data_object.value = self.pitch_confidences
        self.add_result(pitch_confidence)


# Generate Grapher for Aubio Pitch analyzer
from timeside.core.grapher import DisplayAnalyzer
DisplayAubioPitch = DisplayAnalyzer.create(
    analyzer=AubioPitch,
    result_id='aubio_pitch.pitch',
    grapher_id='grapher_aubio_pitch',
    grapher_name='Pitch',
    background='spectrogram')
