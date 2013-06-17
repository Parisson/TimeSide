# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Maxime Le Coz <lecoz@irit.fr>

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

# Author: Maxime Le Coz <lecoz@irit.fr>

from timeside.core import Processor, implements, interfacedoc, FixedSizeInputAdapter
from timeside.analyzer.core import *
from timeside.api import IValueAnalyzer
from numpy import array,hamming,dot,mean
from numpy.fft import rfft
from scipy.ndimage.morphology import binary_opening
from scipy.signal import firwin,lfilter
from scipy.io.wavfile import write as wavwrite
from matplotlib import pylab

class IRITSpeech4Hz(Processor):
    implements(IValueAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        super(IRITSpeech4Hz, self).setup(channels, samplerate, blocksize, totalframes)
        self.energy4hz = []
        self.threshold = 2.0
        self.smoothLen = 5
        self.fCenter = 4.0
        self.normalizeEnergy = True
        self.nFFT=2048
        self.orderFilter=100
        self.nbFilters =30
        self.modulLen = 2
        self.fwidth = 0.5
        self.melFilter = melFilterBank(self.nbFilters,self.nFFT,samplerate);
    @staticmethod
    @interfacedoc
    def id():
        return "irit_speech_4hz"

    @staticmethod
    @interfacedoc
    def name():
        return "Speech entropy (IRIT)"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def __str__(self):
        return "Speech confidences indexes"

    def process(self, frames, eod=False):
		'''
		
		'''
		
		frames = frames.T[0]
		w = frames * hamming(len(frames));
		f = abs(rfft(w,n=2*self.nFFT)[0:self.nFFT])
		e = dot(f**2,self.melFilter)
		self.energy4hz.append(e)
		return frames, eod
        
    def results(self):
		'''
		
		'''		
		#wavwrite('out.wav',self.fe,(numpy.array(self.data)*2**15).astype(numpy.int16))
		
		Wo = self.fCenter/self.samplerate()  ;
		Wn = [ Wo-(self.fwidth/2)/self.samplerate() , Wo+(self.fwidth/2)/self.samplerate()];
		num = firwin(self.orderFilter, Wn,pass_zero=False);
		self.energy4hz=numpy.array(self.energy4hz)
		energy = lfilter(num,1,self.energy4hz.T,0)
		energy = sum(energy)
		
		if self.normalizeEnergy :
			energy =energy/mean(energy)
			
		
		w= int(float(self.modulLen)*self.samplerate()/self.blocksize())
		modEnergyValue =computeModulation(energy,w,True)
				
		conf = array(modEnergyValue-self.threshold)/self.threshold
		conf[conf>1] = 1

		modEnergy = AnalyzerResult(id = "irit_4hzenergy_confidence", name = "modulation energie (IRIT)", unit = "?")
		modEnergy.value = conf
		convert = {False:'NonSpeech',True:'Speech'}
		
		segList = segmentFromValues(modEnergyValue>self.threshold)
		segmentsEntropy =[]
		for s in segList : 
			segmentsEntropy.append((s[0],s[1],convert[s[2]]))
		segs = AnalyzerResult(id = "irit_4hzenergy_segments", name = "seg 4Hz (IRIT)", unit = "s")
		segs.value = segmentsEntropy
		return AnalyzerResultContainer([modEnergy,segs])
