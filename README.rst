==============================================
TimeSide : open web audio processing framework
==============================================

TimeSide is a set of python components enabling low and high level audio analysis, imaging, transcoding and streaming. Its high-level API is designed to enable complex processing on large datasets of audio and video assets of any format. Its simple plug-in architecture can be adapted to various use cases.

TimeSide also includes a smart interactive HTML5 player which provides various streaming playback functions, formats selectors, fancy audio visualizations, segmentation and semantic labelling synchronized with audio events. It is embeddable in any web application.


Build status
============
- Branch **master** : |travis_master| |coveralls_master|
- Branch **dev** : |travis_dev| |coveralls_dev|

.. |travis_master| image:: https://secure.travis-ci.org/yomguy/TimeSide.png?branch=master
    :target: https://travis-ci.org/yomguy/TimeSide/

.. |travis_dev| image:: https://secure.travis-ci.org/yomguy/TimeSide.png?branch=dev
    :target: https://travis-ci.org/yomguy/TimeSide/

.. |coveralls_master| image:: https://coveralls.io/repos/yomguy/TimeSide/badge.png?branch=master
  :target: https://coveralls.io/r/yomguy/TimeSide?branch=master

.. |coveralls_dev| image:: https://coveralls.io/repos/yomguy/TimeSide/badge.png?branch=dev
  :target: https://coveralls.io/r/yomguy/TimeSide?branch=dev



Goals
======

* **Do** asynchronous and fast audio processing with Python,
* **Decode** audio frames from **any** audio or video media format into numpy arrays,
* **Analyze** audio content with some state-of-the-art audio feature extraction libraries,
* **Organize**, serialize and save analysis metadata through various formats,
* **Draw** various fancy waveforms, spectrograms and other cool visualizers,
* **Transcode** audio data in various media formats and stream them through web apps,
* **Playback** and **interact** **on demand** through a smart high-level HTML5 extensible player,
* **Index**, **tag** and **organize semantic metadata** (see `Telemeta <http://telemeta.org>`_ which embed TimeSide).


Architecture
============

The streaming architecture of TimeSide relies on 2 main parts: a processing engine including various plugin processors written in pure Python and a user interface providing some web based visualization and playback tools in pure HTML5.

.. image:: http://vcs.parisson.com/gitweb/?p=timeside.git;a=blob_plain;f=doc/slides/img/timeside_schema.svg;hb=refs/heads/dev


Processors
==========

IDecoder
---------

  * FileDecoder [gst_dec]
  * ArrayDecoder [array_dec]
  * LiveDecoder [gst_live_dec]

IAnalyzer
---------

  *  AubioTemporal [aubio_temporal]
  *  AubioPitch [aubio_pitch]
  *  AubioMfcc [aubio_mfcc]
  *  AubioMelEnergy [aubio_melenergy]
  *  AubioSpecdesc [aubio_specdesc]
  *  Yaafe [yaafe]
  *  Spectrogram [spectrogram_analyzer]
  *  Waveform [waveform_analyzer]
  *  VampSimpleHost [vamp_simple_host]
  *  IRITSpeechEntropy [irit_speech_entropy]
  *  IRITSpeech4Hz [irit_speech_4hz]
  *  OnsetDetectionFunction [odf]
  *  LimsiSad [limsi_sad]

IValueAnalyzer
---------------

  * Level [level]
  * MeanDCShift [mean_dc_shift]

IGrapher
---------

  *  Waveform [waveform_simple]
  *  WaveformCentroid [waveform_centroid]
  *  WaveformTransparent [waveform_transparent]
  *  WaveformContourBlack [waveform_contour_black]
  *  WaveformContourWhite [waveform_contour_white]
  *  SpectrogramLog [spectrogram_log]
  *  SpectrogramLinear [spectrogram_lin]
  *  Display.aubio_pitch.pitch [grapher_aubio_pitch]
  *  Display.odf [grapher_odf]
  *  Display.waveform_analyzer [grapher_waveform]
  *  Display.irit_speech_4hz.segments [grapher_irit_speech_4hz_segments]

IEncoder
---------

  * VorbisEncoder [gst_vorbis_enc]
  * WavEncoder [gst_wav_enc]
  * Mp3Encoder [gst_mp3_enc]
  * FlacEncoder [gst_flac_enc]
  * AacEncoder [gst_aac_enc]
  * WebMEncoder [gst_webm_enc]
  * OpusEncoder [gst_opus_enc]
  * AudioSink [gst_audio_sink_enc]

News
=====

0.5.5

 * All processor folders (decoder, analyzer, grapher, encoder) are now real plugin repositories : you can just drop processors in it and play!
 * TimeSide can be installed without Aubio, Yaafe nor Vamp : it should be easier to install on old distributions for which those librairies are difficult or impossible to compile
 * Experimental : add a django web server with a REST API (see Interface : web server)
 * Encoder : add an Opus encoder
 * AubioPitch: prevent NaN in result by converting them to zero
 * Yaafe analyzer: simplify adaptation of process frames from TimeSide to Yaafe
 * LimsiSad: add a default value for parameter sad_model
 * Fix various NaN and Inf and PEP8 issues also many PyFlake warnings
 * Full Travis integration
 * Thanks to all contributors!

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
 * EXPERIMENTAL : add new audio feature extraction thanks to the VAMP plugin library (NEW dependency on some vamp toold)
 * Add new documentation : http://files.parisson.com/timeside/doc/
 * New Debian repository for instant install
 * Various bugfixes
 * Comptatible with Python >=2.7
 * WARNING : no longer compatible with Telemeta 1.4.5


Dive in
========

To list all available plugins::

 >>> import timeside
 >>> timeside.core.list_processors()

Define some processors::

 >>> from timeside.core import get_processor
 >>> decoder  =  get_processor('gst_dec')('sweep.wav')
 >>> grapher  =  get_processor('waveform_simple')
 >>> analyzer =  get_processor('level')
 >>> encoder  =  get_processor('gst_vorbis_enc')('sweep.ogg')

Then run the *magic* pipeline::

 >>> (decoder | grapher | analyzer | encoder).run()

Render the grapher results::

 >>> grapher.render(output='waveform.png')

Show the analyzer results::

 >>> print 'Level:', analyzer.results

The encoded OGG file should also be there...

Note you can also instanciate each processor with its own class::
 
 >>> decoder  =  timeside.decoder.file.FileDecoder('sweep.wav')
 >>> grapher  =  timeside.grapher.waveform_simple.Waveform()
 >>> analyzer =  timeside.analyzer.level.Level()
 >>> encoder  =  timeside.encoder.ogg.VorbisEncoder('sweep.ogg')
 
For more extensive examples, please see the `http://files.parisson.com/timeside/doc/ <full documentation>`_.

API / Documentation
====================

* General : http://files.parisson.com/timeside/doc/
* Tutorial : http://files.parisson.com/timeside/doc/tutorial/index.html
* API : http://files.parisson.com/timeside/doc/api/index.html
* Player / UI : https://github.com/yomguy/TimeSide/wiki/Ui-Guide (see also "Web Interface")
* Examples:

  - http://nbviewer.ipython.org/github/thomasfillon/AES53-timeside-demos/tree/master/
  - https://github.com/yomguy/TimeSide/blob/master/tests/sandbox/example_CMMR.py
  - https://github.com/yomguy/TimeSide/blob/master/tests/sandbox/exempleCMMR_vamp.py

Install
=======

The TimeSide engine is intended to work on all Linux and Unix like platforms.

It depends on several other python modules and compiled librairies like GStreamer. 

Debian, Ubuntu
---------------

For Debian based distributions, we provide a safe repository which provides all additional dependencies that are not included in Debian yet:

.. code-block:: bash

 $ echo "deb http://debian.parisson.com/debian/ stable main" | sudo tee -a /etc/apt/sources.list
 $ sudo apt-get update
 $ sudo apt-get install python-timeside

This method is known to be compatible with Debian 7 Wheezy and Ubuntu 14.04 LTS. It will install additional binary packages from several audio feature extraction librairies like Aubio and Yaafe for which TimeSide has some nice processors.

Note you can also use pip if you already have already satisfied all the dependencies::

 $ sudo pip install timeside

Other Linux distributions
--------------------------

On other Linux platforms, you need to install all dependencies listed at the paragraph `Dependencies <#dependencies>`_ (find all equivalent package names for your distribution). 

Then, use pip::
 
 $ sudo pip install timeside

OSX
---

The installation on OSX platforms is pretty hard at the moment because all dependencies are not in brew. But, it will be fully documented in the next release 0.5.6.

Dependencies
-------------

Needed::

 python python-setuptools python-numpy python-scipy python-h5py python-matplotlib pillow 
 python-simplejson python-yaml libhdf5-serial-dev python-gst0.10 gstreamer0.10-gnonlin 
 gstreamer0.10-plugins-good gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly 

Optional::

 aubio yaafe python-aubio python-yaafe vamp-examples
 django django-south djangorestframework django-extensions
User Interfaces
===============

Shell
------

Of course, TimeSide can be used in any python environment. But, a shell script is also provided to enable preset based and recursive processing through your command line interface::

 $ timeside-launch -h
 Usage: scripts/timeside-launch [options] -c file.conf file1.wav [file2.wav ...]
  help: scripts/timeside-launch -h

 Options:
  -h, --help            show this help message and exit
  -v, --verbose         be verbose
  -q, --quiet           be quiet
  -C <config_file>, --conf=<config_file>
                        configuration file
  -s <samplerate>, --samplerate=<samplerate>
                        samplerate at which to run the pipeline
  -c <channels>, --channels=<channels>
                        number of channels to run the pipeline with
  -b <blocksize>, --blocksize=<blocksize>
                        blocksize at which to run the pipeline
  -a <analyzers>, --analyzers=<analyzers>
                        analyzers in the pipeline
  -g <graphers>, --graphers=<graphers>
                        graphers in the pipeline
  -e <encoders>, --encoders=<encoders>
                        encoders in the pipeline
  -R <formats>, --results-formats=<formats>
                        list of results output formats for the analyzers
                        results
  -I <formats>, --images-formats=<formats>
                        list of graph output formats for the analyzers results
  -o <outputdir>, --ouput-directory=<outputdir>
                        output directory

Web player
-----------

TimeSide comes with a smart and pure **HTML5** audio player.

Features:
    * embed it in any audio web application
    * stream, playback and download various audio formats on the fly
    * synchronize sound with text, bitmap and vectorial events
    * seek through various semantic, analytic and time synced data
    * fully skinnable with CSS style

Screenshot:
 .. image:: https://raw.github.com/yomguy/TimeSide/master/doc/slides/img/timeside_player_01.png

Examples of the player embeded in the Telemeta open web audio CMS:
    * http://parisson.telemeta.org/archives/items/PRS_07_01_03/
    * http://archives.crem-cnrs.fr/items/CNRSMH_I_1956_002_001_01/

Development documentation:
    * https://github.com/yomguy/TimeSide/wiki/Ui-Guide

TODO list:
    * zoom
    * layers


Web server
-----------

An EXPERIMENTAL web server based on Django has been added to the package from version 0.5.5. The goal is to provide a full REST API to TimeSide to enable new kinds of audio processing web services.

A sandbox is provide in timeside/server/sandbox and you can initialize it and test it like this:

.. code-block:: bash

  $ cd timeside/server/sandbox
  $ ./manage.py syncdb
  $ ./manage.py migrate
  $ ./manage.py runserver

and browse http://localhost:8000/api/

At the moment, this server is NOT connected to the player using TimeSide alone. Please use Telemeta.


Development
===========

For versions >=0.5 on Debian 7 Wheezy:

.. code-block:: bash

 $ echo "deb http://debian.parisson.com/debian/ stable main" | sudo tee -a /etc/apt/sources.list
 $ echo "deb-src http://debian.parisson.com/debian/ stable main" | sudo tee -a /etc/apt/sources.list
 $ sudo apt-get update
 $ sudo apt-get install git
 $ sudo apt-get build-dep python-timeside

 $ git clone https://github.com/yomguy/TimeSide.git
 $ cd TimeSide
 $ git checkout dev
 $ sudo pip install -e .
 $ python tests/run_all_tests

Sponsors and Partners
=====================

    * `Parisson <http://parisson.com>`_
    * `CNRS <http://www.cnrs.fr>`_ (National Center of Science Research, France)
    * `Huma-Num <http://www.huma-num.fr/>`_ (big data equipment for digital humanities, ex TGE Adonis)
    * `CREM <http://www.crem-cnrs.fr>`_ (french National Center of Ethomusicology Research, France)
    * `Université Pierre et Marie Curie <http://www.upmc.fr>`_ (UPMC Paris, France)
    * `ANR <http://www.agence-nationale-recherche.fr/>`_ (CONTINT 2012 project : DIADEMS)
    * `MNHN <http://www.mnhn.fr>`_ : Museum National d'Histoire Naturelle (Paris, France)


Related projects
=================

    * `Telemeta <http://telemeta.org>`_ : open web audio platform
    * `Sound archives <http://archives.crem-cnrs.fr/>`_ of the CNRS, CREM and the "Musée de l'Homme" in Paris, France.
    * The `DIADEMS project <http://www.irit.fr/recherches/SAMOVA/DIADEMS/en/welcome/>`_ sponsored by the ANR.



Copyrights
==========

* Copyright (c) 2006, 2014 Parisson SARL
* Copyright (c) 2006, 2014 Guillaume Pellerin
* Copyright (c) 2010, 2014 Paul Brossier
* Copyright (c) 2013, 2014 Thomas Fillon
* Copyright (c) 2013, 2014 Maxime Lecoz
* Copyright (c) 2013, 2014 David Doukhan
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

