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
from __future__ import absolute_import

from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from timeside.api import IAnalyzer
from timeside.analyzer.preprocessors import downmix_to_mono, frames_adapter
from aubio import onset, tempo

import numpy


class AubioTemporal(Analyzer):

    """Aubio Temporal analyzer"""
    implements(IAnalyzer)

    def __init__(self):
        super(AubioTemporal, self).__init__()
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
        self.beat_confidences = []

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

    @downmix_to_mono
    @frames_adapter
    def process(self, frames, eod=False):
        if self.o(frames):
            self.onsets += [self.o.get_last_s()]
        if self.t(frames):
            self.beats += [self.t.get_last_s()]
            self.beat_confidences += [self.t.get_confidence()]
        self.block_read += 1
        return frames, eod

    def post_process(self):

        #---------------------------------
        #  Onsets: Event (time, "Onset")
        #---------------------------------
        onsets = self.new_result(data_mode='label', time_mode='event')
        onsets.id_metadata.id += '.' + 'onset'
        onsets.id_metadata.name += ' ' + 'Onset'
        onsets.id_metadata.unit = 's'
        onsets.data_object.time = self.onsets
        onsets.data_object.label = numpy.ones(len(self.onsets))
        onsets.label_metadata.label = {1: 'Onset'}

        self.process_pipe.results.add(onsets)

        #---------------------------------
        #  Onset Rate: Segment (time, duration, value)
        #---------------------------------
        onsetrate = self.new_result(data_mode='value', time_mode='segment')
        onsetrate.id_metadata.id += '.' + "onset_rate"
        onsetrate.id_metadata.name = " " + "Onset Rate"
        onsetrate.id_metadata.unit = "bpm"
        if len(self.onsets) > 1:
            periods = numpy.diff(self.onsets)
            periods = numpy.append(periods, periods[-1])
            onsetrate.data_object.time = self.onsets
            onsetrate.data_object.duration = periods
            onsetrate.data_object.value = 60. / periods
        else:
            onsetrate.data_object.value = []
            onsetrate.data_object.time = []

        self.process_pipe.results.add(onsetrate)

        #---------------------------------
        #  Beats: Event (time, "Beat")
        #---------------------------------
        beats = self.new_result(data_mode='label', time_mode='event')
        beats.id_metadata.id += '.' + "beat"
        beats.id_metadata.name += " " + "Beats"
        beats.id_metadata.unit = "s"
        beats.data_object.time = self.beats
        beats.data_object.label = numpy.ones(len(self.beats))
        beats.label_metadata.label = {1: 'Beat'}

        self.process_pipe.results.add(beats)

        #---------------------------------
        #  Beat confidences: Event (time, value)
        #---------------------------------
        beat_confidences = self.new_result(
            data_mode='value', time_mode='event')
        beat_confidences.id_metadata.id += '.' + "beat_confidence"
        beat_confidences.id_metadata.name += " " + "Beat confidences"
        beat_confidences.id_metadata.unit = None
        beat_confidences.data_object.time = self.beats
        beat_confidences.data_object.value = self.beat_confidences

        self.process_pipe.results.add(beat_confidences)

        #---------------------------------
        #  BPM: Segment (time, duration, value)
        #---------------------------------
        bpm = self.new_result(data_mode='value', time_mode='segment')
        bpm.id_metadata.id += '.' + "bpm"
        bpm.id_metadata.name += ' ' + "bpm"
        bpm.id_metadata.unit = "bpm"
        if len(self.beats) > 1:
            periods = numpy.diff(self.beats)
            periods = numpy.append(periods, periods[-1])
            bpm.data_object.time = self.beats
            bpm.data_object.duration = periods
            bpm.data_object.value = 60. / periods
        else:
            bpm.data_object.value = []

        self.process_pipe.results.add(bpm)
