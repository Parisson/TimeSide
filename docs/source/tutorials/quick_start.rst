=============
 Quick start
=============

A most basic operation, transcoding, is easily performed with two processors:

.. testsetup:: *

    import os

.. testcleanup:: test_1

   os.remove('sweep.ogg')

.. testcleanup:: test_2

   os.remove('graph.png')

.. testcleanup:: test_3

   os.remove('sweep.mp3')
   os.remove('sweep.flac')

.. doctest:: test_1

   >>> import timeside
   >>> from timeside.core.tools.test_samples import samples
   >>> from timeside.core import get_processor
   >>> decoder = get_processor('file_decoder')(samples["sweep.wav"])
   >>> encoder = get_processor('vorbis_encoder')("sweep.ogg")
   >>> pipe = decoder | encoder
   >>> pipe.run()

As one can see in the above example, creating a processing pipe is performed with
the binary OR operator.

Audio data visualisation can be performed using graphers, such as Waveform and
Spectrogram. All graphers return an image:

.. doctest:: test_2

   >>> import timeside
   >>> from timeside.core.tools.test_samples import samples
   >>> from timeside.core import get_processor
   >>> decoder =  get_processor('file_decoder')(samples["sweep.wav"])
   >>> spectrogram = get_processor('spectrogram_lin')(width=400, height=150)
   >>> (decoder | spectrogram).run()
   >>> spectrogram.render('graph.png')

It is possible to create longer pipes, as well as subpipes, here for both
analysis and encoding:

.. doctest:: test_3

   >>> import timeside
   >>> from timeside.core.tools.test_samples import samples
   >>> from timeside.core import get_processor
   >>> decoder = get_processor('file_decoder')(samples["sweep.wav"])
   >>> levels = get_processor('level')()
   >>> encoders = get_processor('mp3_encoder')('sweep.mp3') | get_processor('flac_encoder')('sweep.flac')
   >>> (decoder | levels | encoders).run()
   >>> print levels.results
