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

from timeside.core import implements, interfacedoc, abstract
from timeside.core.analyzer import Analyzer
from timeside.core.api import IAnalyzer
from timeside.core.tools.parameters import HasTraits, List
from timeside.core.preprocessors import downmix_to_mono, frames_adapter

from timeside.core.tools.parameters import store_parameters

import vamp
import vampyhost


class VampAnalyzer(Analyzer):

    """Parent Abstract Class for Vamp Analyzer through Vampyhost
    """

    implements(IAnalyzer)
    abstract()

    class _Param(HasTraits):
        pass

    _schema = {'$schema': 'http://json-schema.org/schema#',
               'properties': {},
               'type': 'object'}

    @store_parameters
    def __init__(self):
        super(VampAnalyzer, self).__init__()
        # Define Vamp plugin key and output
        # run vamp.list_plugins() to get the list of
        # available plugins
        # and vamp.get_outputs_of('plugin_key')
        # to get the outputs of the corresponding plugin
        self.plugin_key = None
        self.plugin_output = None
        # Attributes initialize later during setup
        self.plugin = None
        self.out_index = None  # TODO: manage several outputs

        # Process Attribute
        self.frame_index = 0

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(VampAnalyzer, self).setup(
            channels, samplerate, blocksize, totalframes)

        self.plugin = vampyhost.load_plugin(self.plugin_key,
                                            float(self.input_samplerate),
                                            vampyhost.ADAPT_INPUT_DOMAIN +
                                            vampyhost.ADAPT_BUFFER_SIZE +
                                            vampyhost.ADAPT_CHANNEL_COUNT)

        self.out_index = self.plugin.get_output(self.plugin_output)["output_index"]

        if not self.plugin.initialise(self.input_channels,
                                      self.input_stepsize,
                                      self.input_blocksize):
            raise RuntimeError("Vampy-Host failed to initialise plugin %d" % self.plugin_key)

    @staticmethod
    @interfacedoc
    def id():
        return "vamp_analyzer"

    @staticmethod
    @interfacedoc
    def name():
        return "Parent Abstract Class for Vamp Analyzer through Vampyhost"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    @frames_adapter
    def process(self, frames, eod=False):

        timestamp = vampyhost.frame_to_realtime(self.frame_index,
                                                self.input_samplerate)

        self.plugin.process_block(frames.T, timestamp)
        self.frame_index += self.input_stepsize
        return frames, eod

    def post_process(self):
        pass
