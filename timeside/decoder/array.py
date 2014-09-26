#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2007-2013 Parisson
# Copyright (c) 2007 Olivier Guilyardi <olivier@samalyse.com>
# Copyright (c) 2007-2013 Guillaume Pellerin <pellerin@parisson.com>
# Copyright (c) 2010-2013 Paul Brossier <piem@piem.org>
#
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

# Authors:
# Paul Brossier <piem@piem.org>
# Guillaume Pellerin <yomguy@parisson.com>
# Thomas Fillon <thomas@parisson.com>

from timeside.core import implements, interfacedoc
from timeside.decoder.core import Decoder, IDecoder
import numpy as np


class ArrayDecoder(Decoder):

    """ Decoder taking Numpy array as input"""
    implements(IDecoder)

    output_blocksize = 8 * 1024

    # IProcessor methods

    @staticmethod
    @interfacedoc
    def id():
        return "array_dec"

    def __init__(self, samples, samplerate=44100, start=0, duration=None):
        '''
            Construct a new ArrayDecoder from an numpy array

            Parameters
            ----------
            samples : numpy array of dimension 1 (mono) or 2 (multichannel)
                    if shape = (n) or (n,1) : n samples, mono
                    if shape = (n,m) : n samples with m channels
            start : float
                start time of the segment in seconds
            duration : float
                duration of the segment in seconds
        '''
        super(ArrayDecoder, self).__init__(start=start, duration=duration)

        # Check array dimension
        if samples.ndim > 2:
            raise TypeError('Wrong number of dimensions for argument samples')
        if samples.ndim == 1:
            samples = samples[:, np.newaxis]  # reshape to 2D array

        self.samples = samples.astype('float32')  # Create a 2 dimensions array
        self.input_samplerate = samplerate
        self.input_channels = self.samples.shape[1]

        self.uri = '_'.join(['raw_audio_array',
                            'x'.join([str(dim) for dim in samples.shape]),
                             samples.dtype.type.__name__])
        from .utils import sha1sum_numpy
        self._sha1 = sha1sum_numpy(self.samples)
        self.frames = self.get_frames()

    def setup(self, channels=None, samplerate=None, blocksize=None):

        # the output data format we want
        if blocksize:
            self.output_blocksize = blocksize
        if samplerate:
            self.output_samplerate = int(samplerate)
        if channels:
            self.output_channels = int(channels)

        if self.uri_duration is None:
            self.uri_duration = (len(self.samples) / self.input_samplerate
                                 - self.uri_start)

        if self.is_segment:
            start_index = self.uri_start * self.input_samplerate
            stop_index = start_index + int(np.ceil(self.uri_duration
                                           * self.input_samplerate))
            stop_index = min(stop_index, len(self.samples))
            self.samples = self.samples[start_index:stop_index]

        if not self.output_samplerate:
            self.output_samplerate = self.input_samplerate

        if not self.output_channels:
            self.output_channels = self.input_channels

        self.input_totalframes = len(self.samples)
        self.input_duration = self.input_totalframes / self.input_samplerate
        self.input_width = self.samples.itemsize * 8

    def get_frames(self):
        "Define an iterator that will return frames at the given blocksize"
        nb_frames = self.input_totalframes // self.output_blocksize

        if self.input_totalframes % self.output_blocksize == 0:
            nb_frames -= 1  # Last frame must send eod=True

        for index in xrange(0,
                            nb_frames * self.output_blocksize,
                            self.output_blocksize):
            yield (self.samples[index:index + self.output_blocksize], False)

        yield (self.samples[nb_frames * self.output_blocksize:], True)

    @interfacedoc
    def process(self):
        return self.frames.next()

    # IDecoder methods
    @interfacedoc
    def format(self):
        import re
        base_type = re.search('^[a-z]*', self.samples.dtype.name).group(0)
        return 'audio/x-raw-' + base_type

    @interfacedoc
    def metadata(self):
        return None

    @interfacedoc
    def release(self):
        self.frames = self.get_frames()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
