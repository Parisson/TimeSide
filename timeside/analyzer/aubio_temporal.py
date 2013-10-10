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
from utils import downsample_blocking
from aubio import onset, tempo

import numpy


class AubioTemporal(Analyzer):
    implements(IAnalyzer)

    def __init__(self):
        self.input_blocksize = 1024
        self.input_stepsize = 256

    @interfacedoc
    def setup(self,
              channels=None,
              samplerate=None,
              blocksize=None,
              totalframes=None):
        super(AubioTemporal, self).setup(
            channels, samplerate, blocksize, totalframes)
        self.o = onset(
            "default", self.input_blocksize, self.input_stepsize, samplerate)
        self.t = tempo(
            "default", self.input_blocksize, self.input_stepsize, samplerate)
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
        return ""

    def __str__(self):
        return "%s %s" % (str(self.value), self.unit())

    def process(self, frames, eod=False):
        for samples in downsample_blocking(frames, self.input_stepsize):
            if self.o(samples):
                self.onsets += [self.o.get_last_s()]
            if self.t(samples):
                self.beats += [self.t.get_last_s()]
            self.block_read += 1
        return frames, eod

    def release(self):

        #---------------------------------
        #  Onsets
        #---------------------------------
        onsets = self.new_result(dataMode='label', timeMode='event')

        onsets.idMetadata.id += '.' + 'onset'
        onsets.idMetadata.name += ' ' + 'Onset'
        onsets.idMetadata.unit = 's'

        # Set Data , dataMode='label', timeMode='event'
        # Event = list of (time, labelId)

        onsets.dataObject.label = numpy.ones(len(self.onsets))
        onsets.dataObject.time = self.onsets

        onsets.labelMetadata.label = {1: 'Onset'}

        self._results.add(onsets)

        #---------------------------------
        #  Onset Rate
        #---------------------------------
        onsetrate = self.new_result(dataMode='value', timeMode='event')
        # Set metadata
        onsetrate.idMetadata.id += '.' + "onset_rate"
        onsetrate.idMetadata.name = " " + "Onset Rate"
        onsetrate.idMetadata.unit = "bpm"

        # Set Data , dataMode='value', timeMode='event'
        # Event = list of (time, value)
        # TODO : add time
        if len(self.onsets) > 1:
            onsetrate.dataObject.value = 60. / numpy.diff(self.onsets)
            onsetrate.dataObject.time = self.onsets[:-1]
        else:
            onsetrate.dataObject.value = []

        self._results.add(onsetrate)

        #---------------------------------
        #  Beats
        #---------------------------------
        beats = self.new_result(dataMode='label', timeMode='segment')
        # Set metadata
        beats.idMetadata.id += '.' + "beat"
        beats.idMetadata.name += " " + "Beats"
        beats.idMetadata.unit = "s"

        #  Set Data, dataMode='label', timeMode='segment'
        # Segment = list of (time, duration, labelId)
        if len(self.beats) > 1:
            duration = numpy.diff(self.beats)
            duration = numpy.append(duration, duration[-1])
            beats.dataObject.time = self.beats
            beats.dataObject.duration = duration
            beats.dataObject.label = numpy.ones(len(self.beats))
        else:
            beats.dataObject.label = []

        beats.labelMetadata.label = {1: 'Beat'}

        self._results.add(beats)

        #---------------------------------
        #  BPM
        #---------------------------------
        bpm = self.new_result(dataMode='value', timeMode='segment')
        # Set metadata
        bpm.idMetadata.id += '.' + "bpm"
        bpm.idMetadata.name += ' ' + "bpm"
        bpm.idMetadata.unit = "bpm"

        #  Set Data, dataMode='value', timeMode='segment'
        if len(self.beats) > 1:
            periods = 60. / numpy.diff(self.beats)
            periods = numpy.append(periods, periods[-1])

            bpm.dataObject.time = self.beats
            bpm.dataObject.duration = duration
            bpm.dataObject.value = periods

        else:
            bpm.dataObject.value = []

        self._results.add(bpm)
