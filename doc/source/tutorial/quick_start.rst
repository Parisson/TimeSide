=============
 Quick start
=============

A most basic operation, transcoding, is easily performed with two processors:


.. testsetup:: test_1,test_2,test_3

   import timeside
   import os
   ModulePath =  os.path.dirname(os.path.realpath(timeside.analyzer.core.__file__))
   wavFile = os.path.join(ModulePath , '../../tests/samples/sweep.wav')
   decoder = timeside.decoder.FileDecoder(wavFile)

.. testcleanup:: test_1

   os.remove('sweep.ogg')

.. testcleanup:: test_2

   os.remove('graph.png')

.. testcleanup:: test_3

   os.remove('sweep.mp3')
   os.remove('sweep.flac')

.. doctest:: test_1

 >>> import timeside # doctest: +SKIP
 >>> decoder = timeside.decoder.FileDecoder('sweep.wav')# doctest: +SKIP
 >>> encoder = timeside.encoder.VorbisEncoder('sweep.ogg')
 >>> pipe = decoder | encoder
 >>> pipe.run()

As one can see in the above example, creating a processing pipe is performed with
the binary OR operator.

Audio data visualisation can be performed using graphers, such as Waveform and
Spectrogram. All graphers return an image:

.. doctest:: test_2

   >>> import timeside
   >>> decoder = timeside.decoder.FileDecoder('sweep.wav') # doctest: +SKIP
   >>> spectrogram = timeside.grapher.SpectrogramLinear(width=400, height=150)
   >>> (decoder | spectrogram).run()
   >>> spectrogram.render('graph.png')

It is possible to create longer pipes, as well as subpipes, here for both
analysis and encoding:

.. doctest:: test_3

   >>> import timeside
   >>> decoder = timeside.decoder.FileDecoder('sweep.wav') # doctest: +SKIP
   >>> levels = timeside.analyzer.Level()
   >>> encoders = timeside.encoder.Mp3Encoder('sweep.mp3') | timeside.encoder.FlacEncoder('sweep.flac')
   >>> (decoder | levels | encoders).run()
   >>> print levels.results
   {'level.max': GlobalValueResult(id_metadata=IdMetadata(id='level.max', name='Level Analyzer Max', unit='dBFS', description='', date='...', version='...', author='TimeSide', uuid='...'), data_object=DataObject(value=array([-6.021])), audio_metadata=AudioMetadata(uri='file://...sweep.wav', start=0.0, duration=8.0, is_segment=False, channels=None, channelsManagement=''), parameters={}), 'level.rms': GlobalValueResult(id_metadata=IdMetadata(id='level.rms', name='Level Analyzer RMS', unit='dBFS', description='', date='...', version='...', author='TimeSide', uuid='...'), data_object=DataObject(value=array([-9.856])), audio_metadata=AudioMetadata(uri='file://...sweep.wav', start=0.0, duration=8.0, is_segment=False, channels=None, channelsManagement=''), parameters={})}
