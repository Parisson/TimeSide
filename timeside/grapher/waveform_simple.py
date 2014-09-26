# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2010 Guillaume Pellerin <yomguy@parisson.com>
# Copyright (c) 2010 Olivier Guilyardi <olivier@samalyse.com>

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


from timeside.core import implements, interfacedoc
from timeside.api import IGrapher
from timeside.grapher.core import Grapher
from . utils import peaks


class Waveform(Grapher):

    """ Builds a PIL image representing a simple waveform of the audio stream.
    """

    implements(IGrapher)

    @interfacedoc
    def __init__(self, width=1024, height=256, bg_color=(255, 255, 255), color_scheme='default'):
        super(Waveform, self).__init__(width, height, bg_color, color_scheme)
        self.line_color = (0, 0, 0)

    @staticmethod
    @interfacedoc
    def id():
        return "waveform_simple"

    @staticmethod
    @interfacedoc
    def name():
        return "Waveform simple"

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(Waveform, self).setup(
            channels, samplerate, blocksize, totalframes)

    @interfacedoc
    def process(self, frames, eod=False):
        if len(frames) != 1:
            if len(frames.shape) > 1:
                buffer = frames[:, 0]
            else:
                buffer = frames
            buffer.shape = (len(buffer), 1)
            for samples, end in self.pixels_adapter.process(buffer, eod):
                if self.pixel_cursor < self.image_width - 1:
                    self.draw_peaks(
                        self.pixel_cursor, peaks(samples), self.line_color)
                    self.pixel_cursor += 1
            if self.pixel_cursor == self.image_width - 1:
                self.draw_peaks(
                    self.pixel_cursor, peaks(samples), self.line_color)
                self.pixel_cursor += 1
        return frames, eod

    @interfacedoc
    def post_process(self, output=None):
        a = 1
        for x in range(self.image_width):
            self.pixel[x, self.image_height / 2] = tuple(
                map(lambda p: p + a, self.pixel[x, self.image_height / 2]))
