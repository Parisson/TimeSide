.. This file is part of TimeSide
   @author: Guillaume Pellerin

Streaming out encoded audio
============================

Instead of calling a pipe.run(), the chunks of an encoding processor can also be retrieved and streamed outside the pipe during the process.

>>> import timeside
>>> from timeside.core import get_processor
>>> from timeside.tools.test_samples import samples
>>> import numpy as np
>>> audio_file = samples['sweep.wav']
>>> decoder = get_processor('file_decoder')
>>> output = '/tmp/test.mp3'
>>> encoder = get_processor('mp3_encoder')(output, streaming=True)
>>> pipe = decoder | encoder

Create a process callback method so that you can retrieve end send the chunks:

>>> def streaming_callback():
>>>     for chunk in pipe.stream():
>>>         # Do something with chunk
>>>         yield chunk

Now you can use the callback to stream the audio data outside TimeSide!
