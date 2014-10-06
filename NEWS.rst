News
=====

0.5.6

  * Bugfix release
  * Fix analyzer instanciation as parent for some graphers

0.5.5

 * All processor folders (decoder, analyzer, grapher, encoder) are now real plugin repositories : you can just drop processors in it and play!
 * TimeSide can be installed without Aubio, Yaafe nor Vamp : it should be easier to install on old distributions for which those librairies are difficult or impossible to compile
 * Encoder : add an Opus encoder
 * Experimental : add a django web server with a REST API (see "Web server")
 * AubioPitch: prevent NaN in result by converting them to zero
 * Yaafe analyzer: simplify adaptation of process frames from TimeSide to Yaafe
 * LimsiSad: add a default value for parameter sad_model
 * Fix various NaN and Inf and PEP8 issues also many PyFlake warnings
 * Full `Travis integration <https://travis-ci.org/yomguy/TimeSide/>`_ with tests and test coverage through `coveralls.io <https://coveralls.io/r/yomguy/TimeSide>`_
 * Thanks to all contributors!
 * WARNING: some of the processor paths used in your app could have moved between 0.5.4 and 0.5.5. Check them with timeside.core.processors(). Note that it is now advised to use the timeside.core.get_processor() method to instantiate the processors with their respective id as argument.
 * UPGRADING from the sources: please remove all .pyc files from your repository.

0.5.4

 * Encoder : transcoded streams where broken. Now fixed with some smart thread controls.
 * Analyzer : update VAMP plugin example in sandbox
 * Analyzer : new *experimental* plugin : Limsi Speech Activity Detection Systems (limsi_sad)
 * Decoder : process any media in streaming mode giving its URL
 * Install : fix some setup requirements

0.5.3

 * Make Analyzer rendering more generic and easy to implement
 * Analyzer : implement rendering capability for event and segment + add some more analyzer graphers
 * Analyzer : refactoring the results rendering method. + Capability to use matplotlib in environnement with no display
 * Decoder : Add a Live decoder to get data from the soundcard
 * Decoder : add support for 96kHz sampling rate
 * Encoder: live AudioSink encoder, encoder that plays the audio stream through the soundcard
 * Grapher : add a generic Class to display Analyzers through their 'render' method. Add the new grapher file
 * Grapher : add a generic Class to display Analyzers through their 'render' method. For now, it only support FrameValueResult analyzer
 * Core : add a condition to catch signal only if a LiveDecoder source is used
 * Various bugfixes

0.5.2

 * Add a general launch script "timeside-launch" (see "Shell interface")
 * Add some decorators to filter the inputs of processes (see analyzer.waveform for ex)
 * Add a "stack" option to the FileDecoder to accumulate audio data allowing multipass processes
 * Add beat confidence to aubio_temporal
 * Add AAC encoder (gstreamer voaacenc plugin needed)
 * Add UUIDs to the file URI and to all processors
 * Add a Debian repository with all dependencies for i386 and amd64 architectures
 * Fix buggy WebM encoder
 * Fix buggy MP3 muxing
 * Fix various minor bugs

0.5.1

 * Add *parent* processor list to Processor
 * Simplify and optimize the grapher system
 * Add Grapher abstract generic class
 * Add a UUID property to Processor
 * Add a SpectrogramLinear grapher
 * Add WaveformTransparent grapher
 * Fix some assignment issues regarding immutable type in for Analyzer Result
 * Simplify analyzer results implementation by introducing a Factory and multiple classes and subclasses to handle the 8 different kinds of results
 * Add doctests and improve the unit tests
 * Add a OnsetDetectionFunction analyzer
 * Update documentation
 * Various cleanups
 * Various bugfixes

0.5.0

 * Deep refactoring of the analyzer API to handle various new usecases, specifically audio feature extraction
 * Add serializable global result container (NEW dependency to h5py, json, yaml)
 * Add new audio feature extraction analyzers thanks to the Aubio library providing beat & BPM detection, pitch dectection and other cool stuff (NEW dependency on aubio)
 * Add new audio feature extraction analyzers thanks to the Yaafe library (NEW dependency on yaafe)
 * Add new IRIT speech detection analyzers (NEW dependency on scipy)
 * EXPERIMENTAL : add new audio feature extraction thanks to the VAMP plugin library (NEW dependency on some vamp tools)
 * Add new documentation : http://files.parisson.com/timeside/doc/
 * New Debian repository for instant install
 * Various bugfixes
 * Comptatible with Python >=2.7
 * WARNING : no longer compatible with Telemeta 1.4.5
