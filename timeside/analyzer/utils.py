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

import numpy as np

MACHINE_EPSILON = np.finfo(np.float32).eps


def downsample_blocking(frames, hop_s, dtype='float32'):
    # downmixing to one channel
    if len(frames.shape) != 1:
        downsampled = frames.sum(axis=-1) / frames.shape[-1]
    else:
        downsampled = frames
    # zero padding to have a multiple of hop_s
    if downsampled.shape[0] % hop_s != 0:
        pad_length = hop_s + \
            downsampled.shape[0] / hop_s * hop_s - downsampled.shape[0]
        downsampled = np.hstack(
            [downsampled, np.zeros(pad_length, dtype=dtype)])
    # blocking
    return downsampled.reshape(downsampled.shape[0] / hop_s, hop_s)


def computeModulation(serie, wLen, withLog=True):
        '''
        Compute the modulation of a parameter centered.
        Extremums are set to zero.

        Args :
            - serie       : list or numpy array containing the serie.
            - wLen        : Length of the analyzis window in samples.
            - withLog     : Whether compute the var() or log(var()) .

        Returns :
            - modul       : Modulation of the serie.

        '''
        sLen = len(serie)
        modul = np.zeros((sLen,))
        w = int(wLen / 2)

        for i in range(w, sLen - w):

            d = serie[i - w:i + w]
            if withLog:
                if not (d > 0).all():
                    d[d <= 0] = MACHINE_EPSILON  # prevent log(0)=inf
                d = np.log(d)

            modul[i] = np.var(d)

        modul[:w] = modul[w]
        modul[-w:] = modul[-w - 1]

        return modul


def segmentFromValues(values, offset=0):
    '''

    '''

    seg = [offset, -1, values[0]]
    segList = []
    for i, v in enumerate(values):

        if not (v == seg[2]):
            seg[1] = i + offset - 1
            segList.append(tuple(seg))
            seg = [i + offset, -1, v]

    seg[1] = i + offset
    segList.append(tuple(seg))

    return segList


# Attention
# ---------
#
# Double emploi avec le calcul mfcc d'aubio. Voir pour la fusion...
#                         Maxime

def melFilterBank(nbFilters, fftLen, sr):
    '''
    Grenerate a Mel Filter-Bank

    Args :
        - nbFilters  : Number of filters.
        - fftLen     : Length of the frequency range.
        - sr         : Sampling rate of the signal to filter.
    Returns :
        - filterbank : fftLen x nbFilters matrix containing one filter by column.
                        The filter bank can be applied by matrix multiplication
                        (Use numpy *dot* function).
    '''

    fh = float(sr) / 2.0
    mh = 2595 * np.log10(1 + fh / 700)

    step = mh / nbFilters

    mcenter = np.arange(step, mh, step)

    fcenter = 700 * (10 ** (mcenter / 2595) - 1)

    filterbank = np.zeros((fftLen, nbFilters))

    for i, _ in enumerate(fcenter):

        if i == 0:
            fmin = 0.0
        else:
            fmin = fcenter[i - 1]

        if i == len(fcenter) - 1:
            fmax = fh
        else:
            fmax = fcenter[i + 1]

        imin = np.ceil(fmin / fh * fftLen)
        imax = np.ceil(fmax / fh * fftLen)

        filterbank[imin:imax, i] = triangle(imax - imin)

    return filterbank


def triangle(length):
    '''
    Generate a triangle filter.

    Args :
         - length  : length of the filter.
    returns :
        - triangle : triangle filter.

    '''
    triangle = np.zeros((1, length))[0]
    climax = np.ceil(length / 2)

    triangle[0:climax] = np.linspace(0, 1, climax)
    triangle[climax:length] = np.linspace(1, 0, length - climax)
    return triangle


def entropy(serie, nbins=10, base=np.exp(1), approach='unbiased'):
        '''
        Compute entropy of a serie using the histogram method.

        Args :
            - serie     : Serie on witch compute the entropy
            - nbins     : Number of bins of the histogram
            - base      : Base used for normalisation
            - approach  : String in the following set : {unbiased,mmse}
                          for un-biasing value.

        Returns :
            - estimate  : Entropy value
            - nbias     : N-bias of the estimate
            - sigma     : Estimated standard error

        Raises :
            A warning in case of unknown 'approach' value.
            No un-biasing is then performed

        '''

        estimate = 0
        sigma = 0
        bins, edges = np.histogram(serie, nbins)
        ncell = len(bins)
        norm = (np.max(edges) - np.min(edges)) / len(bins)

        for b in bins:
            if b == 0:
                logf = 0
            else:
                logf = np.log(b)
            estimate = estimate - b * logf
            sigma = sigma + b * logf ** 2

        count = np.sum(bins)
        estimate = estimate / count
        sigma = np.sqrt((sigma / count - estimate ** 2) / float(count - 1))
        estimate = estimate + np.log(count) + np.log(norm)
        nbias = -(ncell - 1) / (2 * count)

        if approach == 'unbiased':
            estimate = estimate - nbias
            nbias = 0

        elif approach == 'mmse':
            estimate = estimate - nbias
            nbias = 0
            lambda_value = estimate ^ 2 / (estimate ^ 2 + sigma ^ 2)
            nbias = (1 - lambda_value) * estimate
            estimate = lambda_value * estimate
            sigma = lambda_value * sigma
        else:
            return 0

        estimate = estimate / np.log(base)
        nbias = nbias / np.log(base)
        sigma = sigma / np.log(base)
        return estimate
