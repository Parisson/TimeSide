.. This file is part of TimeSide
   @author: Thomas Fillon

===============================================
 Running a pipe with previously decoded frames
===============================================

Example of use of the `stack` option in :func:`timeside.core.ProcessPipe.run` to run a pipe with previously decoded frames stacked in memory on a second pass.

>>> import timeside
>>> import numpy as np
>>> audio_file = 'http://github.com/yomguy/timeside-samples/raw/master/samples/sweep.mp3'
>>> decoder = timeside.decoder.FileDecoder(audio_file)

Setup an arbitrary analyzer to check that decoding process from file and from stack are equivalent:

>>> pitch_on_file = timeside.analyzer.AubioPitch()
>>> pipe = (decoder | pitch_on_file)
>>> print pipe.processors #doctest: +ELLIPSIS
[<timeside.decoder.core.FileDecoder object at 0x...>, <timeside.analyzer.aubio_pitch.AubioPitch object at 0x...>]

If the pipe is run with the default argument `stack=False`, the other processes of the pipe are released from the pipe after the run and only the  :class:`fileDecoder <timeside.decoder.core.FileDecoder>` is kept in the pipe:

>>> pipe.run()
>>> print pipe.processors #doctest: +ELLIPSIS
[<timeside.decoder.core.FileDecoder object at 0x...>]


If the pipe is run with the argument `stack=True`, the processed frames are stored in the pipe attribute `frames_stack`.
The other processes of the pipe are also released from the pipe after the run but the :class:`fileDecoder <timeside.decoder.core.FileDecoder>` is replaced by an :class:`ArrayDecoder <timeside.decoder.core.ArrayDecoder>`:

>>> pipe = (decoder | pitch_on_file)
>>> pipe.run(stack=True)
>>> print pipe.processors #doctest: +ELLIPSIS
[<timeside.decoder.core.ArrayDecoder object at 0x...>]

The stack

>>> pipe.frames_stack #doctest: +ELLIPSIS
array([[...]], dtype=float32)


Then we can run a second pipe with the previously decoded frames and pass the frames to the same analyzer.

Define a second analyzer equivalent to the previous one:

>>> pitch_on_stack = timeside.analyzer.AubioPitch()

Add it to the pipe:

>>> pipe |= pitch_on_stack
>>> print pipe.processors #doctest: +ELLIPSIS
[<timeside.decoder.core.ArrayDecoder object at 0x...>, <timeside.analyzer.aubio_pitch.AubioPitch object at 0x...>]


Run the pipe:

>>> pipe.run()

Assert that the frames passed to the two analyzers are the same, we check that the results of these analyzers are equivalent:

>>> np.allclose(pitch_on_file.results['aubio_pitch.pitch'].data,
...                    pitch_on_stack.results['aubio_pitch.pitch'].data)
True

