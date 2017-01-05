# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Thomas Fillon <thomas@parisson.com>

# This file is part of TimeSide.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author : Thomas Fillon <thomas@parisson.com>
"""
Module Yaafe Analyzer
"""

from timeside.core import implements, interfacedoc
from timeside.core.analyzer import Analyzer
from timeside.core.api import IAnalyzer

import yaafelib
import numpy
from timeside.core.preprocessors import downmix_to_mono
from timeside.core.tools.parameters import HasTraits, ListUnicode, Float
from timeside.core.tools.parameters import store_parameters


class Yaafe(Analyzer):
    """Yaafe feature extraction library interface analyzer

    Parameters
    ----------
    feature_plan : list, optional
        Yaafe feature plan as a list of feature definition,
        default to ['mfcc: MFCC blockSize=512 stepSize=256']
    input_samplerate : int, optional
        The samplerate, default to 32000.

    Examples
    --------
    >>> import timeside
    >>> from timeside.core.tools.test_samples import samples
    >>> from timeside.core import get_processor
    >>> source = samples['C4_scale.wav']
    >>> FileDecoder = get_processor('file_decoder')
    >>> YaafeAnalyzer = get_processor('yaafe')
    >>> # feature extraction defition
    >>> feature_plan = ['mfcc: MFCC CepsIgnoreFirstCoeff=0 blockSize=1024 stepSize=256',
    ...                 'mfccd1: MFCC CepsIgnoreFirstCoeff=0 blockSize=1024 stepSize=256 > Derivate DOrder=1',
    ...                 'mfccd2: MFCC CepsIgnoreFirstCoeff=0 blockSize=1024 stepSize=256 > Derivate DOrder=2',
    ...                 'zcr: ZCR blockSize=1024 stepSize=256']
    >>> decoder = FileDecoder(uri=source)
    >>> yaafe = YaafeAnalyzer(feature_plan=feature_plan,
    ...                       input_samplerate=16000)
    >>> pipe = (decoder | yaafe)
    >>> pipe.run()
    >>> print yaafe.results.keys()
    ['yaafe.mfccd1', 'yaafe.mfcc', 'yaafe.mfccd2', 'yaafe.zcr']
    >>> # Access to one of the result:
    >>> res_mfcc = yaafe.results['yaafe.mfcc']
    >>> print type(res_mfcc.data_object)
    <class 'timeside.core.analyzer.FrameValueObject'>
    >>> res_mfcc.data  # doctest: +ELLIPSIS
    array([[...]])
"""
    implements(IAnalyzer)

    # Define Parameters
    class _Param(HasTraits):

        feature_plan = ListUnicode
        input_samplerate = Float

    _schema = {'$schema': 'http://json-schema.org/schema#',
               'type': 'object',
               'properties': {'feature_plan': {'type': 'array',
                                               'items': {'type': 'string'},
                                               'default': ['mfcc: MFCC blockSize=512 stepSize=256']},
                              'input_samplerate': {'default': 32000,
                                                   'type': 'integer'}
                              }
               }

    @store_parameters
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
        # self.input_samplerate = samplerate
        # self.input_blocksize = blocksize

    @property
    def force_samplerate(self):
        """Yaafe analyzer force the pipe samplerate to match
        the `input_samplerate` parameters
        """
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

if __name__ == "__main__":
    import doctest
    import timeside
    doctest.testmod(timeside.analyzer.externals.yaafe, verbose=True)
