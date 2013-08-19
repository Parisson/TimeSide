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

from timeside.core import Processor, implements, interfacedoc, FixedSizeInputAdapter
from timeside.analyzer.core import *
from timeside.api import IAnalyzer
from aubio import onset, tempo


class AubioTemporal(Analyzer):
    implements(IAnalyzer)

    def __init__(self):
        self.input_blocksize = 1024
        self.input_stepsize = 256

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(AubioTemporal, self).setup(channels, samplerate, blocksize, totalframes)
        self.o = onset("default", self.input_blocksize, self.input_stepsize, samplerate)
        self.t = tempo("default", self.input_blocksize, self.input_stepsize, samplerate)
        self.block_read = 0
        self.onsets = []
        self.beats = []

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_temporal"

    @staticmethod
    @interfacedoc
    def name():
        return "onsets (aubio)"

    @staticmethod
    @interfacedoc
    def unit():
        return "seconds"

    def __str__(self):
        return "%s %s" % (str(self.value), unit())

    def process(self, frames, eod=False):
        for samples in downsample_blocking(frames, self.input_stepsize):
            if self.o(samples):
                self.onsets += [self.o.get_last_s()]
            if self.t(samples):
                self.beats += [self.t.get_last_s()]
            self.block_read += 1
        return frames, eod

    def results(self):

        container = super(AubioTemporal, self).results()

        #---------------------------------
        #  Onsets
        #---------------------------------
        onsets = self.new_result(dataMode='label', resultType='event')

        onsets.idMetadata.id = "aubio_onset"
        onsets.idMetadata.name = "onsets (aubio)"
        onsets.idMetadata.unit = 's'

        # Set Data , dataMode='label', resultType='event'
        # Event = list of (time, labelId)
        onsets.data.data = [(time,1) for time in self.onsets]

        onsets.labelMetadata.label = {1: 'Onset'}

        container.add_result(onsets)

        #---------------------------------
        #  Onset Rate
        #---------------------------------
        onsetrate = self.new_result(dataMode='value', resultType='event')
        # Set metadata
        onsetrate.idMetadata.id = "aubio_onset_rate"
        onsetrate.idMetadata.name = "onset rate (aubio)"
        onsetrate.idMetadata.unit = "bpm"

        # Set Data , dataMode='value', resultType='event'
        # Event = list of (time, value)
        if len(self.onsets) > 1:
            periods = 60. / numpy.diff(self.onsets)
            onsetrate.data.data = zip(periods,self.onsets[:-1])
        else:
            onsetrate.data.data = []

        container.add_result(onsetrate)

        #---------------------------------
        #  Beats
        #---------------------------------
        beats = self.new_result(dataMode='label', resultType='segment')
        # Set metadata
        beats.idMetadata.id="aubio_beat"
        beats.idMetadata.name="beats (aubio)"
        beats.idMetadata.unit="s"

        #  Set Data, dataMode='label', resultType='segment'
        # Segment = list of (time, duration, labelId)
        if len(self.beats) > 1:
            duration = numpy.diff(self.beats)
            duration = numpy.append(duration,duration[-1])
            beats.data.data = [(time,dur,1) for (time, dur) in zip(self.beats, duration)]
        else:
            beats.data.data = []
        beats.labelMetadata.label = {1: 'Beat'}

        container.add_result(beats)

        #---------------------------------
        #  BPM
        #---------------------------------
        bpm = self.new_result(dataMode='value', resultType='segment')
        # Set metadata
        bpm.idMetadata.id="aubio_bpm"
        bpm.idMetadata.name="bpm (aubio)"
        bpm.idMetadata.unit="bpm"

        #  Set Data, dataMode='value', resultType='segment'
        if len(self.beats) > 1:
            periods = 60. / numpy.diff(self.beats)
            periods = numpy.append(periods,periods[-1])

            bpm.data.data = zip(self.beats, duration, periods)

        else:
            bpm.data.data = []

        container.add_result(bpm)

        return container
