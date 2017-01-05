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

# Author: Paul Brossier <piem@piem.org>

from timeside.core import implements, interfacedoc
from timeside.core.analyzer import Analyzer
from timeside.core.api import IAnalyzer
from timeside.core.tools.parameters import HasTraits, List

import subprocess
import tempfile
import numpy as np
from timeside.core.tools.parameters import store_parameters


def simple_host_process(argslist):
    """Call vamp-simple-host"""

    vamp_host = 'vamp-simple-host'
    command = [vamp_host]
    command.extend(argslist)
    # try ?
    stdout = subprocess.check_output(command,
                                     stderr=subprocess.STDOUT).splitlines()

    return stdout


# Raise an exception if Vamp Host is missing
from timeside.core.exceptions import VampImportError
try:
    simple_host_process(['-v'])
    WITH_VAMP = True
except OSError:
    WITH_VAMP = False
    raise VampImportError


def get_plugins_list():
    arg = ['--list-outputs']
    stdout = simple_host_process(arg)

    return [line.split(':')[1:] for line in stdout]


class VampSimpleHost(Analyzer):

    """Vamp plugins library interface analyzer"""

    implements(IAnalyzer)

    class _Param(HasTraits):
        plugin_list = List

    _schema = {'$schema': 'http://json-schema.org/schema#',
               'properties': {'plugin_list': {'default': get_plugins_list(),
                                              'type': 'array',
                                              'items': {'type': 'array',
                                                        'items': {'type': 'string'}}
                                              }
                              },
               'type': 'object'}

    @store_parameters
    def __init__(self, plugin_list=None):
        super(VampSimpleHost, self).__init__()
        if plugin_list is None:
            plugin_list = get_plugins_list()
            #plugin_list = [['vamp-example-plugins', 'percussiononsets', 'detectionfunction']]

        self.plugin_list = plugin_list

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(VampSimpleHost, self).setup(
            channels, samplerate, blocksize, totalframes)

    @staticmethod
    @interfacedoc
    def id():
        return "vamp_simple_host"

    @staticmethod
    @interfacedoc
    def name():
        return "Vamp Plugins host"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def process(self, frames, eod=False):
        pass
        return frames, eod

    def post_process(self):
        #plugin = 'vamp-example-plugins:amplitudefollower:amplitude'

        wavfile = self.mediainfo()['uri'].split('file://')[-1]

        for plugin_line in self.plugin_list:

            plugin = ':'.join(plugin_line)
            (time, duration, value) = self.vamp_plugin(plugin, wavfile)
            if value is None:
                return

            if duration is not None:
                plugin_res = self.new_result(
                    data_mode='value', time_mode='segment')
                plugin_res.data_object.duration = duration
            else:
                plugin_res = self.new_result(
                    data_mode='value', time_mode='event')

            plugin_res.data_object.time = time
            plugin_res.data_object.value = value

# Fix strat, duration issues if audio is a segment
#            if self.mediainfo()['is_segment']:
#                start_index = np.floor(self.mediainfo()['start'] *
#                                       self.result_samplerate /
#                                       self.result_stepsize)
#
#                stop_index = np.ceil((self.mediainfo()['start'] +
#                                      self.mediainfo()['duration']) *
#                                     self.result_samplerate /
#                                     self.result_stepsize)
#
#                fixed_start = (start_index * self.result_stepsize /
#                               self.result_samplerate)
#                fixed_duration = ((stop_index - start_index) * self.result_stepsize /
#                                  self.result_samplerate)
#
#                plugin_res.audio_metadata.start = fixed_start
#                plugin_res.audio_metadata.duration = fixed_duration
#
#                value = value[start_index:stop_index + 1]
            plugin_res.id_metadata.id += '.' + '.'.join(plugin_line[1:])
            plugin_res.id_metadata.name += ' ' + \
                ' '.join(plugin_line[1:])

            self.add_result(plugin_res)

    @staticmethod
    def vamp_plugin(plugin, wavfile):
        def get_vamp_result(txt_file):
            # Guess format
            time_, value_ = np.genfromtxt(txt_file, delimiter=':', dtype=str,
                                          unpack=True)
            time_duration = np.genfromtxt(np.array(time_).ravel(),
                                          delimiter=',',
                                          dtype=float, unpack=True)

            if len(time_duration.shape) <= 1:
                time = time_duration
            if len(time_duration.shape) == 2:
                time = time_duration[:, 0]
                duration = time_duration[:, 1]
            else:
                duration = None

            if value_.size == 1 and value_ == '':
                value = None
            elif value_.size > 1 and (value_ == '').all():
                value = None
            else:
                value = np.genfromtxt(np.array(value_).ravel(), delimiter=' ',
                                      invalid_raise=False)
                value = np.atleast_2d(value)
                if np.isnan(value[:, -1]).all():
                    value = value[:, 0:-1]

            return (time, duration, value)

        vamp_output_file = tempfile.NamedTemporaryFile(suffix='_vamp.txt',
                                                       delete=False)
        args = [plugin, wavfile, '-o', vamp_output_file.name]

        stderr = simple_host_process(args)  # run vamp-simple-host

        # Parse stderr to get blocksize and stepsize
        blocksize_info = stderr[4]

        import re
        # Match agianst pattern 'Using block size = %d, step size = %d'
        m = re.match(
            'Using block size = (\d+), step size = (\d+)', blocksize_info)

        blocksize = int(m.groups()[0])
        stepsize = int(m.groups()[1])
        # Get the results

        return get_vamp_result(vamp_output_file)
