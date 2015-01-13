==============================================
TimeSide : open web audio processing framework
==============================================

|version| |downloads| |travis_master| |coveralls_master|

.. |travis_master| image:: https://secure.travis-ci.org/Parisson/TimeSide.png?branch=master
    :target: https://travis-ci.org/Parisson/TimeSide/

.. |coveralls_master| image:: https://coveralls.io/repos/yomguy/TimeSide/badge.png?branch=master
  :target: https://coveralls.io/r/yomguy/TimeSide?branch=master

.. |version| image:: https://pypip.in/version/TimeSide/badge.png
  :target: https://pypi.python.org/pypi/TimeSide/
  :alt: Version

.. |downloads| image:: https://pypip.in/download/TimeSide/badge.svg
    :target: https://pypi.python.org/pypi/TimeSide/
    :alt: Downloads

TimeSide is a set of python components enabling low and high level audio analysis, imaging, transcoding and streaming. Its high-level API is designed to enable complex processing on large datasets of audio and video assets of any format. Its simple plug-in architecture can be adapted to various use cases.

TimeSide also includes a smart interactive HTML5 player which provides various streaming playback functions, formats selectors, fancy audio visualizations, segmentation and semantic labelling synchronized with audio events. It is embeddable in any web application.


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


Funding and Support
===================

To fund the project and continue our fast development process, we need your explicit support. So if you use TimeSide in production or even in development, please let us know:

 * star or fork the project on `GitHub <https://github.com/Parisson/TimeSide>`_
 * tweet something to `@parisson_studio <https://twitter.com/parisson_studio>`_ or `@yomguy <https://twitter.com/yomguy>`_
 * drop us an email <support@parisson.com>

Thanks for your help!

Architecture
============

The streaming architecture of TimeSide relies on 2 main parts: a processing engine including various plugin processors written in pure Python and a user interface providing some web based visualization and playback tools in pure HTML5.

.. image:: http://vcs.parisson.com/gitweb/?p=timeside.git;a=blob_plain;f=doc/slides/img/timeside_schema.svg;hb=refs/heads/dev
  :width: 800 px

Dive in
========

To list all available plugins::

 import timeside
 timeside.core.list_processors()

Define some processors::

 from timeside.core import get_processor
 decoder  =  get_processor('file_decoder')('sweep.wav')
 grapher  =  get_processor('waveform_simple')
 analyzer =  get_processor('level')
 encoder  =  get_processor('vorbis_encoder')('sweep.ogg')

Then run the *magic* pipeline::

 (decoder | grapher | analyzer | encoder).run()

Render the grapher results::

 grapher.render(output='waveform.png')

Show the analyzer results::

 print 'Level:', analyzer.results

The encoded OGG file should also be there...

For more extensive examples, please see the `full documentation <http://files.parisson.com/timeside/doc/>`_.


News
=====

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

For older news, please visit: https://github.com/Parisson/TimeSide/blob/master/NEWS.rst

Processors
==========

IEncoder
--------

   * **live_encoder** : Gstreamer-based Audio Sink
   * **flac_encoder** : FLAC encoder based on Gstreamer
   * **aac_encoder** : AAC encoder based on Gstreamer
   * **mp3_encoder** : MP3 encoder based on Gstreamer
   * **vorbis_encoder** : OGG Vorbis encoder based on Gstreamer
   * **opus_encoder** : Opus encoder based on Gstreamer
   * **wav_encoder** : WAV encoder based on Gstreamer
   * **webm_encoder** : WebM encoder based on Gstreamer

IDecoder
--------

   * **array_decoder** : Decoder taking Numpy array as input
   * **file_decoder** : File Decoder based on Gstreamer
   * **live_decoder** : Live source Decoder based on Gstreamer

IGrapher
--------

   * **grapher_aubio_pitch** : Image representing Aubio Pitch
   * **grapher_onset_detection_function** : Image representing Onset detection function
   * **grapher_waveform** : Image representing Waveform from Analyzer
   * **grapher_irit_speech_4hz_segments** : Image representing Irit 4Hz Speech Segmentation
   * **grapher_irit_speech_4hz_segments_median** : Image representing Irit 4Hz Speech Segmentation with median filter
   * **grapher_monopoly_segments** : Image representing Irit Monopoly Segmentation
   * **grapher_limsi_sad_etape** : Image representing LIMSI SAD with ETAPE model
   * **grapher_limsi_sad_maya** : Image representing LIMSI SAD with Mayan model
   * **grapher_irit_startseg** : Image representing IRIT Start Noise
   * **spectrogram_log** : Logarithmic scaled spectrogram (level vs. frequency vs. time).
   * **spectrogram_lin** : Linear scaled spectrogram (level vs. frequency vs. time).
   * **waveform_simple** : Simple monochrome waveform image.
   * **waveform_centroid** : Waveform where peaks are colored relatively to the spectral centroids of each frame buffer.
   * **waveform_contour_black** : Black amplitude contour waveform.
   * **waveform_contour_white** : an white amplitude contour wavform.
   * **waveform_transparent** : Transparent waveform.

IAnalyzer
---------

   * **mean_dc_shift** : Mean DC shift analyzer
   * **level** : Audio level analyzer
   * **aubio_melenergy** : Aubio Mel Energy analyzer
   * **aubio_mfcc** : Aubio MFCC analyzer
   * **aubio_pitch** : Aubio Pitch estimation analyzer
   * **aubio_specdesc** : Aubio Spectral Descriptors collection analyzer
   * **aubio_temporal** : Aubio Temporal analyzer
   * **yaafe** : Yaafe feature extraction library interface analyzer
   * **irit_monopoly** : Segmentor Monophony/Polyphony based on the analysis of yin confidence.
   * **irit_startseg** : Segmentation of recording sessions into 'start' and 'session' segments
   * **irit_speech_4hz** : Speech Segmentor based on the 4Hz energy modulation analysis.
   * **irit_speech_entropy** : Speech Segmentor based on Entropy analysis.
   * **limsi_sad** : Limsi Speech Activity Detection Systems
   * **spectrogram_analyzer** : Spectrogram image builder with an extensible buffer based on tables
   * **onset_detection_function** : Onset Detection Function analyzer
   * **spectrogram_analyzer_buffer** : Spectrogram image builder with an extensible buffer based on tables
   * **waveform_analyzer** : Waveform analyzer

IEffect
-------

   * **fx_gain** : Gain effect processor

API / Documentation
====================

* General : http://files.parisson.com/timeside/doc/
* Tutorial : http://files.parisson.com/timeside/doc/tutorial/index.html
* API : http://files.parisson.com/timeside/doc/api/index.html
* Publications : https://github.com/Parisson/Telemeta-doc
* Player / UI : https://github.com/Parisson/TimeSide/wiki/Ui-Guide (see also "Web player")
* Notebooks : http://nbviewer.ipython.org/github/thomasfillon/Timeside-demos/tree/master/
* Example : http://archives.crem-cnrs.fr/archives/items/CNRSMH_E_2004_017_001_01/

Install
=======

The TimeSide engine is intended to work on all Linux and Unix like platforms. It depends on several other python modules and compiled libraries like GStreamer.

Debian, Ubuntu
---------------

For Debian based distributions, we provide a safe repository giving additional dependencies that are not included in Debian yet. Please follow the instructions on `this page <http://debian.parisson.com/debian/>`_.

Other Linux distributions
--------------------------

On other Linux platforms, you need to install all dependencies listed in Dependencies finding all equivalent package names for your distribution.

Then, use pip::

 sudo pip install timeside

OSX / Windows
--------------

Native install is hard at the moment but you can either run our Vagrant or Docker images (see Development).

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
 .. image:: https://raw.github.com/Parisson/TimeSide/master/doc/slides/img/timeside_player_01.png

Examples of the player embeded in the Telemeta open web audio CMS:
    * http://parisson.telemeta.org/archives/items/PRS_07_01_03/
    * http://archives.crem-cnrs.fr/items/CNRSMH_I_1956_002_001_01/

Development documentation:
    * https://github.com/Parisson/TimeSide/wiki/Ui-Guide

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

|travis_dev| |coveralls_dev|

.. |travis_dev| image:: https://secure.travis-ci.org/Parisson/TimeSide.png?branch=dev
    :target: https://travis-ci.org/Parisson/TimeSide/

.. |coveralls_dev| image:: https://coveralls.io/repos/yomguy/TimeSide/badge.png?branch=dev
  :target: https://coveralls.io/r/yomguy/TimeSide?branch=dev


Docker (recommended)
--------------------

Docker is a great tool for developing and deploying processing environments. We provide a docker image which contains TimeSide and all the necessary packages (nginx, uwsgi, etc) to run it either in development or in production stages.

First, install Docker: https://docs.docker.com/installation/

Then, simply pull the image and run it::

  docker pull parisson/timeside
  docker run -p 9000:80 parisson/timeside

You can now browse the TimeSide API: http://localhost:9000/api/

or get a shell session::

  docker run -ti parisson/timeside bash

To start a new development, it is advised to checkout the dev branch in the container::

  cd /opt/TimeSide
  git checkout dev

or get our latest-dev image::

  docker pull parisson/timeside:latest-dev

More infos: https://registry.hub.docker.com/u/parisson/timeside/


VirtualBox and Vagrant (deprecated)
-----------------------------------

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


Native
-------

First, install TimeSide (see Install).

Then::

 sudo apt-get build-dep python-timeside
 sudo apt-get install git
 git clone https://github.com/Parisson/TimeSide.git
 cd TimeSide
 git checkout dev
 sudo pip install -e .
 echo "export PYTHONPATH=$PYTHONPATH:`pwd`" >> ~/.bashrc
 source ~/.bashrc
 tests/run_all_tests


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

* Copyright (c) 2006, 2014 Parisson Sarl
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

