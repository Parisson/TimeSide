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


class VampSpectralKurtosis(VampAnalyzer):
    """Extract the kurtosis of an audio spectrum"""

    implements(IAnalyzer)

    class _Param(HasTraits):
        pass

    _schema = {'$schema': 'http://json-schema.org/schema#',
               'properties': {},
               'type': 'object'}

    @store_parameters
    def __init__(self):
        super(VampSpectralKurtosis, self).__init__()
        # Define Vamp plugin key and output
        self.plugin_key = 'vamp-libxtract:spectral_kurtosis'
        self.plugin_output = 'spectral_kurtosis'

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(VampSpectralKurtosis, self).setup(
            channels, samplerate, blocksize, totalframes)

        self.spectral_kurtosis = self.plugin.get_parameter_value('spectral_kurtosis')

    @staticmethod
    @interfacedoc
    def id():
        return "vamp_spectral_kurtosis"

    @staticmethod
    @interfacedoc
    def name():
        return "Spectral kurtosis"

    @staticmethod
    @interfacedoc
    def version():
        return "1.0.0"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def post_process(self):
        super(VampSpectralKurtosis, self).post_process()  # get remaining results

        spectral_kurtosis = self.new_result(data_mode='value', time_mode='framewise')
        spectral_kurtosis.data_object.y_value = self.spectral_kurtosis
        spectral_kurtosis.data_object.value = self.vamp_results['matrix'][1]
        self.add_result(spectral_kurtosis)
