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
from __future__ import absolute_import


from timeside.analyzer.utils import segmentFromValues
from timeside.core import Processor, implements, interfacedoc, FixedSizeInputAdapter
from timeside.analyzer.core import Analyzer
from timeside.analyzer.preprocessors import frames_adapter
from timeside.api import IAnalyzer
from aubio import pitch
import numpy
from scipy.signal import firwin,lfilter
from scipy.ndimage.morphology import binary_opening,binary_closing
import pylab




class IRITStartSeg(Analyzer):
    implements(IAnalyzer)
    '''
    Segmentor MOnophony/Polyphony based on the analalysis of yin confidence.

    Properties:
    '''

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):

        super(IRITStartSeg, self).setup(channels,
                                      samplerate,
                                      blocksize,
                                      totalframes)
        lowFreq = 100.0

        self.input_blocksize = int(0.02 * samplerate)
        self.input_stepsize = int(0.008 * samplerate)


        sr = float(samplerate)
        highFreq = sr/2
        f1= lowFreq/sr
        f2= highFreq/sr
        self.filtre = firwin(10, [f1,f2], pass_zero=False)
        self.energy = []
        self.maxenergy = 0.002
        self.min_overlap = 20
        self.threshold = 0.1
    @staticmethod
    @interfacedoc
    def id():
        return "irit_startseg"

    @staticmethod
    @interfacedoc
    def name():
        return "IRIT Monophony / Polyphony classification"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def __str__(self):
        return "Labeled Monophonic/Polyphonic segments"

    @frames_adapter
    def process(self, frames, eod=False):
        '''

        '''

        self.energy += [numpy.sqrt(numpy.mean(lfilter(self.filtre,1.0,frames.T[0])**2))]
        return frames, eod

    def post_process(self):
        '''

        '''
        self.energy = numpy.array(self.energy)/max(self.energy)
        silences = numpy.zeros((1,len(self.energy)))[0]
        silences[self.energy<self.maxenergy] = 1

        step = float(self.input_stepsize) / float(self.samplerate())
        tL = numpy.arange(len(silences))*step

        prototype = numpy.load('timeside/analyzer/protoStart2.dat')
        prototype2 = numpy.load('timeside/analyzer/protoStart3.dat')
        # Lissage pour éliminer les petits segments dans un sens ou l'autre
        struct= [1]*len(prototype)
        silences = binary_closing(silences, struct)
        silences = binary_opening(silences, struct)
        seg = [0,-1,silences[0]]
        silencesList = []
        for i,v in enumerate(silences) :
            if not (v == seg[2]) :
                seg[1] = i
                silencesList.append(tuple(seg))
                seg = [i,-1,v]
        seg[1] = i
        silencesList.append(tuple(seg))
        segsList = []
        candidates = []
        l = len(prototype)
        #import pylab
        for s in silencesList :
			if s[2] == 1 :
				shape = numpy.array(self.energy[s[0]:s[1]])
				#shape = shape/numpy.max(shape)

				d1,_ = computeDist2(prototype,shape)
				d2,_ = computeDist2(prototype2,shape)
				dist = min([d1,d2])

				candidates.append((s[0],s[1],dist))
				#pylab.plot(shape)
				#pylab.plot(range(decal,decal+l),prototype)
				#pylab.show()
				if dist < self.threshold :
					segsList.append(s)

        label = {0: 'Start',1:'Session'}
        with open('out.lab','w') as f :
            for s in segsList :
				f.write('%.2f\t%.2f\t%s\n'%(s[0]*step,s[1]*step,label[s[2]]))

        with open('cand.lab','w') as f :
            for s in candidates :
				f.write('%.2f\t%.2f\t%f\n'%(s[0]*step,s[1]*step,s[2]))

        segs = self.new_result(data_mode='label', time_mode='segment')
        segs.id_metadata.id += '.' + 'segments'
        segs.id_metadata.name += ' ' + 'Segments'
        segs.label_metadata.label = label
        segs.data_object.label = [s[2] for s in segsList]
        segs.data_object.time = [(float(s[0])*step)
                                  for s in segsList]
        segs.data_object.duration = [(float(s[1]-s[0])*step)
                                  for s in segsList]
        self.process_pipe.results.add(segs)


def computeDist2(proto,serie) :
	l = len(proto)
	r=  range(len(serie))
	serie = numpy.array(list(serie)+[0]*(l-1))
	v = [numpy.mean(numpy.abs((serie[i:i+l]/numpy.max(serie[i:i+l]))-proto))for i in r]
	return numpy.min(v),numpy.argmin(v)

def computeDist(v1,v2,min_overlap):
		'''

		'''
		m1 = numpy.argmax(v1)
		m2 = numpy.argmax(v2)
		l1 = len(v1)
		l2 = len(v2)
		decal = numpy.abs(m1-m2)

		if m1  >= m2 :
			fin = numpy.min([l1-decal,l2])
			if fin-decal > min_overlap:

				v1_out = numpy.array(v1[decal:decal+fin])
				v2_out = numpy.array(v2[:fin])
				d = numpy.mean(numpy.abs(v1_out-v2_out))
			else :
				v1_out = [0]
				v2_out = [1]
				d = 1
		else :
			return computeDist(v2, v1,min_overlap)


		return d,v1_out,v2_out

