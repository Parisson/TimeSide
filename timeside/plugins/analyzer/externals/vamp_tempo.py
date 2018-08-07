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
from timeside.core.api import IValueAnalyzer
#from timeside.core.tools.parameters import HasTraits
from timeside.core.preprocessors import downmix_to_mono, frames_adapter

from timeside.core.tools.parameters import store_parameters

import vamp
import vampyhost
from .vampyhost_wrapper import VampAnalyzer


class VampTempo(VampAnalyzer):

    """Tempo from QMUL vamp plugins"""

    implements(IValueAnalyzer)

    _schema = {'$schema': 'http://json-schema.org/schema#',
               'properties': {},
               'type': 'object'}

    @store_parameters
    def __init__(self):
        super(VampTempo, self).__init__()
        # Define Vamp plugin key and output
        self.plugin_key = 'qm-vamp-plugins:qm-tempotracker'
        self.plugin_output = 'tempo'

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(VampTempo, self).setup(
            channels, samplerate, blocksize, totalframes)

    @staticmethod
    @interfacedoc
    def id():
        return "vamp_tempo"

    @staticmethod
    @interfacedoc
    def name():
        return "Tempo"

    @staticmethod
    @interfacedoc
    def unit():
        return "bpm"

    def post_process(self):
        super(VampTempo, self).post_process()
        tempo = self.new_result(data_mode='value', time_mode='global')
        if self.vamp_results['list']:
            tempo.data_object.value = self.vamp_results['list'][0]['values']
        self.add_result(tempo)
