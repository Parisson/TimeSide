Dive in
========

To list all available plugins::

 import timeside
 timeside.core.list_processors()

Define some processors::

 from timeside.core import get_processor
 decoder  =  get_processor('gst_dec')('sweep.wav')
 grapher  =  get_processor('waveform_simple')
 analyzer =  get_processor('level')
 encoder  =  get_processor('gst_vorbis_enc')('sweep.ogg')

Then run the *magic* pipeline::

 (decoder | grapher | analyzer | encoder).run()

Render the grapher results::

 grapher.render(output='waveform.png')

Show the analyzer results::

 print 'Level:', analyzer.results

The encoded OGG file should also be there...

Note you can also instanciate each processor with its own class::

 decoder  =  timeside.decoder.file.FileDecoder('sweep.wav')
 grapher  =  timeside.grapher.waveform_simple.Waveform()
 analyzer =  timeside.analyzer.level.Level()
 encoder  =  timeside.encoder.ogg.VorbisEncoder('sweep.ogg')

For more extensive examples, please see the `full documentation <http://files.parisson.com/timeside/doc/>`_.

