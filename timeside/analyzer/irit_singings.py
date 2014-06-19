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
from timeside.analyzer.utils import smoothing
from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from timeside.analyzer.irit_monopoly import IRITMonopoly
from timeside.api import IAnalyzer
from aubio import pitch
from numpy.fft import rfft
from numpy import argmin, argmax, sqrt, log2, linspace, abs, median
from collections import Counter
from timeside.analyzer.preprocessors import frames_adapter


class IRITSingings(Analyzer):
    """

    """
    implements(IAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):

        super(IRITSingings, self).setup(channels,
                                        samplerate,
                                        blocksize,
                                        totalframes)

        self.parents.append(IRITMonopoly())

        self.aubio_pitch = pitch(
            "default", self.input_blocksize, self.input_stepsize,
            samplerate)
        self.aubio_pitch.set_unit("freq")
        self.block_read = 0
        self.pitches = []
        self.spectro = []
        self.pitch_confidences = []

        self.wLen = 0.1
        self.wStep = 0.05

        self.thPoly = 0.15
        self.thMono = 0.1

        self.input_blocksize = int(self.wLen * samplerate)
        self.input_stepsize = int(self.wStep * samplerate)

    @staticmethod
    @interfacedoc
    def id():
        return "irit_singings"

    @staticmethod
    @interfacedoc
    def name():
        return "IRIT singings detection"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def __str__(self):
        return "Labeled segments with/out singings"

    @frames_adapter
    def process(self, frames, eod=False):
        frame = frames[0]
        # in seconds
        pf = self.aubio_pitch(frame)
        self.pitches += list(pf)
        self.pitch_confidences += [self.aubio_pitch.get_confidence()]
        self.block_read += 1
        spectro_frame = list(abs(rfft(frame)))
        self.spectro += [spectro_frame]
        return frames, eod

    def post_process(self):
        """

        """
        preproc = self.process_pipe.results['irit_monopoly.segments'].data_object
        labels = self.process_pipe.results['irit_monopoly.segments'].label_metadata['label']
        segments_monopoly = [(start, duration, labels[label])for start, duration, label in zip(preproc.time,
                                                                                               preproc.duration,
                                                                                               preproc.label)]
        segments_chant = []
        for start, duration, label in segments_monopoly:
            cumulChant = 0
            ## Atention aux changements de labels ...
            if label == 'Mono':
                f0_frame_rate = 1.0/self.wStep
                segs = split_notes(self.pitches, f0_frame_rate)
                for seg in segs:
                    if has_vibrato(seg[2], f0_frame_rate):
                        cumulChant += seg[1]-seg[0]
                segments_chant += [(start, duration, cumulChant/duration >= self.thMono)]

            elif label == 'Poly':
                pass
            else:
                pass

        return



class SinusoidalSegment(object):

    """
    Segment sinusoidal assurant le suivi des fréquences prédominantes du spectre


    .. py:attribute:: last_peak

    Dernier peak ajouté au segment

    .. py:attribute:: start

    Temps de départ du segment

    .. py:attribute:: stop

    Temps d'arret du segment

    .. py:attribute:: activated

    Booleen pour une recherche rapide des segments encore prolongeables

    .. py:attribute:: times

    Liste des temps sur lesquels le segment est présent

    .. py:attribute:: frequencies

    Listes des fréquences par lesquels passes le segment

    .. py:attribute:: amplitudes

    Liste des amplitudes

    """
    def __init__(self, peak, t):
        self.last_peak = peak
        self.start = t
        self.activated = True
        self.times = [t]
        self.frequencies = [peak[0]]
        self.amplitudes = [peak[1]]
        self.stop = t

    def append(self, peak_list, t, dth=1):
        """
        Ajoute au segment le meilleur candidat de la liste peak_list correspondant aux pic de l'instant t.

       :param list peak_list: list des pics candidats
       :param float t: temps correspondant aux candidats
       :param float: seuil pour la distance de tanigushi

       """

        dists = [tanigushi_distance(self.last_peak, peak) for peak in peak_list]
        if len(dists) > 0 and min(dists) < dth:
            im = argmin(dists)
            peak = peak_list[im]
            self.last_peak = peak
            self.times += [t]
            self.frequencies += [peak[0]]
            self.amplitudes += [peak[1]]
            self.stop = t
            return im
        else:
            self.activated = False
            return -1

    def get_portion(self, start, stop):
        """

        Récupération d'une portion de segment

        :param float start: temps de début
        :param float stop: temps de fin

        :returns: la portion de segment entre start et stop.


        """

        return zip(* [(f, t) for f, t in zip(self.times, self.frequencies) if stop >= t >= start])


def tanigushi_distance(peak_A, peak_B, Cf=100, Cp=3):
    """
    Calcul de la distance de tanigushi entre deux pics

    :param couple peak_A: pic A sous la forme (frequence, amplitude)
    :param couple peak_B: pic B sous la forme (frequence, amplitude)
    :param float Cf: diviseur des fréquences dans la formule de Tanigushi.
    :param float Cp: diviseur de l'amplitude dans la formule de Tanigushi.
    :returns: la distance de Tanigushi entre les deux pics

    """

    return sqrt(((freq_to_cent(peak_A[0])-freq_to_cent(peak_B[0]))/Cf)**2 +((peak_A[1]-peak_B[1])/Cp)**2)


def freq_to_cent(frequency):
    """
    Transforme une valeur fréquentielle en Hertz en cent

    :param float frequency: Valeur en Hertz
    :returns: La valeur equivalente en cent

    """
    return 1200*log2(frequency/(440*2**(3/11-5)))


def get_peaks_cent(frame, frequency_scale, distance_between_peaks=100, max_number_of_peaks=None,
                   threshold_amplitude=0.02):
    """

    Retourne la liste des pics d'une trame

    :param list frame: Spectre à analyser
    :param list frequency_scale: Liste des fréquences en Hertz correspondant aux bins de frame.
    :param int distance_between_peaks: distance minimale possible entre pics sélectionnés.
    :param max_number_of_peaks: Nombre maximum de pics à sélectionner. Pas de limite si *None*
    :type max_number_of_peaks: int ou None
    :param list threshold_amplitude: amplitude minimale (en ratio de l'amplitude maximale) pour sélectionner un pic.


    """

    threshold_amplitude = max(frame)*threshold_amplitude

    peaks = [(frequency_scale[i+1], amplitude) for i, amplitude in enumerate(frame[1:-1])
             if amplitude > threshold_amplitude and frame[i] < amplitude > frame[i+2]]
    peaks = sorted(peaks, key=lambda tup: tup[1], reverse=True)

    selected = [peaks.pop(0)]

    if max_number_of_peaks is None:
        max_number_of_peaks = len(peaks)

    while len(peaks) > 0 and len(selected) <= max_number_of_peaks:
        candidate = peaks.pop(0)
        cent = freq_to_cent(candidate[0])
        dists = [p for p in selected if abs(freq_to_cent(p[0])-cent) < distance_between_peaks]
        if len(dists) == 0:
            selected += [candidate]

    return selected


def compute_simple_sinusoidal_segments(spectrogram):
    """
    Fonction de calcul des segments sinusoidaux sur un spectrogramme
    """

    segments = []
    active_segments = []
    for i, frame in enumerate(spectrogram.content):
        t = spectrogram.time_scale[i]
        frame = smoothing(frame)
        peaks = get_peaks_cent(frame,spectrogram.frequency_scale)

        for s in active_segments :
            im = s.append(peaks, t)
            if not im == -1:
                peaks.pop(im)

        active_segments = [s for s in active_segments if s.activated]

        for p in peaks:
            ns = SinusoidalSegment(p, t)
            segments += [ns]
            active_segments+=[ns]

    return segments


def has_vibrato(serie, sampling_rate, minimum_frequency=4, maximum_frequency=8, Nfft=100):
    """
    Calcul de vibrato sur une serie par la méthode de la transformée de Fourier de la dérivée.
    """
    vibrato = False
    frequency_scale = linspace(0, sampling_rate/2, Nfft/2)

    index_min_vibrato = argmin(abs(frequency_scale-minimum_frequency))
    index_max_vibrato = argmin(abs(frequency_scale-maximum_frequency))

    derivative = [v1-v2 for v1, v2 in zip(serie[:-2], serie[1:])]
    fft_derivative = abs(rfft(derivative, Nfft))[:Nfft/2]
    i_max = argmax(fft_derivative)
    if index_max_vibrato >= i_max >= index_min_vibrato:
        vibrato = True

    return vibrato


def extended_vibrato(spectrogram, maximum_frequency=1500, minimum_segment_length=4, number_of_extrema_for_rupture=3):
    """

    Detection de vibrato en contexte polyphonique

    """

    spectrogram = spectrogram.get_spectal_band(maximum_frequency=maximum_frequency)

    segments = [s for s in compute_simple_sinusoidal_segments(spectrogram) if len(s.time) > minimum_segment_length]

    extremums = [s.start for s in segments]+[s.stop for s in segments]
    counter = Counter(extremums)

    ruptures = sorted([0]
                      + [time for time in counter if counter[time] >= number_of_extrema_for_rupture]
                      + [spectrogram.time_scale[-1]])
    spectrogram_sampling_rate = spectrogram.get_sampling_rate()
    scores = []
    for i, rupture in enumerate(ruptures[:-1]):
        sum_present = 0.0
        sum_vibrato = 0.0
        for s in segments:
            times, frequencies = s.get_portion(rupture, ruptures[i+1])
            if len(times) > 0:
                sum_present += 1.0
                if has_vibrato(frequencies, spectrogram_sampling_rate):
                    sum_vibrato += 1.0
        scores += [(rupture, ruptures[i+1], sum_vibrato/sum_present)]

    return scores


def split_notes(f0, f0_sample_rate, minimum_segment_length=0.0):
    """
    Découpage en pseudo-notes en fonction de la fréquence fondamentale.
    Retourne la liste des segments en secondes
    """

    f0 = smoothing(f0, number_of_points=5, smoothing_function=median)
    half_tone_ratio = 2**(1.0/12.0)
    minimum_segment_length = minimum_segment_length/f0_sample_rate
    ratios = [max([y1, y2])/min([y1, y2]) for y1, y2 in zip(f0[:-2], f0[1:])]
    boundaries = [0]+[i+1 for i, ratio in enumerate(ratios) if ratio > half_tone_ratio]

    return [(start*f0_sample_rate, stop*f0_sample_rate, f0[start:stop])
            for start, stop in zip(boundaries[:-2], boundaries[1:]) if stop-start > minimum_segment_length]

