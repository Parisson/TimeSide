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

from timeside.core.api import IAnalyzer
from timeside.core.tools.parameters import HasTraits


from timeside.core.tools.parameters import store_parameters

import vamp
import vampyhost
from .vampyhost_wrapper import VampAnalyzer

import numpy as np


def midi2freq(midi_number, tuningA4=440):
    """
    Given a MIDI pitch number, returns its frequency in Hz.
    """
    MIDI_A4 = 69
    return tuningA4 * 2 ** ((midi_number - MIDI_A4) * (1. / 12.))


class VampConstantQ(VampAnalyzer):
    """Constant Q transform from QMUL vamp plugins"""

    implements(IAnalyzer)

    class _Param(HasTraits):
        pass

    _schema = {'$schema': 'http://json-schema.org/schema#',
               'properties': {},
               'type': 'object'}

    @store_parameters
    def __init__(self):
        super(VampConstantQ, self).__init__()
        # Define Vamp plugin key and output
        self.plugin_key = 'qm-vamp-plugins:qm-constantq'
        self.plugin_output = 'constantq'

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(VampConstantQ, self).setup(
            channels, samplerate, blocksize, totalframes)

        self.minpitch = self.plugin.get_parameter_value('minpitch')
        self.maxpitch = self.plugin.get_parameter_value('maxpitch')
        self.bpo = self.plugin.get_parameter_value('bpo')
        self.tuning = self.plugin.get_parameter_value('tuning')

    @staticmethod
    @interfacedoc
    def id():
        return "vamp_constantq"

    @staticmethod
    @interfacedoc
    def name():
        return "Constant Q transform from QMUL vamp plugins"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def post_process(self):
        super(VampConstantQ, self).post_process()  # get remaining results

        constant_q = self.new_result(data_mode='value', time_mode='framewise')

        midi_pitches = np.arange(self.minpitch, self.maxpitch, 12.0 / self.bpo)
        constant_q.data_object.y_value = [midi2freq(midi_number=p, tuningA4=self.tuning)
                                          for p in midi_pitches]

        constant_q.data_object.value = self.vamp_results['matrix'][1]
        self.add_result(constant_q)


# Generate Grapher for CQT analyzer
from timeside.core.grapher import DisplayAnalyzer

DisplayCQT = DisplayAnalyzer.create(
    analyzer=VampConstantQ,
    result_id='vamp_constantq',
    grapher_id='grapher_vamp_cqt',
    grapher_name='Constant Q Transform',
    staging=False)
