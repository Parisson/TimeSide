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

from __future__ import division

from timeside.core import Processor, implements, interfacedoc, abstract
from timeside.api import IDecoder


class Decoder(Processor):

    """General abstract base class for Decoder
    """
    implements(IDecoder)
    abstract()

    type = 'decoder'

    mimetype = ''
    output_samplerate = None
    output_channels = None

    def __init__(self, start=0, duration=None):
        super(Decoder, self).__init__()

        self.uri_start = float(start)
        if duration:
            self.uri_duration = float(duration)
        else:
            self.uri_duration = duration

        if start == 0 and duration is None:
            self.is_segment = False
        else:
            self.is_segment = True

    @interfacedoc
    def channels(self):
        return self.output_channels

    @interfacedoc
    def samplerate(self):
        return self.output_samplerate

    @interfacedoc
    def blocksize(self):
        return self.output_blocksize

    @interfacedoc
    def totalframes(self):
        return self.input_totalframes

    @interfacedoc
    def release(self):
        pass

    @interfacedoc
    def mediainfo(self):
        return dict(uri=self.uri,
                    duration=self.uri_duration,
                    start=self.uri_start,
                    is_segment=self.is_segment,
                    samplerate=self.input_samplerate,
                    sha1=self.sha1)

    @property
    def sha1(self):
        return self._sha1

    def __del__(self):
        self.release()

    @interfacedoc
    def encoding(self):
        return self.format().split('/')[-1]

    @interfacedoc
    def resolution(self):
        return self.input_width
