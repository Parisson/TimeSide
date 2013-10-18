 Quick start
============

A most basic operation, transcoding, is easily performed with two processors:

 >>> import timeside
 >>> decoder = timeside.decoder.FileDecoder('sweep.wav')
 >>> encoder = timeside.encoder.VorbisEncoder("sweep.ogg")
 >>> pipe = decoder | encoder
 >>> pipe.run()

As one can see in the above example, creating a processing pipe is performed with
the binary OR operator.

Audio data visualisation can be performed using graphers, such as Waveform and
Spectrogram. All graphers return an image:

 >>> import timeside
 >>> decoder = timeside.decoder.FileDecoder('sweep.wav')
 >>> spectrogram = timeside.grapher.Spectrogram(width=400, height=150)
 >>> (decoder | spectrogram).run()
 >>> spectrogram.render().save('graph.png')

It is possible to create longer pipes, as well as subpipes, here for both
analysis and encoding:

 >>> import timeside
 >>> decoder = timeside.decoder.FileDecoder('sweep.wav')
 >>> levels = timeside.analyzer.Level()
 >>> encoders = timeside.encoder.Mp3Encoder('sweep.mp3') | timeside.encoder.FlacEncoder('sweep.flac')
 >>> (decoder | levels | encoders).run()
 >>> print levels.results

