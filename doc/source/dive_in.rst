Dive in
========

Define some processors::

 >>> import timeside
 >>> decoder  =  timeside.decoder.FileDecoder('sweep.wav')
 >>> grapher  =  timeside.grapher.Waveform()
 >>> analyzer =  timeside.analyzer.Level()
 >>> encoder  =  timeside.encoder.VorbisEncoder('sweep.ogg')

then, the *magic* pipeline::

 >>> (decoder | grapher | analyzer | encoder).run()

get the results::

 >>> grapher.render(output='waveform.png')
 >>> print 'Level:', analyzer.results

`More examples <http://code.google.com/p/timeside/wiki/PythonApi>`_

