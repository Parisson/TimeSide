# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2009 Guillaume Pellerin <yomguy@parisson.com>

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

# Authors:
#   Bram de Jong <bram.dejong at domain.com where domain in gmail>
#   Guillaume Pellerin <yomguy at parisson.com>

from timeside.core import *
import optparse, math, sys
import numpy
import scikits.audiolab as audiolab

class AudioProcessor(Component):

    def __init__(self):
        self.fft_size = 2048
        self.window_function = numpy.ones
        self.window = self.window_function(self.fft_size)
        self.spectrum_range = None
        self.lower = 100
        self.higher = 22050
        self.lower_log = math.log10(self.lower)
        self.higher_log = math.log10(self.higher)
        self.clip = lambda val, low, high: min(high, max(low, val))

    def pre_process(self, media_item):
        wav_file = media_item
        self.audio_file = audiolab.sndfile(wav_file, 'read')
        self.frames = self.audio_file.get_nframes()
        self.samplerate = self.audio_file.get_samplerate()
        self.channels = self.audio_file.get_channels()
        self.format = self.audio_file.get_file_format()
        self.encoding = self.audio_file.get_encoding()

    def get_samples(self):
        samples = self.audio_file.read_frames(self.frames)
        return samples

    def get_mono_samples(self):
        # convert to mono by selecting left channel only
        samples = self.get_samples()
        if self.channels > 1:
            return samples[:,0]
        else:
            return samples

    def read(self, start, size, resize_if_less=False):
        """ read size samples starting at start, if resize_if_less is True and less than size
        samples are read, resize the array to size and fill with zeros """

        # number of zeros to add to start and end of the buffer
        add_to_start = 0
        add_to_end = 0

        if start < 0:
            # the first FFT window starts centered around zero
            if size + start <= 0:
                if resize_if_less:
                    return numpy.zeros(size)
                else:
                    return numpy.array([])
            else:
                self.audio_file.seek(0)

                add_to_start = -start # remember: start is negative!
                to_read = size + start

                if to_read > self.frames:
                    add_to_end = to_read - self.frames
                    to_read = self.frames
        else:
            self.audio_file.seek(start)

            to_read = size
            if start + to_read >= self.frames:
                to_read = self.frames - start
                add_to_end = size - to_read

        try:
            samples = self.audio_file.read_frames(to_read)
        except IOError:
            # this can happen for wave files with broken headers...
            if resize_if_less:
                return numpy.zeros(size)
            else:
                return numpy.zeros(2)

        # convert to mono by selecting left channel only
        if self.channels > 1:
            samples = samples[:,0]

        if resize_if_less and (add_to_start > 0 or add_to_end > 0):
            if add_to_start > 0:
                samples = numpy.concatenate((numpy.zeros(add_to_start), samples), axis=1)

            if add_to_end > 0:
                samples = numpy.resize(samples, size)
                samples[size - add_to_end:] = 0

        return samples


    def spectral_centroid(self, seek_point, spec_range=120.0):
        """ starting at seek_point read fft_size samples, and calculate the spectral centroid """

        samples = self.read(seek_point - self.fft_size/2, self.fft_size, True)

        samples *= self.window
        fft = numpy.fft.fft(samples)
        spectrum = numpy.abs(fft[:fft.shape[0] / 2 + 1]) / float(self.fft_size) # normalized abs(FFT) between 0 and 1
        length = numpy.float64(spectrum.shape[0])

        # scale the db spectrum from [- spec_range db ... 0 db] > [0..1]
        db_spectrum = ((20*(numpy.log10(spectrum + 1e-30))).clip(-spec_range, 0.0) + spec_range)/spec_range

        energy = spectrum.sum()
        spectral_centroid = 0

        if energy > 1e-20:
            # calculate the spectral centroid

            if self.spectrum_range == None:
                self.spectrum_range = numpy.arange(length)

            spectral_centroid = (spectrum * self.spectrum_range).sum() / (energy * (length - 1)) * self.samplerate * 0.5

            # clip > log10 > scale between 0 and 1
            spectral_centroid = (math.log10(self.clip(spectral_centroid, self.lower, self.higher)) - self.lower_log) / (self.higher_log - self.lower_log)

        return (spectral_centroid, db_spectrum)


    def peaks(self, start_seek, end_seek):
        """ read all samples between start_seek and end_seek, then find the minimum and maximum peak
        in that range. Returns that pair in the order they were found. So if min was found first,
        it returns (min, max) else the other way around. """

        # larger blocksizes are faster but take more mem...
        # Aha, Watson, a clue, a tradeof!
        block_size = 4096

        max_index = -1
        max_value = -1
        min_index = -1
        min_value = 1

        if end_seek > self.frames:
            end_seek = self.frames

        if block_size > end_seek - start_seek:
            block_size = end_seek - start_seek

        if block_size <= 1:
            samples = self.read(start_seek, 1)
            return samples[0], samples[0]
        elif block_size == 2:
            samples = self.read(start_seek, True)
            return samples[0], samples[1]

        for i in range(start_seek, end_seek, block_size):
            samples = self.read(i, block_size)

            local_max_index = numpy.argmax(samples)
            local_max_value = samples[local_max_index]

            if local_max_value > max_value:
                max_value = local_max_value
                max_index = local_max_index

            local_min_index = numpy.argmin(samples)
            local_min_value = samples[local_min_index]

            if local_min_value < min_value:
                min_value = local_min_value
                min_index = local_min_index

        if min_index < max_index:
            return (min_value, max_value)
        else:
            return (max_value, min_value)



