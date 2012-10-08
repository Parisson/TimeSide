==============================================
TimeSide : open and fast web audio components
==============================================

.. image:: https://secure.travis-ci.org/yomguy/TimeSide.png?branch=master
    :target: http://travis-ci.org/yomguy/TimeSide/

TimeSide is a set of python components enabling easy audio processing, transcoding, imaging and streaming. Its simple architecture and high-level API have been design to process serial pipelines.

It includes a powerfull HTM5 interactive player which can be embedded in any web application to provide fancy waveforms, various analyzer results, synced time metadata display during playback and remote indexing.

The engine (server side) is fully written in Python, the player (client side) in HTML, CSS and JavaScript.

Goals
=====

We just *need* a python library to:

 * forget Matlab,
 * build a python framework to do asynchronous audio processing,
 * decode audio frames from ANY format to numpy arrays,
 * stream the frames in processors and do numpy data analyzing,
 * create various waveforms, spectrograms, etc.. with numpy and PIL,
 * transcode the processed frames in various media formats and stream it,
 * provide a high-level HTML5 UI to stream the results *on demand* through the web,
 * do temporal metadata indexing remotely.


News
=====

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
 >>> decoder  =  timeside.decoder.FileDecoder('source.wav')
 >>> grapher  =  timeside.grapher.Waveform()
 >>> analyzer =  timeside.analyzer.MaxLevel()
 >>> encoder  =  timeside.encoder.Mp3Encoder('output.mp3')

then, the *magic* pipeline::

 >>> (decoder | grapher | analyzer | encoder).run()

get the results::

 >>> grapher.render(output='image.png')
 >>> print 'Level:', analyzer.result()

finally see image.png and play output.mp3 ;)


More examples
=============

 * http://code.google.com/p/timeside/
 * http://code.google.com/p/timeside/wiki/PythonApi
 * https://github.com/yomguy/TimeSide/tree/master/scripts/batch/
 * http://archives.crem-cnrs.fr/items/CNRSMH_I_1956_002_001_01/ (player embedded in a Telemeta session)


Related projects
=================

TimeSide has emerged in 2010 from the `Telemeta project <http://telemeta.org>`_ which develops a free and open-source web audio CMS.

Some decoders and encoders depend on the great `GStreamer framework <http://gstreamer.freedesktop.org/>`_.


APIs
====

Engine API : http://code.google.com/p/timeside/source/browse/trunk/timeside/api.py

Player API and guide : http://code.google.com/p/timeside/wiki/UiGuide


Platforms
=========

The TimeSide engine is intended to work on all Unix / Linux platforms, but MacOS X and Windows versions will soon be explorated.

The player should work on any modern HTML5 enabled browser. Flash is needed for MP3 if the browser doesn't support it.


Install
=======

TimeSide needs some other python modules to run. The following methods explain how to install all dependencies on a Debian based system like Debian, Ubuntu, etc.. On Fedora and Red-Hat you might replace 'apt-get by 'yum', on Gentoo by 'emerge', or any other package manager you like::

 $ sudo apt-get update
 $ sudo apt-get install python python-pip python-setuptools python-gobject \
                        python-gst0.10 gstreamer0.10-plugins-base gir1.0-gstreamer-0.10 \
                        gstreamer0.10-plugins-good gstreamer0.10-plugins-bad \
                        gobject-introspection

 $ sudo pip install timeside

To get non-free (MP3, MP4, AAC, etc) decoding and encoding features, add Debian Multimedia repository and install the modules::

 $ echo "deb http://www.deb-multimedia.org stable main non-free" | sudo tee -a /etc/apt/sources.list
 $ sudo apt-get update
 $ apt-get install gstreamer0.10-lame gstreamer0.10-plugins-really-bad gstreamer0.10-plugins-ugly


Batching
=========

TimeSide provides *ts-waveforms*, a waveform rendering batch script. Usage::

 $ ts-waveforms /path/to/media_dir /path/to/img_dir

Please use absolute paths. For example::

 $ ts-waveforms /home/$user/music/mp3/ /home/$USER/images/

To change the color scheme or the size of the waveforms, edit the script from the source and change the variables of the GrapherScheme object::

 $ git clone git://github.com/yomguy/TimeSide.git
 $ cd timeside/scripts/
 $ vi ts-waveforms
 $ ./ts-waveforms /home/$user/music/mp3/ /home/$USER/images/


Packages included
=================

 * SoundManager 2 >= 2.91 (http://www.schillmania.com/projects/soundmanager2)
 * jQuery => 1.2.6 (http://www.jquery.com)
 * jsGraphics => 3.03 (http://www.walterzorn.com/jsgraphics/jsgraphics_e.htm)


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


Development
===========

 * http://code.google.com/p/timeside/
 * https://github.com/yomguy/TimeSide


Copyrights
==========

 * Copyright (c) 2006, 2012 Parisson SARL
 * Copyright (c) 2006, 2012 Guillaume Pellerin
 * Copyright (c) 2010, 2012 Paul Brossier
 * Copyright (c) 2006, 2010 Samalyse SARL


