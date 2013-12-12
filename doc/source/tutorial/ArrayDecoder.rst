.. This file is part of TimeSide
   @author: Thomas Fillon

===============================================
 Running a pipe with previously decoded frames
===============================================

Example of use of the  :class:`ArrayDecoder <timeside.decoder.core.ArrayDecoder>` and  :class:`Waveform analyzer <timeside.analyzer.waveform.Waveform>` to run a pipe with previously frames from memory on a second pass

First, setup a  :class:`FileDecoder <timeside.decoder.core.FileDecoder>` on an audio file:

>>> import timeside
>>> import numpy as np
>>> 
>>> audio_file = 'http://github.com/yomguy/timeside-samples/raw/master/samples/sweep.mp3'
>>> 
>>> file_decoder = timeside.decoder.FileDecoder(audio_file)

Then, setup an arbitrary analyzer to check that both decoding process are equivalent and a :class:`Waveform analyzer <timeside.analyzer.waveform.Waveform>` which result will store the decoded frames:

>>> pitch_on_file = timeside.analyzer.AubioPitch()
>>> waveform = timeside.analyzer.Waveform()

And run the pipe:

>>> (file_decoder | pitch_on_file | waveform).run()

To run the second pass, we need to get back the decoded samples and the original samplerate and pass them to :class:`ArrayDecoder <timeside.decoder.core.ArrayDecoder>`:

>>> samples = waveform.results['waveform_analyzer'].data
>>> samplerate = waveform.results['waveform_analyzer'].frame_metadata.samplerate
>>> array_decoder = timeside.decoder.ArrayDecoder(samples=samples, samplerate=samplerate)

Then we can run a second pipe with the previously decoded frames and pass the frames to the same analyzer:

>>> pitch_on_array = timeside.analyzer.AubioPitch()
>>> (array_decoder | pitch_on_array).run()

To assert that the frames passed to the two analyzers are the same, we check that the results of these analyzers are equivalent:

>>> np.allclose(pitch_on_file.results['aubio_pitch.pitch'].data,
...             pitch_on_array.results['aubio_pitch.pitch'].data)
True

