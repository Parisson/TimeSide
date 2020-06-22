# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Paul Brossier <piem@aubio.org>
# Copyright (c) 2020 Guillaume Pellerin <yomguy@parisson.com>

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

import aubio
import numpy as np
from timeside.core import Processor, implements, interfacedoc, abstract
from timeside.core.api import IEncoder

class AubioEncoder(Processor):
    implements(IEncoder)
    abstract()

    type = 'encoder'

    def __init__(self, output, streaming=False, overwrite=False):

        super (AubioEncoder, self).__init__()

        if isinstance(output, str):
            import os.path
            if os.path.isdir(output):
                raise IOError("Encoder output must be a file, not a directory")
            elif os.path.isfile(output) and not overwrite:
                raise IOError(
                    "Encoder output %s exists, but overwrite set to False")
            self.filename = output
        else:
            self.filename = None
        self.streaming = streaming

        if not self.filename and not self.streaming:
            raise Exception('Must give an output')

        self.eod = False
        self.metadata = None
        self.num_samples = 0

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None,
            totalframes=None):
        super(AubioEncoder, self).setup(
            channels, samplerate, blocksize, totalframes)
        print ('setting up aubio with with', samplerate, blocksize)

        self.sink = aubio.sink(self.filename, samplerate, channels)

    @interfacedoc
    def release(self):
        if hasattr (self, 'sink'):
            self.sink.close()
            delattr(self, 'sink')

    @interfacedoc
    def set_metadata(self, metadata):
        self.metadata = metadata

    @interfacedoc
    def process(self, frames, eod=False):
        self.eod = eod
        max_write = 4096
        indices = range(max_write, frames.shape[0], max_write)
        for f_slice in np.array_split(frames, indices):
            write_frames = f_slice.shape[0]
            self.sink.do_multi(f_slice.T, write_frames)
            self.num_samples += write_frames
        return frames, eod
