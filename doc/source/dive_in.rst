Dive in
========

Define some processors::

 >>> import timeside
 >>> decoder  =  timeside.decoder.file.FileDecoder('sweep.wav')
 >>> grapher  =  timeside.grapher.waveform_simple.Waveform()
 >>> analyzer =  timeside.analyzer.level.Level()
 >>> encoder  =  timeside.encoder.ogg.VorbisEncoder('sweep.ogg')

then, the *magic* pipeline::

 >>> (decoder | grapher | analyzer | encoder).run()

get the results::

 >>> grapher.render(output='waveform.png')
 >>> print 'Level:', analyzer.results

For more extensive examples, please see the `http://files.parisson.com/timeside/doc/ <full documentation>`_.

