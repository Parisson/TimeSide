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

from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from timeside.api import IAnalyzer

import subprocess
import numpy as np


def simple_host_process(argslist):
    """Call vamp-simple-host"""

    vamp_host = 'vamp-simple-host'
    command = [vamp_host]
    command.extend(argslist)
    # try ?
    stdout = subprocess.check_output(
        command, stderr=subprocess.STDOUT).splitlines()

    return stdout


# Raise an exception if Vamp Host is missing
from ..exceptions import VampImportError
try:
    simple_host_process(['-v'])
    WITH_VAMP = True
except OSError:
    WITH_VAMP = False
    raise VampImportError


class VampSimpleHost(Analyzer):

    """Vamp plugins library interface analyzer"""

    implements(IAnalyzer)

    def __init__(self, plugin_list=None):
        super(VampSimpleHost, self).__init__()
        if plugin_list is None:
            plugin_list = self.get_plugins_list()
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

            self.process_pipe.results.add(plugin_res)

    @staticmethod
    def vamp_plugin(plugin, wavfile):

        args = [plugin, wavfile]

        stdout = simple_host_process(args)  # run vamp-simple-host

        stderr = stdout[0:8]  # stderr containing file and process information
        res = stdout[8:]  # stdout containg the feature data

        if len(res) == 0:
            return ([], [], [])

        # Parse stderr to get blocksize and stepsize
        blocksize_info = stderr[4]

        import re
        # Match agianst pattern 'Using block size = %d, step size = %d'
        m = re.match(
            'Using block size = (\d+), step size = (\d+)', blocksize_info)

        blocksize = int(m.groups()[0])
        stepsize = int(m.groups()[1])
        # Get the results

        value = np.asfarray([line.split(': ')[1].split(' ')
                            for line in res if (len(line.split(': ')) > 1)])
        time = np.asfarray([r.split(':')[0].split(',')[0] for r in res])

        time_len = len(res[0].split(':')[0].split(','))
        if time_len == 1:
            # event
            duration = None
        elif time_len == 2:
            # segment
            duration = np.asfarray(
                [r.split(':')[0].split(',')[1] for r in res])

        return (time, duration, value)

    @staticmethod
    def get_plugins_list():
        arg = ['--list-outputs']
        stdout = simple_host_process(arg)

        return [line.split(':')[1:] for line in stdout]
