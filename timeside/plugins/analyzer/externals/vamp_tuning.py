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
from timeside.core.preprocessors import downmix_to_mono, frames_adapter
from timeside.core.tools.parameters import store_parameters

import vamp
import vampyhost
from .vampyhost_wrapper import VampAnalyzer


class VampTuning(VampAnalyzer):

    """Tuning from NNLS Chroma vamp plugins"""

    implements(IValueAnalyzer)

    _schema = {'$schema': 'http://json-schema.org/schema#',
               'properties': {},
               'type': 'object'}

    @store_parameters
    def __init__(self):
        super(VampTuning, self).__init__()
        # Define Vamp plugin key and output
        self.plugin_key = 'nnls-chroma:tuning'
        self.plugin_output = 'tuning'

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(VampTuning, self).setup(
            channels, samplerate, blocksize, totalframes)

    @staticmethod
    @interfacedoc
    def id():
        return "vamp_tuning"

    @staticmethod
    @interfacedoc
    def name():
        return "Tuning"

    @staticmethod
    @interfacedoc
    def unit():
        return "Hz"


    def post_process(self):
        super(VampTuning, self).post_process()
        tuning = self.new_result(data_mode='value', time_mode='global')
        tuning.data_object.value = self.vamp_results['list'][0]['values']
        self.add_result(tuning)
