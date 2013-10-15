==============================================
TimeSide : open web audio processing framework
==============================================

.. image:: https://secure.travis-ci.org/yomguy/TimeSide.png?branch=master
    :target: http://travis-ci.org/yomguy/TimeSide/

TimeSide is a set of python components enabling audio analysis, imaging, transcoding and streaming. Its high-level API has been designed to enable complex processing on big media data corpus. Its simple plugin architecture can be adapted to various usecases.

It also includes a smart HTML5 interactive user interface embeddable in any web application to provide various media format playback, on the fly transcoding and streaming, fancy waveforms and spectrograms, various low and high level audio analyzers, semantic labelling and segmentation.


Goals
=====

We just *need* a python library to:

 * Do asynchronous and fast audio processing with Python,
 * Decode audio frames from ANY format into numpy arrays,
 * Analyze audio content with some state-of-the-art audio feature extraction libraries,
 * Organize, serialize and save analysis metadata through various formats,
 * Draw various fancy waveforms, spectrograms and other cool graphers,
 * Transcode audio data in various media formats and stream them through web apps,
 * Playback and interact *on demand* through a smart high-level HTML5 extensible player,
 * Index, tag and organize semantic metadata (see `Telemeta <http://telemeta.org>`_ which embed TimeSide).

Here is a schematic diagram of the TimeSide engine architecture:

.. image:: http://timeside.googlecode.com/git/doc/img/timeside_schema.png


Available plugins
=================

 * Decoder:
     - ALL known media formats thanks to Gstreamer

 * Analyzers:
     - MaxLevel, MeanLevel
     - DC
     - any Yaafe data flow
     - Aubio BPM, Beats, MFCC, ...

 * Graphers:
     - WaveForm
     - Contour
     - Spectrogram

 * Encoders:
     - WAV
     - FLAC
     - WebM
     - OGG Vorbis
     - MP3

 * Serializers:
     - YAML
     - JSON
     - XML
     - HDF5

News
=====

0.5.0

 * Deep refactoring of the analyzer API to handle various new usecases, specifically audio feature extraction
 * Add serializable global result container (AnalyzerResultContainer)
 * Add new audio feature extraction thanks to the Aubio library providing beat & BPM detection, pitch dectection and other cool stuff (NEW dependency)
 * Add new audio feature extraction thanks to the Yaafe library (NEW dependency)
 * EXPERIMENTAL : add new audio feature extraction thanks to the VAMP plugin library (NEW dependency)
 * Add new documentation, see http://files.parisson.com/timeside/doc/
 * Provide a Debian repository for instant install (see [Install](#Install))
 * Various bugfixes
 * Comptatible with python >=2.7

0.4.5

 * (re)fix Pillow support (#12)
 * fix some python package rules
 * add a Debian package directory (thanks to piem, in git repo only)

0.4.4

 * Only minor setup bugfixes
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


Install
=======

TimeSide needs some other python modules to run. The following methods explain how to install all dependencies on various Linux based systems.

On Debian, Ubuntu, etc::

 $ echo "deb http://debian.parisson.com/debian/ stable main" | sudo tee -a /etc/apt/sources.list
 $ sudo apt-get update
 $ sudo apt-get install python-timeside

On other system, you'll need to install the Gstreamer framework, some librairies and some python modules (see #Dependencies) ::

 $ sudo pip install timeside

Dependencies
============

python (>=2.7), python-setuptools, python-gst0.10, gstreamer0.10-plugins-good, gstreamer0.10-gnonlin,
gstreamer0.10-plugins-ugly, python-aubio, python-yaafe, python-simplejson, python-yaml, python-h5py


Extensible HTML5 User Interface
================================

TimeSide comes with a smart HTML5 audio player which can drive the process engine through a web server.

Some examples of application:

 * http://parisson.telemeta.org/archives/items/PRS_07_01_03/
 * http://archives.crem-cnrs.fr/items/CNRSMH_I_1956_002_001_01/ (player embedded in a Telemeta session)

The detailed documentation to extend the player:

 * https://github.com/yomguy/TimeSide/wiki/Ui-Guide


Documentation
==============

Engine API : http://code.google.com/p/timeside/source/browse/trunk/timeside/api.py


Related projects
=================

TimeSide has emerged in 2010 from the `Telemeta project <http://telemeta.org>`_ which develops a free and open source web audio CMS.

Some decoders and encoders depend on the great `GStreamer framework <http://gstreamer.freedesktop.org/>`_.


Platforms
=========

The TimeSide engine is intended to work on all Unix / Linux platforms.
MacOS X and Windows versions will soon be explorated.
The player should work on any modern HTML5 enabled browser.
Flash is needed for MP3 if the browser doesn't support it.


Development
===========

For versions >=0.5 on Debian Stable 7.0 Wheezy::

 $ echo "deb http://debian.parisson.com/debian/ stable main" | sudo tee -a /etc/apt/sources.list
 $ echo "deb-src http://debian.parisson.com/debian/ stable main" | sudo tee -a /etc/apt/sources.list
 $ sudo apt-get update
 $ sudo apt-get install git
 $ sudo apt-get build-dep python-timeside

 $ git clone https://github.com/yomguy/TimeSide.git
 $ cd TimeSide
 $ git checkout dev
 $ export PYTHONPATH=$PYTHONPATH:`pwd`
 $ python tests/run_all_tests


API / Documentation
====================

The *source code*, the API and some slides:

 * https://github.com/yomguy/TimeSide
 * http://files.parisson.com/api/timeside/
 * http://files.parisson.com/timeside/timeside/doc/timeside_slides.html


Copyrights
==========

 * Copyright (c) 2006, 2013 Parisson SARL
 * Copyright (c) 2006, 2013 Guillaume Pellerin
 * Copyright (c) 2010, 2013 Paul Brossier
 * Copyright (c) 2013 Thomas Fillon
 * Copyright (c) 2006, 2010 Samalyse SARL


License
=======

TimeSide is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

TimeSide is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See LICENSE for more details.
