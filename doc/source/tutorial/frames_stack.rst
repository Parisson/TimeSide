.. This file is part of TimeSide
   @author: Thomas Fillon

===============================================
 Running a pipe with previously decoded frames
===============================================

Example of use of the `stack` argument in :class:`timeside.decoder.file.FileDecoder` to run a pipe with previously decoded frames stacked in memory on a second pass.

First, let's import everything and define the audio file source :

>>> import timeside
>>> from timeside.core import get_processor
>>> import numpy as np
>>> audio_file = 'http://github.com/yomguy/timeside-samples/raw/master/samples/sweep.mp3'

Then let's setup a :class:`FileDecoder <timeside.decoder.file.FileDecoder>` with argument `stack=True` (default argument is `stack=False`) :

>>> decoder = timeside.decoder.file.FileDecoder(audio_file, stack=True)

Setup an arbitrary analyzer to check that decoding process from file and from stack are equivalent:

>>> pitch_on_file = get_processor('aubio_pitch')()
>>> pipe = (decoder | pitch_on_file)
>>> print pipe.processors #doctest: +ELLIPSIS
[<timeside.decoder.file.FileDecoder object at 0x...>, <timeside.analyzer.aubio.aubio_pitch.AubioPitch object at 0x...>]

After the pipe has been run, the other processes of the pipe are removed from the pipe and only the :class:`FileDecoder <timeside.decoder.file.FileDecoder>` is kept :

>>> pipe.run()
>>> print pipe.processors #doctest: +ELLIPSIS
[<timeside.decoder.file.FileDecoder object at 0x...>]

The processed frames are stored in the pipe attribute `frames_stack` as a list of frames :

>>> print type(pipe.frames_stack)
<type 'list'>

First frame :

>>> print pipe.frames_stack[0] #doctest: +ELLIPSIS
(array([[...]], dtype=float32), False)

Last frame :

>>> print pipe.frames_stack[-1] #doctest: +ELLIPSIS
(array([[...]], dtype=float32), True)

If the pipe is used for a second run, the processed frames stored in the stack are passed to the other processors without decoding the audio source again.
Let's define a second analyzer equivalent to the previous one:

>>> pitch_on_stack = get_processor('aubio_pitch')()

Add it to the pipe:

>>> pipe |= pitch_on_stack
>>> print pipe.processors #doctest: +ELLIPSIS
[<timeside.decoder.file.FileDecoder object at 0x...>, <timeside.analyzer.aubio.aubio_pitch.AubioPitch object at 0x...>]

And run the pipe:

>>> pipe.run()

Assert that the frames passed to the two analyzers are the same, we check that the results of these analyzers are equivalent:

>>> np.allclose(pitch_on_file.results['aubio_pitch.pitch'].data,
...                    pitch_on_stack.results['aubio_pitch.pitch'].data)
True

