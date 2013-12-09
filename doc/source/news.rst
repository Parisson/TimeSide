News
=====

0.5.2

 * Add a general launch script "timeside-launch" (see "User interface")
 * Add some pre-processing decorators to downmix and filter inputs of processors (see analyzer.waveform for ex)
 * Add a fake numpy decoder to setup multi-pass process pipes
 * Add beat confidence to aubio_temporal
 * Add AAC encoder (gstreamer voaacenc plugin needed)
 * Add UUIDs to the file URI and to all processors
 * Add a Debian repository with all dependencies for i386 and amd64 architectures
 * Fix WebM encoder
 * Fix MP3 muxing
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
 * EXPERIMENTAL : add new audio feature extraction thanks to the VAMP plugin library (NEW dependency on some vamp toold)
 * Add new documentation : http://files.parisson.com/timeside/doc/
 * New Debian repository for instant install
 * Various bugfixes
 * Comptatible with Python >=2.7
 * WARNING : no longer compatible with Telemeta 1.4.5

0.4.5

 * (re)fix Pillow support (#12)
 * fix some Python package rules
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

