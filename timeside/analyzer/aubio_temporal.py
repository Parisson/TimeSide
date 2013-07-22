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


class AubioTemporal(Processor):
    implements(IAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(AubioTemporal, self).setup(channels, samplerate, blocksize, totalframes)
        self.win_s = 1024
        self.hop_s = 256
        self.o = onset("default", self.win_s, self.hop_s, samplerate)
        self.t = tempo("default", self.win_s, self.hop_s, samplerate)
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
        for samples in downsample_blocking(frames, self.hop_s):
            if self.o(samples):
                self.onsets += [self.o.get_last_s()]
            if self.t(samples):
                self.beats += [self.t.get_last_s()]
            self.block_read += 1
        return frames, eod

    def results(self):
        # Get common metadata
        commonAttr = dict(samplerate=self.samplerate(),
                          blocksize=self.win_s,
                          stepsize=self.hop_s)
        # FIXME : Onsets, beat and onset rate are not frame based Results
        # samplerate, blocksize, etc. are not appropriate here
        # Those might be some kind of "AnalyzerSegmentResults"

        # list of onset locations
        onsets = AnalyzerResult()
        # Set metadata
        onsetsAttr = dict(id="aubio_onset",
                          name="onsets (aubio)",
                          unit="s")
        onsets.metadata = dict(onsetsAttr.items() + commonAttr.items())
        # Set Data
        onsets.data = self.onsets

        # list of inter-onset intervals, in beats per minute
        onsetrate = AnalyzerResult()
        # Set metadata
        onsetrateAttr = dict(id="aubio_onset_rate",
                             name="onset rate (aubio)",
                             unit="bpm")
        onsetrate.metadata = dict(onsetrateAttr.items() + commonAttr.items())
        # Set Data
        if len(self.onsets) > 1:
            periods = 60. / numpy.diff(self.onsets)
            onsetrate.data = periods
        else:
            onsetrate.data = []

        # list of beat locations
        beats = AnalyzerResult()
        # Set metadata
        beatsAttr = dict(id="aubio_beat",
                        name="beats (aubio)",
                        unit="s")
        beats.metadata = dict(beatsAttr.items() + commonAttr.items())
        #  Set Data
        beats.data = self.beats

        # list of inter-beat intervals, in beats per minute
        bpm = AnalyzerResult()
        # Set metadata
        bpmAttr = dict(id="aubio_bpm",
                       name="bpm (aubio)",
                       unit="bpm")
        bpm.metadata = dict(bpmAttr.items() + commonAttr.items())
        #  Set Data
        if len(self.beats) > 1:
            periods = 60. / numpy.diff(self.beats)
            bpm.data = periods
        else:
            bpm.data = []

        return AnalyzerResultContainer([onsets, onsetrate, beats, bpm])
