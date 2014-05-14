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
from . utils import peaks, interpolate_colors
from timeside.grapher.waveform_simple import Waveform
from timeside.grapher.color_schemes import default_color_schemes


class WaveformCentroid(Waveform):

    """ Builds a PIL image representing a waveform of the audio stream.
    Peaks are colored relatively to the spectral centroids of each frame buffer. """

    implements(IGrapher)

    @interfacedoc
    def __init__(self, width=1024, height=256, bg_color=(0, 0, 0), color_scheme='default'):
        super(WaveformCentroid, self).__init__(
            width, height, bg_color, color_scheme)
        self.lower_freq = 200
        colors = default_color_schemes[color_scheme]['waveform']
        self.color_lookup = interpolate_colors(colors)

    @staticmethod
    @interfacedoc
    def id():
        return "waveform_centroid"

    @staticmethod
    @interfacedoc
    def name():
        return "Waveform spectral"

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(WaveformCentroid, self).setup(
            channels, samplerate, blocksize, totalframes)

    @interfacedoc
    def process(self, frames, eod=False):
        if len(frames) != 1:
            buffer = frames[:, 0].copy()
            buffer.shape = (len(buffer), 1)
            for samples, end in self.pixels_adapter.process(buffer, eod):
                if self.pixel_cursor < self.image_width:
                    (spectral_centroid, db_spectrum) = self.spectrum.process(
                        samples, True)
                    line_color = self.color_lookup[
                        int(spectral_centroid * 255.0)]
                    self.draw_peaks(
                        self.pixel_cursor, peaks(samples), line_color)
                    self.pixel_cursor += 1
        return frames, eod
