==============================================
TimeSide : open and fast web audio components
==============================================

TimeSide is a set of client and server side components for audio-enabling web sites and applications.

It includes a powerful DHTML-based interactive player, with support for time-marking.
The server side components provide generic APIs for easy transcoding, metadata embedding,
sound visualization and audio analysis.

News
=====

0.3.2

 * move mainloop to its own thread to avoid memory hogging on large files
 * add condition values to prepare running gst mainloop in a thread
 * add experimental WebM encoder
 * duration analysis goes to decoder.duration property
 * bugfixes


Platforms
=========

TimeSide is intended to work on all Unix / Linux platforms.
MacOS X and Windows versions will soon be explorated.

It is mostly written in Python and JavaScript / CSS / HTML


Install and usage
==================

See INSTALL.rst


Dependencies
============

  * python (>= 2.4)
  * python-xml
  * python-mutagen
  * python-imaging (>= 1.1.6)
  * python-numpy
  * python-setuptools
  * python-gst0.10
  * gstreamer0.10-plugins-base,
  * gstreamer0.10-plugins-fluendo-mp3
  * gstreamer0.10-plugins-good


Provides
==========

 * SoundManager 2 >= 2.91 (http://www.schillmania.com/projects/soundmanager2)
 * jQuery => 1.2.6 (http://www.jquery.com)
 * jsGraphics => 3.03 (http://www.walterzorn.com/jsgraphics/jsgraphics_e.htm)


High level process example
===========================

For example::

 >>> import timeside
 >>> decoder  =  timeside.decoder.FileDecoder('source.wav')
 >>> grapher  =  timeside.grapher.Waveform()
 >>> analyzer =  timeside.analyzer.MaxLevel()
 >>> encoder  =  timeside.encoder.Mp3Encoder('output.mp3')
 >>> (decoder | grapher | analyzer | encoder).run()
 >>> grapher.render(output='image.png')
 >>> print 'Level:', analyzer.result()


UI Integration
===============

See TimeSide UI integration guide: http://code.google.com/p/timeside/wiki/UiGuide


More examples
==============

 * http://code.google.com/p/timeside/
 * http://archives.crem-cnrs.fr/items/CNRSMH_I_1956_002_001_01/
 * http://demo.telemeta.org (login: demo , pass: demo)


Related projects
=================

Telemeta : open web audio CMS (http://telemeta.org)


Copyrights
==========

Copyright (c) 2006, 2011 Parisson SARL. All rights reserved.
Copyright (c) 2006, 2010 Samalyse SARL.
Copyright (c) 2010, 2012, Paul Brossier.


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


Contact and Informations
========================

See http://code.google.com/p/timeside/
