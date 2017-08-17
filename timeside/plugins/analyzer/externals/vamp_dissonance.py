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
from timeside.core.tools.parameters import HasTraits, List
from timeside.core.preprocessors import downmix_to_mono, frames_adapter

import numpy as np
from timeside.core.tools.parameters import store_parameters

import vamp
import vampyhost


class VampDissonance(Analyzer):

    """Dissonance from Essentia through vamp plugins"""

    implements(IAnalyzer)

    class _Param(HasTraits):
        plugin_list = List

    _schema = {'$schema': 'http://json-schema.org/schema#',
               'properties': {},
               'type': 'object'}

    @store_parameters
    def __init__(self):
        super(VampDissonance, self).__init__()

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(VampDissonance, self).setup(
            channels, samplerate, blocksize, totalframes)

        self.plugin_key = 'libvamp_essentia:Dissonance_12'
        self.plugin_output = 'Dissonance_13'
        
        self.plugin = vampyhost.load_plugin(self.plugin_key, float(self.input_samplerate),
                                   vampyhost.ADAPT_INPUT_DOMAIN +
                                   vampyhost.ADAPT_BUFFER_SIZE +
                                   vampyhost.ADAPT_CHANNEL_COUNT)

        self.frame_index = 0
        self.out_index = self.plugin.get_output(self.plugin_output)["output_index"]

        if not self.plugin.initialise(self.input_channels, self.input_stepsize, self.input_blocksize):
            raise "Failed to initialise plugin"

    @staticmethod
    @interfacedoc
    def id():
        return "vamp_dissonance"

    @staticmethod
    @interfacedoc
    def name():
        return "Dissonace from Essentia through Vamp plugin"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    @frames_adapter
    def process(self, frames, eod=False):
        timestamp = vampyhost.frame_to_realtime(self.frame_index, self.input_samplerate)
        
        self.plugin.process_block(frames.T, timestamp)
        # results is a dict mapping output number -> list of feature dicts
        #if out_index in results:
        #    for r in results[out_index]:
                
        self.frame_index += self.input_stepsize
        return frames, eod

    def post_process(self):
        results = self.plugin.get_remaining_features()[self.out_index]#[0]
        self.plugin.unload()
        print results
        dissonance = self.new_result(data_mode='value', time_mode='global')
        dissonance.data_object.value = results['values'][0]
        self.add_result(dissonance)

        
        #    (time, duration, value) = self.vamp_plugin(plugin, wavfile)
        # if value is None:
        #     return
        
        # if duration is not None:
        #     plugin_res = self.new_result(
        #         data_mode='value', time_mode='segment')
        #     plugin_res.data_object.duration = duration
        # else:
        #     plugin_res = self.new_result(
        #         data_mode='value', time_mode='event')
            
        # plugin_res.data_object.time = time
        #     plugin_res.data_object.value = value
            
