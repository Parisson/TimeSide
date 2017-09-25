
Dive in
========

Let's produce a really simple audio analysis of an audio file.
First, list all available plugins:

.. doctest::

   >>> import timeside.core
   >>> timeside.core.list_processors()  # doctest: +ELLIPSIS
   IProcessor
   ==========
   ...

Define some processors:

.. doctest::

   >>> from timeside.core import get_processor
   >>> from timeside.core.tools.test_samples import samples
   >>> wavfile = samples['sweep.wav']
   >>> decoder  =  get_processor('file_decoder')(wavfile)
   >>> grapher  =  get_processor('waveform_simple')()
   >>> analyzer =  get_processor('level')()
   >>> encoder  =  get_processor('vorbis_encoder')('sweep.ogg')


Then run the *magic* pipeline:

.. doctest::

   >>> (decoder | grapher | analyzer | encoder).run()

Render the grapher results:

.. doctest::

   >>> grapher.render(output='waveform.png')

.. testcleanup::

   import os
   os.remove('waveform.png')
   os.remove('sweep.ogg')


Show the analyzer results:

.. doctest::

   >>> print 'Level:', analyzer.results  # doctest: +ELLIPSIS
   Level: {'level.max': AnalyzerResult(...), 'level.rms': AnalyzerResult(...)}


So, in only one pass, the audio file has been decoded, analyzed, graphed and transcoded.

For more extensive examples, please see the `full documentation <http://files.parisson.com/timeside/doc/>`_.
