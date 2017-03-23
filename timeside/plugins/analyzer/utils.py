# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Paul Brossier <piem@piem.org>
# Copyright (c) 2013-2017 Thomas Fillon <thomas@parisson.com>

# This file is part of TimeSide.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author: Paul Brossier <piem@piem.org>
# Author: Thomas Fillon <thomas@parisson.com>

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


def nextpow2(value):
    """Compute the nearest power of two greater or equal to the input value"""
    if value >= 1:
        return 2**np.ceil(np.log2(value)).astype(int)
    elif value > 0:
        return 1
    elif value == 0:
        return 0
    else:
        raise ValueError('Value must be positive')
