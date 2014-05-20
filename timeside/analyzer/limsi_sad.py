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
        m = np.amax(llh, 1)
        dif = llh - np.atleast_2d(m).T
        return m + np.log(np.sum(np.exp(dif), 1))


class LimsiSad(Analyzer):

    """
    Limsi Speech Activity Detection Systems
    LimsiSad performs frame level speech activity detection based on GMM models
    For each frame, it computes the log likelihood difference between a speech model and a non speech model.
    The highest is the estimate, the largest is the probability that the frame corresponds to speech.
    The initialization of the analyzer requires to chose a model between 'etape' and 'maya'
    'etape' models were trained on data distributed in the framework of the ETAPE campaign (http://www.afcp-parole.org/etape.html)
    'maya' models were obtained on data collected by EREA – Centre Enseignement et Recherche en Ethnologie Amerindienne
    """
    implements(IAnalyzer)

    def __init__(self, sad_model='etape'):
        """
        Parameters:
        ----------
        sad_model : string bellowing to 'etape' 'maya'
        alllows the selection of a SAD model:
        'etape' is more suited to radionews material
        'maya' is more suited to speech obtained in noisy environments
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
        self.parents.append(parent_analyzer)

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

    def process(self, frames, eod=False):
        if self.input_samplerate != 16000:
            raise Exception(
                '%s requires 16000 input sample rate: %d provided' %
                (self.__class__.__name__, self.input_samplerate))
        return frames, eod

    def post_process(self):
        mfcc = self.process_pipe.results['yaafe.mfcc']['data_object']['value']
        mfccd1 = self.process_pipe.results[
            'yaafe.mfccd1']['data_object']['value']
        mfccd2 = self.process_pipe.results[
            'yaafe.mfccd2']['data_object']['value']
        zcr = self.process_pipe.results['yaafe.zcr']['data_object']['value']

        features = np.concatenate((mfcc, mfccd1, mfccd2, zcr), axis=1)

        res = 0.5 + 0.5 * \
            (self.gmms[0].llh(features) - self.gmms[1].llh(features))

        sad_result = self.new_result(data_mode='value', time_mode='framewise')
        sad_result.id_metadata.id += '.' + 'sad_lhh_diff'
        sad_result.id_metadata.name += ' ' + \
            'Speech Activity Detection Log Likelihood Difference'
        sad_result.data_object.value = res
        self.process_pipe.results.add(sad_result)
