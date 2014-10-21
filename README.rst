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
* **Analyze** audio content with some state-of-the-art audio feature extraction libraries like Aubio, Yaafe and VAMP as well as some pure python processors
* **Visualize** sounds with various fancy waveforms, spectrograms and other cool graphers,
* **Transcode** audio data in various media formats and stream them through web apps,
* **Organize**, **serialize** and **save** feature analysis data through various portable formats,
* **Playback** and **interact** **on demand** through a smart high-level HTML5 extensible player,
* **Index**, **tag** and **annotate** audio archives with semantic metadata (see `Telemeta <http://telemeta.org>`__ which embed TimeSide).


Architecture
============

The streaming architecture of TimeSide relies on 2 main parts: a processing engine including various plugin processors written in pure Python and a user interface providing some web based visualization and playback tools in pure HTML5.

.. image:: http://vcs.parisson.com/gitweb/?p=timeside.git;a=blob_plain;f=doc/slides/img/timeside_schema.svg;hb=refs/heads/dev
  :width: 800 px


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

0.5.7

  * Add a Docker development box
  * Add a Vagrant development box
  * Add a Debian package installation procedure
  * Fix parent and child analyzers both using yaafe (fix #60)

0.5.6

  * Bugfix release
  * Fix analyzer instanciation as parent for some graphers

For older news, please visit: https://github.com/yomguy/TimeSide/blob/master/NEWS.rst

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

API / Documentation
====================

* General : http://files.parisson.com/timeside/doc/
* Tutorial : http://files.parisson.com/timeside/doc/tutorial/index.html
* API : http://files.parisson.com/timeside/doc/api/index.html
* Player / UI : https://github.com/yomguy/TimeSide/wiki/Ui-Guide (see also "Web player")
* Examples:

  - http://nbviewer.ipython.org/github/thomasfillon/Timeside-demos/tree/master/
  - https://github.com/yomguy/TimeSide/blob/master/tests/sandbox/example_CMMR.py
  - https://github.com/yomguy/TimeSide/blob/master/tests/sandbox/exempleCMMR_vamp.py

Install
=======

The TimeSide engine is intended to work on all Linux and Unix like platforms.

It depends on several other python modules and compiled librairies like GStreamer.

Debian, Ubuntu
---------------

For Debian based distributions, we provide a safe repository which provides all additional dependencies that are not included in Debian yet. Please follow the instructions on `this page <http://debian.parisson.com/debian/>`_.

Other Linux distributions
--------------------------

On other Linux platforms, you need to install all dependencies listed in the paragraph "Dependencies" (find all equivalent package names for your distribution).

Then, use pip::

 sudo pip install timeside

OSX
---

The installation on OSX platforms is pretty hard at the moment because all dependencies are not in brew. But, it will be fully documented in the next release 0.5.6.

Dependencies
-------------

Needed:

 python (>=2.7) python-setuptools python-numpy python-scipy python-h5py python-matplotlib python-imaging
 python-simplejson python-yaml python-mutagen libhdf5-serial-dev python-tables python-gst0.10
 gstreamer0.10-gnonlin gstreamer0.10-plugins-good gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly

Optional:

 aubio (>=0.4.1) yaafe python-aubio python-yaafe vamp-examples
 django (>=1.4) django-south djangorestframework django-extensions

User Interfaces
===============

Python
-------

Of course all the TimeSide are available in our beloved python envionment.
As IPython is really great for discovering objects with completion, writing notebooks, we strongly advise to install and use it::

  sudo apt-get install ipython
  ipython
  >>> import timeside


Shell
------

Of course, TimeSide can be used in any python environment. But, a shell script is also provided to enable preset based and recursive processing through your command line interface::

 timeside-launch -h
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


Find some preset examples in examples/presets/


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

A sandbox is provided in timeside/server/sandbox and you can initialize it and test it like this::

  cd examples/sandbox
  ./manage.py syncdb
  ./manage.py migrate
  ./manage.py runserver

and browse http://localhost:8000/api/

At the moment, this server is NOT connected to the player using TimeSide alone. Please use Telemeta.

Development
===========

First, install TimeSide (see Install).

Then::

 sudo apt-get install git
 git clone https://github.com/yomguy/TimeSide.git
 cd TimeSide
 git checkout dev
 sudo pip install -e .
 echo "export PYTHONPATH=$PYTHONPATH:`pwd`" >> ~/.bashrc
 source ~/.bashrc
 tests/run_all_tests

VirtualBox and Vagrant
-----------------------

We also provide a vagrant box to install a virtual Debian system including TimeSide and all other dependencies.
First, install Vagrant and VirtualVox::

 sudo apt-get install vagrant virtualbox

On other OS, we need to install the packages correponding to your system:

 * Vagrant: https://www.vagrantup.com/downloads.html
 * VirtualBox: https://www.virtualbox.org/wiki/Downloads

Then setup our image box like this in a terminal::

 vagrant box add parisson/timeside-wheezy64 http://files.parisson.com/vagrant/timeside/parisson-timeside-wheezy64.box
 vagrant init parisson/timeside-wheezy64
 vagrant up
 vagrant ssh

To stop the virtual box::

 exit
 vagrant halt


Docker
-------

Docker is a great tool for developping and deploying processing environments! Our docker container includes all the necessary packages and environments for development and production with TimeSide.

First, install Docker: https://docs.docker.com/installation/

Then, simply pull our dev image and run::

  sudo docker pull yomguy/timeside
  sudo docker run -i -t yomguy/timeside bash

More infos: https://registry.hub.docker.com/u/yomguy/timeside/

To start the web server through the container::

  sudo docker run -p 9000:80 yomguy/timeside supervisord -n

Finally browse http://localhost:9000/api/

To start a new development, it is advised to checkout the dev branch and build your own container::

  cd TimeSide
  git checkout dev
  sudo docker build .

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

    * `Telemeta <http://telemeta.org>`__ : open web audio platform
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
* Copyright (c) 2006, 2010 Olivier Guilyardi


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

