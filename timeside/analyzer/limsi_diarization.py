# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 David Doukhan <doukhan@limsi.fr>

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

# Author: David Doukhan <doukhan@limsi.fr>


from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from timeside.api import IAnalyzer
# from timeside.analyzer import IRITSpeech4Hz
from yaafe import Yaafe
import yaafelib
from timeside.analyzer.limsi_sad import LimsiSad
import numpy as N
import sys

from pyannote.features.audio.yaafe import YaafeFrame
from pyannote.core.feature import SlidingWindowFeature
from pyannote.core import Annotation, Segment
from pyannote.algorithms.clustering.bic import BICClustering

# import time


def gauss_div(data, winsize):
    ret = []
    for i in xrange(winsize , len(data) - winsize +1):
        w1 = data[(i-winsize):i,:]
        w2 = data[i:(i+winsize),:]
        meandiff = N.mean(w1, axis = 0) - N.mean(w2, axis = 0)
        invstdprod = 1. / (N.std(w1, axis = 0) * N.std(w2, axis = 0))
        ret.append(N.sum(meandiff * meandiff * invstdprod))
    
    return ret


def segment(data, minsize):

    if len(data) == 0:
        return []

    am = N.argmax(data)
    if am <= minsize:
        ret1 = ([0] * am)
    else:
        ret1 = segment(data[:(am-minsize)], minsize) + ([0] * minsize)
    if (am + minsize - 1)>= len(data):
        ret2 = ([0] * (len(data) -am -1))
    else:
        ret2 = ([0] * minsize) + segment(data[(am+minsize+1):], minsize)
    return (ret1 + [1] + ret2)


class LimsiDiarization(Analyzer):
    implements(IAnalyzer)

    def __init__(self, sad_analyzer = None, gdiff_win_size_sec=5., min_seg_size_sec=2.5, bic_penalty_coeff=0.5):
        super(LimsiDiarization, self).__init__()

        self.gdiff_win_size_sec = gdiff_win_size_sec
        self.min_seg_size_sec = min_seg_size_sec
        self.bic_penalty_coeff = bic_penalty_coeff

        if sad_analyzer is None:
            sad_analyzer = LimsiSad('etape')
        self.sad_analyzer = sad_analyzer
        self.parents.append(sad_analyzer)

        # feature extraction defition
        spec = yaafelib.FeaturePlan(sample_rate=16000)
        spec.addFeature('mfccchop: MFCC CepsIgnoreFirstCoeff=0 blockSize=1024 stepSize=256')
        parent_analyzer = Yaafe(spec)        
        self.parents.append(parent_analyzer)

        # informative parameters
        # these are not really taken into account by the system
        # these are bypassed by yaafe feature plan
        self.input_blocksize = 1024
        self.input_stepsize = 256


    @staticmethod
    @interfacedoc
    def id():
        return "limsi_diarization"

    @staticmethod
    @interfacedoc
    def name():
        return "Limsi diarization system"

    @staticmethod
    @interfacedoc
    def unit():
        # return the unit of the data dB, St, ...
        return "Speaker Id"

    def process(self, frames, eod=False):
        if self.input_samplerate != 16000:
            raise Exception('%s requires 16000 input sample rate: %d provided' % (self.__class__.__name__, self.input_samplerate))
        return frames, eod

    def post_process(self):
        mfcc = self.process_pipe.results['yaafe.mfccchop']['data_object']['value']

        sw = YaafeFrame(self.input_blocksize, self.input_stepsize, self.input_samplerate)
        pyannotefeat = SlidingWindowFeature(mfcc, sw)     

        # speech activity detection: usefull for debugging purpose only
        # print 'adding sad res to result'
        # sadres = self.new_result(data_mode='value', time_mode='framewise')
        # sadres.id_metadata.id += '.' + 'sadres'
        # sadres.id_metadata.name += ' ' + 'SAD RESULT'
        sadval = self.process_pipe.results[self.sad_analyzer.id() + '.sad_lhh_diff'].data_object.value[:]
        # sadres.data_object.value = sadval
        # self.process_pipe.results.add(sadres)

        # gaussian divergence window size
        #winframesize = int((self.input_samplerate / self.input_stepsize) * self.chop_window_size)
        timestepsize = self.input_stepsize / float(self.input_samplerate)
        gdiff_win_size_frame = int(self.gdiff_win_size_sec / timestepsize)
        min_seg_size_frame = int(self.min_seg_size_sec / timestepsize)
        # print 'timestepsize %d, gdiffwinsize (sec: %f, frame: %d) , minsegsize (sec: %f, frame: %d)' % (timestepsize, self.gdiff_win_size_sec, gdiff_win_size_frame, self.min_seg_size_sec, min_seg_size_frame)
        

        # basic gauss div
        #bgd = (range(0, len(mfcc)), 'basicgdiv')
        # speech gauss div
        sgd = ([i for i, val in enumerate(sadval) if val > 0], 'speechgdiv')
        # speech above threshold
        #thres = N.percentile([val for val in sadval if val > 0], 25)
        #sat = ([i for i, val in enumerate(sadval) if val > thres], 'speechthreshold25p')

#        for frameids, name in [bgd, sgd, sat]:
        for frameids, name in [sgd]:

            gdiff = gauss_div(mfcc[frameids,:], gdiff_win_size_frame)

            # debug purpose only
            # res = self.new_result(data_mode='value', time_mode='event')
            # res.id_metadata.id += ('.%s' % name)
            # res.id_metadata.name += (' %s' % name)
            # res.data_object.value = N.array(gdiff)
            # res.data_object.time = N.array(frameids[gdiff_win_size_frame:(1-gdiff_win_size_frame)]) * timestepsize
            # self.process_pipe.results.add(res)

            seg = segment(gdiff, min_seg_size_frame)
            # seg_result = self.new_result(data_mode='value', time_mode='event')
            # seg_result.id_metadata.id += '.' + name + 'segchop'
            # seg_result.id_metadata.name += ' ' + name + 'seg chop'
            # seg_result.data_object.value = N.array(seg)
            # seg_result.data_object.time = N.array(frameids[gdiff_win_size_frame:(1-gdiff_win_size_frame)]) * timestepsize
            # self.process_pipe.results.add(seg_result)

            # build pyannote annotation
            # print 'building annotation'
            #b = time.time()
            chunks = Annotation()
            fbegin = None
            #fend = None
            lastframe = None
            ichunk = 0
            for segval, iframe in zip(seg, frameids):
                if segval == 1:
                    if lastframe is not None:
                        chunks[pyannotefeat.sliding_window.rangeToSegment(fbegin, iframe-fbegin)] = str(ichunk)
                        ichunk += 1
                    fbegin= iframe
                elif iframe -1 != lastframe:
                    if lastframe is not None:
                        chunks[pyannotefeat.sliding_window.rangeToSegment(fbegin, lastframe-fbegin+1)] = str(ichunk)
                    fbegin= iframe
                lastframe = iframe
            if lastframe != fbegin:
                chunks[pyannotefeat.sliding_window.rangeToSegment(fbegin, lastframe-fbegin+1)] = str(ichunk)
            # print 'chunks', chunks
            #print 'anotation build in', (time.time() - b)

            bicClustering = BICClustering(covariance_type='full', penalty_coef=self.bic_penalty_coeff)
            hypothesis = bicClustering(chunks, feature=pyannotefeat)

            # gen result interval
            #print 'gen result interval'
            diar_res = self.new_result(data_mode='label', time_mode='segment')
            diar_res.id_metadata.id += '.' + 'speakers' # + name + 'diarisation'
            diar_res.id_metadata.name += ' ' + 'speaker identifiers' # name + 'diarisation'

            tmplabel = [int(h[2]) for h in hypothesis.itertracks(True)]
            tmptime = [h[0].start for h in hypothesis.itertracks()]
            tmpduration = [h[0].duration for h in hypothesis.itertracks()]

            label = []
            time = []
            duration = []
            lastlabel = None

            for l, t, d in zip(tmplabel, tmptime, tmpduration):
                if l != lastlabel:
                    label.append(l)
                    duration.append(d)
                    time.append(t)
                else:
                    duration[-1] = t + d - time[-1]
                lastlabel = l


            diar_res.data_object.label = label
            diar_res.data_object.time = time
            diar_res.data_object.duration = duration
            diar_res.label_metadata.label = dict()
            for lab in diar_res.data_object.label:
                diar_res.label_metadata.label[lab] = str(lab)
            # TODO FIXME
            # for h in hypothesis.itertracks(label=True):
            #     diar_res.data_object.label.append(h[2])
            #     diar_res.data_object.time.append(h[0].start)
            #     diar_res.data_object.duration.apeend(h[0].duration)
            #sadres.data_object.value = sadval
            self.process_pipe.results.add(diar_res)
