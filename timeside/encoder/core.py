#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2009 Guillaume Pellerin <yomguy@parisson.com>

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

# Author: Guillaume Pellerin <yomguy@parisson.com>

from timeside.core import *
import subprocess

class SubProcessPipe(object):
    """Read media and stream data through a generator.
    Taken from Telemeta (see http://telemeta.org)"""

    def __init__(self, command, stdin=None):
        self.buffer_size = 0xFFFF
        if not stdin:
            stdin =  subprocess.PIPE

        self.proc = subprocess.Popen(command.encode('utf-8'),
                    shell = True,
                    bufsize = self.buffer_size,
                    stdin = stdin,
                    stdout = subprocess.PIPE,
                    close_fds = True)

        self.input = self.proc.stdin
        self.output = self.proc.stdout


class EncoderSubProcessCore(Processor):
    """Defines the main parts of the encoding tools :
    paths, metadata parsing, data streaming thru system command"""

    def core_process(self, command, stdin):
        """Encode and stream audio data through a generator"""

        proc = SubProcessPipe(command, stdin)

        while True:
            __chunk = proc.output.read(proc.buffer_size)
            #status = proc.poll()
            #if status != None and status != 0:
                #raise EncodeProcessError('Command failure:', command, proc)
            if len(__chunk) == 0:
                break
            yield __chunk
