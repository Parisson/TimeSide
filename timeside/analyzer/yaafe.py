# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Thomas Fillon <thomas@parisson.com>

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

# Author : Thomas Fillon <thomas@parisson.com>
"""
Module Yaafe Analyzer
"""

from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from timeside.api import IAnalyzer

import yaafelib
import numpy
from timeside.analyzer.preprocessors import downmix_to_mono
from ..tools.parameters import HasTraits, ListUnicode, Float


class Yaafe(Analyzer):
    """Yaafe feature extraction library interface analyzer"""
    implements(IAnalyzer)

    # Define Parameters
    class _Param(HasTraits):

        feature_plan = ListUnicode
        input_samplerate = Float

    def __init__(self, feature_plan=None, input_samplerate=32000):
        super(Yaafe, self).__init__()

        if input_samplerate is None:
            self.input_samplerate = 0
        else:
            self.input_samplerate = input_samplerate

        # Check arguments
        if feature_plan is None:
            feature_plan = ['mfcc: MFCC blockSize=512 stepSize=256']

        self.feature_plan = feature_plan
        self.yaafe_engine = None

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(Yaafe, self).setup(channels, samplerate, blocksize, totalframes)

        # Setup Yaafe Feature plan and Dataflow
        yaafe_feature_plan = yaafelib.FeaturePlan(sample_rate=samplerate)
        for feat in self.feature_plan:
            yaafe_feature_plan.addFeature(feat)

        self.data_flow = yaafe_feature_plan.getDataFlow()

        # Configure a YAAFE engine
        self.yaafe_engine = yaafelib.Engine()
        self.yaafe_engine.load(self.data_flow)
        self.yaafe_engine.reset()
        #self.input_samplerate = samplerate
        #self.input_blocksize = blocksize

    @property
    def force_samplerate(self):
        return self.input_samplerate

    @staticmethod
    @interfacedoc
    def id():
        return "yaafe"

    @staticmethod
    @interfacedoc
    def name():
        return "Yaafe Descriptor"

    @staticmethod
    @interfacedoc
    def unit():
        return ''

    @downmix_to_mono
    def process(self, frames, eod=False):
        # do process things...
        # Convert to float64and reshape
        # for compatibility with Yaafe engine
        yaafe_frames = frames.astype(numpy.float64).reshape(1, -1)

        # write audio array on 'audio' input
        self.yaafe_engine.writeInput('audio', yaafe_frames)
        # process available data
        self.yaafe_engine.process()
        if eod:
            # flush yaafe engine to process remaining data
            self.yaafe_engine.flush()

        return frames, eod

    def post_process(self):
        # Get feature extraction results from yaafe
        featNames = self.yaafe_engine.getOutputs().keys()
        if len(featNames) == 0:
            raise KeyError('Yaafe engine did not return any feature')
        for featName in featNames:

            result = self.new_result(data_mode='value', time_mode='framewise')
            result.id_metadata.id += '.' + featName
            result.id_metadata.name += ' ' + featName
            # Read Yaafe Results
            result.data_object.value = self.yaafe_engine.readOutput(featName)

            yaafe_metadata = self.yaafe_engine.getOutputs()[featName]
            result.data_object.frame_metadata.blocksize = yaafe_metadata['frameLength']
            result.data_object.frame_metadata.stepsize = yaafe_metadata['sampleStep']
            result.data_object.frame_metadata.samplerate = yaafe_metadata['sampleRate']

            # Store results in Container
            if len(result.data_object.value):
                self.add_result(result)
