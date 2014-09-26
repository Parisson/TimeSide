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

from timeside.core import implements, interfacedoc, get_processor
from timeside.analyzer.core import Analyzer
from timeside.api import IAnalyzer
import timeside

import yaafelib
import numpy as np
import pickle
import os.path


class GMM:
    """
    Gaussian Mixture Model
    """
    def __init__(self, weights, means, vars):
        self.weights = weights
        self.means = means
        self.vars = vars

    def llh(self, x):
        n_samples, n_dim = x.shape
        llh = -0.5 * (n_dim * np.log(2 * np.pi) + np.sum(np.log(self.vars), 1)
                      + np.sum((self.means ** 2) / self.vars, 1)
                      - 2 * np.dot(x, (self.means / self.vars).T)
                      + np.dot(x ** 2, (1.0 / self.vars).T))
        + np.log(self.weights)
        m = np.amax(llh,1)
        dif = llh - np.atleast_2d(m).T
        return m + np.log(np.sum(np.exp(dif),1))


def slidewinmap(lin, winsize, func):
    """
    map a function to a list of elements using a sliding window
    the window is centered on the element to process
    missing values required by the windows corresponding to the beginning, or end
    of the signal are replaced with the first, or last, element of the list

    Parameters:
    ----------
    lin: input (list)
    winsize: size of the sliding windows in samples (int)
    func: function to be mapped on sliding windows
    """
    tmpin = ([lin[0]] * (winsize/2)) + list(lin) + ([lin[-1]] * (winsize -1 - winsize/2))
    lout = []
    for i in xrange(len(lin)):
        lout.append(func(tmpin[i:(i+winsize)]))
    assert(len(lin) == len(lout))
    return lout

def dilatation(lin, winsize):
    """
    morphological dilation
    """
    return slidewinmap(lin, winsize, max)

def erosion(lin, winsize):
    """
    morphological erosion
    """
    return slidewinmap(lin, winsize, min)


class LimsiSad(Analyzer):
    """
    Limsi Speech Activity Detection Systems
    LimsiSad performs frame level speech activity detection based on trained GMM models
    For each frame, it computes the log likelihood difference between a speech model and a non speech model. 
    The highest is the estimate, the largest is the probability that the frame corresponds to speech.
    Dilatation and erosion procedures are used in a latter stage to obtain speech and non speech segments

    The analyser outputs 3 result structures:
    * sad_lhh_diff: the raw frame level speech/non speech log likelihood difference
    * sad_de_lhh_diff: frame level speech/non speech log likelihood difference
      altered with erosion and dilatation procedures
    * sad_segments: speech/non speech segments
    """
    implements(IAnalyzer)
    

    def __init__(self, sad_model, dews=0.2, speech_threshold=1., dllh_bounds=(-10., 10.)):
        """
        Parameters:
        ----------

        sad_model : string bellowing to ['etape', 'maya']
          Allows the selection of trained speech activity detection models.
          * 'etape' models were trained on data distributed in the framework of the
            ETAPE campaign (http://www.afcp-parole.org/etape.html)
            These models are suited for radionews material (0.974 AUC on Etape data)
          * 'maya' models were obtained on data collected by EREA – Centre
            Enseignement et Recherche en Ethnologie Amerindienne
            These models are suited to speech obtained in noisy environments
            (0.915 AUC on Maya data)


        dews: dilatation and erosion window size (seconds)
          This value correspond to the size in seconds of the sliding window
          used to perform a dilation followed by an erosion procedure
          these procedures consist to output the max (respectively the min) of the
          speech detection estimate. The order of these procedures is aimed at removing
          non-speech frames corresponding to fricatives or short pauses
          The size of the windows correspond to the minimal size of the resulting
          speech/non speech segments

        speech_threshold: threshold used for speech/non speech decision
          based on the log likelihood difference

        dllh_bounds: raw log likelihood difference estimates will be bound
          according this (min_llh_difference, max_llh_difference) tuple
          Usefull for plotting log likelihood differences
          if set to None, no bounding will be done
        """
        super(LimsiSad, self).__init__()

        # feature extraction defition
        spec = yaafelib.FeaturePlan(sample_rate=16000)
        spec.addFeature(
            'mfcc: MFCC CepsIgnoreFirstCoeff=0 blockSize=1024 stepSize=256')
        spec.addFeature(
            'mfccd1: MFCC CepsIgnoreFirstCoeff=0 blockSize=1024 stepSize=256 > Derivate DOrder=1')
        spec.addFeature(
            'mfccd2: MFCC CepsIgnoreFirstCoeff=0 blockSize=1024 stepSize=256 > Derivate DOrder=2')
        spec.addFeature('zcr: ZCR blockSize=1024 stepSize=256')
        parent_analyzer = get_processor('yaafe')(spec)
        self.parents['yaafe'] = parent_analyzer

        # informative parameters
        # these are not really taken into account by the system
        # these are bypassed by yaafe feature plan
        self.input_blocksize = 1024
        self.input_stepsize = 256

        # load gmm model
        if sad_model not in ['etape', 'maya']:
            raise ValueError(
                "argument sad_model %s not supported. Supported values are 'etape' or 'maya'" % sad_model)
        picfname = os.path.join(
            timeside.__path__[0], 'analyzer', 'trained_models', 'limsi_sad_%s.pkl' % sad_model)
        self.gmms = pickle.load(open(picfname, 'rb'))

        self.dews = dews
        self.speech_threshold = speech_threshold
        self.dllh_bounds = dllh_bounds

    @staticmethod
    @interfacedoc
    def id():
        return "limsi_sad"

    @staticmethod
    @interfacedoc
    def name():
        return "Limsi speech activity detection system"

    @staticmethod
    @interfacedoc
    def unit():
        # return the unit of the data dB, St, ...
        return "Log Probability difference"

    @property
    def force_samplerate(self):
        return 16000

    def process(self, frames, eod=False):
        return frames, eod

    def post_process(self):
        # extract signal features
        yaafe_result = self.process_pipe.results[self.parents['yaafe'].uuid()]
        mfcc = yaafe_result['yaafe.mfcc']['data_object']['value']
        mfccd1 = yaafe_result['yaafe.mfccd1']['data_object']['value']
        mfccd2 = yaafe_result['yaafe.mfccd2']['data_object']['value']
        zcr = yaafe_result['yaafe.zcr']['data_object']['value']
        features = np.concatenate((mfcc, mfccd1, mfccd2, zcr), axis=1)

        # compute log likelihood difference
        res = 0.5 + 0.5 * (self.gmms[0].llh(features) - self.gmms[1].llh(features))

        # bounds log likelihood difference
        if self.dllh_bounds is not None:
            mindiff, maxdiff = self.dllh_bounds
            res = np.minimum(np.maximum(res,  mindiff), maxdiff)

        # performs dilation, erosion, erosion, dilatation
        ws = int(self.dews * float(self.input_samplerate ) / self.input_stepsize)
        deed_llh = dilatation(erosion(erosion(dilatation(res, ws), ws), ws), ws)

        # infer speech and non speech segments from dilated
        # and erroded likelihood difference estimate
        last = None
        labels = []
        times = []
        durations = []
        for i, val in enumerate([1 if e > self.speech_threshold else 0 for e in deed_llh]):
            if val != last:
                labels.append(val)
                durations.append(1)
                times.append(i)
            else:
                durations[-1] += 1
            last = val
        times = [(float(e) * self.input_stepsize) / self.input_samplerate for e in times]
        durations = [(float(e) * self.input_stepsize) / self.input_samplerate for e in durations]


        # outputs the raw frame level speech/non speech log likelihood difference
        sad_result = self.new_result(data_mode='value', time_mode='framewise')
        sad_result.id_metadata.id += '.' + 'sad_lhh_diff'
        sad_result.id_metadata.name += ' ' + 'Speech Activity Detection Log Likelihood Difference'
        sad_result.data_object.value = res
        self.add_result(sad_result)

        # outputs frame level speech/non speech log likelihood difference
        # altered with erosion and dilatation procedures
        sad_de_result = self.new_result(data_mode='value', time_mode='framewise')
        sad_de_result.id_metadata.id += '.' + 'sad_de_lhh_diff'
        sad_de_result.id_metadata.name += ' ' + 'Speech Activity Detection Log Likelihood Difference | dilat | erode'
        sad_de_result.data_object.value = deed_llh
        self.add_result(sad_de_result)

        # outputs speech/non speech segments
        sad_seg_result = self.new_result(data_mode='label', time_mode='segment')
        sad_seg_result.id_metadata.id += '.' + 'sad_segments'
        sad_seg_result.id_metadata.name += ' ' + 'Speech Activity Detection Segments'
        sad_seg_result.data_object.label = labels
        sad_seg_result.data_object.time = times
        sad_seg_result.data_object.duration = durations
        sad_seg_result.data_object.label_metadata.label = {0: 'Not Speech', 1: 'Speech'}

        self.add_result(sad_seg_result)
