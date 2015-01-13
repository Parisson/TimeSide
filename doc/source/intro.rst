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


