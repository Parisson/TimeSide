==========
 Tutorial
==========

== Quick Start ==

A most basic operation, transcoding, is easily performed with two processors:

 >>> import timeside
 >>> decoder = timeside.decoder.FileDecoder('myfile.wav')
 >>> encoder = timeside.encoder.OggEncoder("myfile.ogg")
 >>> pipe = decoder | encoder
 >>> pipe.run()

As one can see in the above example, creating a processing pipe is performed with
the binary OR operator.

Audio data visualisation can be performed using graphers, such as Waveform and
Spectrogram. All graphers return a [http://www.pythonware.com/library/pil/handbook/image.htm PIL image]:

 >>> import timeside
 >>> decoder = timeside.decoder.FileDecoder('myfile.wav')
 >>> spectrogram = timeside.grapher.Spectrogram(width=400, height=150)
 >>> (decoder | spectrogram).run()
 >>> spectrogram.render().save('graph.png')

It is possible to create longer pipes, as well as subpipes, here for both
analysis and encoding:

 >>> import timeside
 >>> decoder = timeside.decoder.FileDecoder('myfile.wav')
 >>> levels = timeside.analyzer.Level()
 >>> encoders = timeside.encoder.Mp3Encoder('myfile.mp3') | timeside.encoder.FlacEncoder('myfile.flac')
 >>> (decoder | levels | encoders).run()
 >>> print levels.results
