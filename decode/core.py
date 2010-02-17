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

import os
import re
import md5
import string
import subprocess
import mutagen

from timeside.decode import *
from timeside.core import *


class SubProcessPipe:

    def __init__(self, command, stdin=None):
        """Read media and stream data through a generator.
        Taken from Telemeta (see http://telemeta.org)"""

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


class DecoderCore(Processor):
    """Defines the main parts of the decoding tools :
    paths, metadata parsing, data streaming thru system command"""

    def __init__(self):
        self.command = 'ffmpeg -i "%s" -f wav - '

    def process(self, source, options=None):
        """Encode and stream audio data through a generator"""

        command = self.command % source
        proc = SubProcessPipe(command)
        return proc.output

        #while True:
            #__chunk = proc.output.read(self.proc.buffer_size)
            #status = proc.poll()
            #if status != None and status != 0:
                #raise ExportProcessError('Command failure:', command, proc)
            #if len(__chunk) == 0:
                #break
            #yield __chunk



