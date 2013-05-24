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

import numpy

def downsample_blocking(frames, hop_s, dtype='float32'):
    # downmixing to one channel
    if len(frames.shape) != 1:
        downsampled = frames.sum(axis = -1) / frames.shape[-1]
    else:
        downsampled = frames
    # zero padding to have a multiple of hop_s
    if downsampled.shape[0] % hop_s != 0:
        pad_length = hop_s + downsampled.shape[0] / hop_s * hop_s - downsampled.shape[0]
        downsampled = numpy.hstack([downsampled, numpy.zeros(pad_length, dtype = dtype)])
    # blocking
    return downsampled.reshape(downsampled.shape[0] / hop_s, hop_s)


