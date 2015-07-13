News
=====

0.7.1

* fix django version to 1.6.10 (sync with Telemeta 1.5)

0.7

* Code refactoring:

   - Create a new module `timeside.plugins` and move processors therein: timeside.plugins.decoder,analyzer, timeside.plugins.encoder, timeside.plugins.fx
   - WARNING: to properly manage the namespace packages structure, the TimeSide main module is now `timeside.core` and code should now be initialized with `import timeside.core`
   - `timeside.plugins` is now a `namespace package <https://pythonhosted.org/setuptools/setuptools.html#namespace-packages>`_ enabling external plugins to be **automatically** plugged into TimeSide (see for example `timeside-diadems <https://github.com/ANR-DIADEMS/timeside-diadems>`_). This now makes TimeSide a **real** plugin host, yeah!
   - A dummy timeside plugin will soon be provided for easy development start.

* Move all analyzers developped by the partners of the Diadems project to a new repository: `timeside-diadems <https://github.com/ANR-DIADEMS/timeside-diadems>`_
* Many fixes for a better processing by `Travis-CI <https://travis-ci.org/Parisson/TimeSide>`_
* Add a dox file to test the docker building continously on `various distributions <https://github.com/Parisson/Docker>`_

0.6.2

* Bugfix release for #63 #64 #68

0.6.1

* Fix various minor bugs
* Fix docker sandbox
* Auto build docker image (https://registry.hub.docker.com/u/parisson/timeside/)

0.6

  * WARNING! some processor ids have changed. Please see the full list below.
  * NEW analyzers: IRIT Monopoly (see Processors)
  * NEW graphers: IRIT Start/Session segmentation
  * Add extensible buffering thanks to pytables (NEW dependency)
  * Add typed parameters in processors and server thanks to traits (NEW dependency)
  * Add a graph model to the pipe thanks to networkx (NEW dependency)
  * Add test sample generators based on GStreamer
  * Add a background image option for rendering analyzers
  * Add on-the-fly filtering decorators
  * Add a Docker development image and a Dockerfile
  * Add a Vagrant development box
  * Update the Debian package installation procedure
  * Results are now stored in pipe.results as as dictionnary of AnalyzerResults
  * Update various processors
  * Prevent duplication of processor in the pipe (i.e. processors sharing the same class and parameters). This also fix #60.
  * Update of Travis CI scripts https://travis-ci.org/Parisson/TimeSide/

0.5.6

  * Bugfix release
  * Fix analyzer instanciation as parent for some graphers
  * Store analyzer's results in pipe.results by uuid instead of id (fix #24)

0.5.5

 * All processor folders (decoder, analyzer, grapher, encoder) are now real plugin repositories : you can just drop processors in it and play!
 * TimeSide can be installed without Aubio, Yaafe nor Vamp : it should be easier to install on old distributions for which those librairies are difficult or impossible to compile
 * Encoder : add an Opus encoder
 * Experimental : add a django web server with a REST API (see "Web server")
 * AubioPitch: prevent NaN in result by converting them to zero
 * Yaafe analyzer: simplify adaptation of process frames from TimeSide to Yaafe
 * LimsiSad: add a default value for parameter sad_model
 * Fix various NaN and Inf and PEP8 issues also many PyFlake warnings
 * Full `Travis integration <https://travis-ci.org/Parisson/TimeSide/>`_ with tests and test coverage through `coveralls.io <https://coveralls.io/r/Parisson/TimeSide>`_
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

0.4.5

 * (re)fix Pillow support (#12)
 * fix some python package rules
 * add a Debian package directory (thanks to piem, in git repo only)

0.4.4

 * Only setup bugfixes
 * Last compatible version with Python 2.6
 * Next version 0.5 will integrate serious new analyzer features (aubio, yaafe and more)

0.4.3

 * finally fix decoder leaks and de-synchronizations (thanks to piem)
 * this also fixes bad variable encoder file lengths
 * fix OGG and FLAC encoders (closes: #8)
 * fix multi-channels streaming (closes: #13)
 * add support for Pillow (closes: #12)
 * temporally desactivate AAC and WebM encoders (need to add some limits for them)
 * WARNING : we now need to add overwrite=True to encoder kwargs instances in order to overwrite the destination file, i.e. e=Mp3Encoder(path, overwrite=True)

0.4.2

 * many releases these days, but there are some patches which are really worth to be HOT released : we just need them in production..
 * finally fix FFT window border leaks in the streaming spectrum process for *really* better spectrograms and *smoother* spectral centroid waveforms
 * *mv* gstutils to timeside.gstutils
 * cleanup various processes
 * Ogg, Aac and Flac encoders not really working now (some frames missing) :( Will be fixed in next release.

0.4.1

 * move UI static files from ui/ to static/timeside/ (for better django compatibility)
 * upgrade js scripts from telemeta 1.4.4
 * upgrade SoundManager2 to v297a-20120916

0.4.0

 * finally fixed an old decoder bug to prevent memory leaks during hard process (thanks to piem)
 * add blocksize property to the processor API
 * add many unit tests (check tests/alltests.py)
 * re-add UI files (sorry, was missing in the last packages)
 * various bugfixes
 * encoders not all much tested on big files, please test!
 * piem is now preparing some aubio analyzers :P

0.3.3

 * mostly a transitional developer and mantainer version, no new cool features
 * but add "ts-waveforms" script for waveform batching
 * fix some tests
 * removed but download audio samples
 * fix setup
 * update README

0.3.2

 * move mainloop to its own thread to avoid memory hogging on large files
 * add condition values to prepare running gst mainloop in a thread
 * add experimental WebM encoder
 * duration analysis goes to decoder.duration property
 * bugfixes
