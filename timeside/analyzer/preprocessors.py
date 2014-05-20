# -*- coding: utf-8 -*-
#
# Copyright (c) 2009-2013 Parisson SARL
#
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
#
# Author : Thomas fillon <thomas@parisson.com>
'''
    Collections of preprocessors to use as decorators for the analyzers process

    Preprocessors process the (frame, eod) arguments in order to handle various
    preprocessing such as :
        - Downmixing to mono
        - Adapt the frames to match the input_blocksize and input_stepsize
            of the analyzer
'''


def downmix_to_mono(process_func):
    '''
    Pre-processing decorator that downmixes frames from multi-channel to mono

    Downmix is achieved by averaging all channels

    >>> from timeside.analyzer.preprocessors import downmix_to_mono
    >>> @downmix_to_mono
    ... def process(analyzer,frames,eod):
    ...     print 'Frames, eod inside process :'
    ...     print frames, eod
    ...     return frames, eod
    ...
    >>> import numpy as np
    >>> frames = np.asarray([[1,2],[3,4],[5,6],[7,8],[9,10]])
    >>> eod = False
    >>> frames_, eod_ = process(object(),frames,eod)
    Frames, eod inside process :
    [ 1.5  3.5  5.5  7.5  9.5] False

    Outside Process frames and eod are preserved :

    >>> frames_
    array([[ 1,  2],
           [ 3,  4],
           [ 5,  6],
           [ 7,  8],
           [ 9, 10]])
    >>> eod_
    False
    '''

    import functools

    @functools.wraps(process_func)
    def wrapper(analyzer, frames, eod):
        # Pre-processing
        if frames.ndim > 1:
            downmix_frames = frames.mean(axis=-1)
        else:
            downmix_frames = frames
        # Processing
        process_func(analyzer, downmix_frames, eod)

        return frames, eod
    return wrapper


def frames_adapter(process_func):
    '''
    Pre-processing decorator that adapt frames to match input_blocksize and
    input_stepsize of the decorated analyzer

    >>> from timeside.analyzer.preprocessors import frames_adapter
    >>> @frames_adapter
    ... def process(analyzer,frames,eod):
    ...     analyzer.frames.append(frames)
    ...     return frames, eod
    ...
    >>> class Fake_Analyzer(object):
    ...     def __init__(self):
    ...         self.input_blocksize = 4
    ...         self.input_stepsize = 3
    ...         self.frames = [] # Container for the frame as viewed by process
    >>> import numpy as np
    >>> analyzer = Fake_Analyzer()
    >>> frames = np.asarray(range(0,12))
    >>> eod = False
    >>> frames_, eod_ = process(analyzer,frames,eod)

    Inside the process the frames have been adapted to match input_blocksize
    and input_stepsize

    >>> analyzer.frames
    [array([0, 1, 2, 3]), array([3, 4, 5, 6]), array([6, 7, 8, 9])]

    Outside the process, the original frames and eod are preserved:

    >>> frames_
    array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11])
    >>> eod_
    False

    Releasing the process with eod=True will zeropad the last frame if necessary

    >>> frames = np.asarray(range(12,14))
    >>> eod = True
    >>> frames_, eod_ = process(analyzer,frames,eod)
    >>> analyzer.frames
    [array([0, 1, 2, 3]), array([3, 4, 5, 6]), array([6, 7, 8, 9]), array([ 9, 10, 11, 12]), array([12, 13,  0,  0])]
    '''

    import functools
    import numpy as np

    class framesBuffer(object):

        def __init__(self, blocksize, stepsize):
            self.blocksize = blocksize
            self.stepsize = stepsize
            self.buffer = None

        def frames(self, frames, eod):
            if self.buffer is not None:
                stack = np.concatenate([self.buffer, frames])
            else:
                stack = frames.copy()

            stack_length = len(stack)

            nb_frames = (
                stack_length - self.blocksize + self.stepsize) // self.stepsize
            nb_frames = max(nb_frames, 0)
            frames_length = nb_frames * self.stepsize + \
                self.blocksize - self.stepsize
            last_block_size = stack_length - frames_length

            if eod:
                # Final zeropadding
                pad_shape = tuple(
                    self.blocksize - last_block_size if i == 0 else x
                    for i, x in enumerate(frames.shape))
                stack = np.concatenate([stack, np.zeros(pad_shape,
                                                        dtype=frames.dtype)])
                nb_frames += 1

            self.buffer = stack[nb_frames * self.stepsize:]

            eod_list = np.repeat(False, nb_frames)
            if eod and len(eod_list):
                eod_list[-1] = eod

            for index, eod in zip(xrange(0, nb_frames * self.stepsize, self.stepsize), eod_list):
                yield (stack[index:index + self.blocksize], eod)

    @functools.wraps(process_func)
    def wrapper(analyzer, frames, eod):
        # Pre-processing
        if not hasattr(analyzer, 'frames_buffer'):
            analyzer.frames_buffer = framesBuffer(analyzer.input_blocksize,
                                                  analyzer.input_stepsize)

        # Processing
        for adapted_frames, adapted_eod in analyzer.frames_buffer.frames(frames, eod):
            process_func(analyzer, adapted_frames, adapted_eod)

        return frames, eod
    return wrapper


if __name__ == "__main__":
    import doctest
    doctest.testmod()
