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
Created on Thu Jun 13 16:05:02 2013

@author: Thomas Fillon
"""
from timeside.core import Processor, implements, interfacedoc, FixedSizeInputAdapter
from timeside.analyzer.core import *
from timeside.api import IValueAnalyzer
#
from yaafelib import *
#
import numpy

class Yaafe(Processor):
    implements(IValueAnalyzer)
    def __init__(self, yaafeSpecification):
        # Check arguments
        if isinstance(yaafeSpecification,DataFlow):
            self.dataFlow = yaafeSpecification
        elif isinstance(yaafeSpecification,FeaturePlan):
            self.featurePlan = yaafeSpecification
            self.dataFlow = self.featurePlan.getDataFlow()
        else:
            raise TypeError("'%s' Type must be either '%s' or '%s'" % (str(yaafeSpecification),str(DataFlow),str(FeaturePlan)))
        
    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(Yaafe, self).setup(channels, samplerate, blocksize, totalframes)
        # Configure a YAAFE engine
        self.yaafe_engine = Engine()
        self.yaafe_engine.load(self.dataFlow)
        self.yaafe_engine.reset()

    @staticmethod
    @interfacedoc
    def id():
        return "yaafe"

    @staticmethod
    @interfacedoc
    def name():
        return "Yaafe Descriptor"

    def process(self, frames, eod=False):
        # do process things...
        # Downmixing to mono and convert to float64 for compatibility with Yaafe       
        yaafe_frames = frames.sum(axis=-1,dtype=numpy.float64) / frames.shape[-1]
        # Reshape for compatibility with Yaafe input format        
        yaafe_frames.shape = (1,yaafe_frames.shape[0]) 
        # write audio array on 'audio' input
        self.yaafe_engine.writeInput('audio',yaafe_frames) 
        # process available data        
        self.yaafe_engine.process() 
        if eod:
            # flush yaafe engine to process remaining data
            self.yaafe_engine.flush() 
           
        return frames, eod

    def results(self):
        # Get back current container
        container = AnalyzerResultContainer()
        # Get feature extraction results from yaafe
        map_keys = {'sampleRate': 'sampleRate',
                    'frameLength': 'blockSize',
                    'sampleStep': 'stepSize', 
                    'parameters': 'parameters', 
                    }
        featNames = self.yaafe_engine.getOutputs().keys()
        for featName in featNames:
            # Map Yaafe attributes into AnalyzerResults dict
            res_dict = {map_keys[name]: self.yaafe_engine.getOutputs()['mfcc'][name] for name in map_keys.keys()}
            # Define ID fields            
            res_dict['id'] = 'yaafe_' + featName
            res_dict['name'] = 'Yaafe ' + featName
            res_dict['unit'] = ''
            # create AnalyzerResult and set its attributes
            result = AnalyzerResult(attributes=res_dict)
            # Get results from Yaafe engine
            result.data = self.yaafe_engine.readOutput(featName)  # Read Yaafe Results       
            # Store results in Container
            if len(result.data):
                container.add_result(result)
        
        return container




