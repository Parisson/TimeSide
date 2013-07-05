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
        # Get common attributes
        commonAttr = dict(sampleRate=self.samplerate(),
                          blockSize=self.win_s,
                          stepSize=self.hop_s)
       # FIXME : Onsets, beat and onset rate are not frame based Results
        # sampleRate, blockSize, etc. are not appropriate here
        # Those might be some kind of "AnalyzerSegmentResults"

        #---------------------------------
        #  Onsets
        #---------------------------------
        onsets = AnalyzerResult()
        # Set attributes
        onsetsAttr = dict(id="aubio_onset",
                          name="onsets (aubio)",
                          unit="s")
        onsets.attributes = dict(onsetsAttr.items() + commonAttr.items())
        # Set Data
        onsets.data = self.onsets

        #---------------------------------
        #  Onset Rate
        #---------------------------------
        onsetRate = AnalyzerResult()
        # Set attributes
        onsetRateAttr = dict(id="aubio_onset_rate",
                             name="onset rate (aubio)",
                             unit="bpm")
        onsetRate.attributes = dict(onsetRateAttr.items() + commonAttr.items())
        # Set Data
        if len(self.onsets) > 1:
            #periods = [60./(b - a) for a,b in zip(self.onsets[:-1],self.onsets[1:])]
            periods = 60. / numpy.diff(self.onsets)
            onsetRate.data = periods
        else:
            onsetRate.data = []

        #---------------------------------
        #  Beats
        #---------------------------------
        beats = AnalyzerResult()
        # Set attributes
        beatsAttr = dict(id="aubio_beat",
                        name="beats (aubio)",
                        unit="s")
        beats.attributes = dict(beatsAttr.items() + commonAttr.items())
        #  Set Data
        beats.data = self.beats

        #---------------------------------
        #  BPM
        #---------------------------------
        bpm = AnalyzerResult()
        # Set attributes
        bpmAttr = dict(id="aubio_bpm",
                       name="bpm (aubio)",
                       unit="bpm")
        bpm.attributes = dict(bpmAttr.items() + commonAttr.items())
        #  Set Data
        if len(self.beats) > 1:
            #periods = [60./(b - a) for a,b in zip(self.beats[:-1],self.beats[1:])]
            periods = 60. / numpy.diff(self.beats)
            bpm.data = periods
        else:
            bpm.data = []

        return AnalyzerResultContainer([onsets, onsetRate, beats, bpm])