==================================================
TimeSide : audio processing framework for the web
==================================================

|version| |downloads| |travis_master| |coveralls_master|

.. |travis_master| image:: https://travis-ci.org/Parisson/TimeSide.svg
    :target: https://travis-ci.org/Parisson/TimeSide/

.. |coveralls_master| image:: https://coveralls.io/repos/Parisson/TimeSide/badge.png?branch=master
  :target: https://coveralls.io/r/Parisson/TimeSide?branch=master

.. |version| image:: https://img.shields.io/pypi/v/timeside.svg
   :target: https://pypi.python.org/pypi/TimeSide/
   :alt: Version

.. |downloads| image:: https://img.shields.io/pypi/dm/timeside.svg
   :target: https://pypi.python.org/pypi/TimeSide/
   :alt: Downloads


TimeSide is a python framework enabling low and high level audio analysis, imaging, transcoding, streaming and labelling. Its high-level API is designed to enable complex processing on very large datasets of any audio or video assets with a plug-in architecture, a secure scalable backend and an extensible dynamic web frontend.


Use cases
==========

* Scaled audio computing (filtering, machine learning, etc)
* Web audio visualization
* Audio process prototyping
* Realtime and on-demand transcoding and streaming over the web
* Automatic segmentation and labelling synchronized with audio events


Goals
=====

* **Do** asynchronous and fast audio processing with Python,
* **Decode** audio frames from **any** audio or video media format into numpy arrays,
* **Analyze** audio content with some state-of-the-art audio feature extraction libraries like Aubio, Yaafe and VAMP as well as some pure python processors
* **Visualize** sounds with various fancy waveforms, spectrograms and other cool graphers,
* **Transcode** audio data in various media formats and stream them through web apps,
* **Serialize** feature analysis data through various portable formats,
* **Playback** and **interact** **on demand** through a smart high-level HTML5 extensible player,
* **Index**, **tag** and **annotate** audio archives with semantic metadata (see `Telemeta <http://telemeta.org>`__ which embed TimeSide).
* **Deploy** and **scale** your own audio processing engine through any infrastructure


Funding and support
===================

To fund the project and continue our fast development process, we need your explicit support. So if you use TimeSide in production or even in development, please let us know:

* star or fork the project on `GitHub <https://github.com/Parisson/TimeSide>`_
* tweet something to `@parisson_studio <https://twitter.com/parisson_studio>`_ or `@yomguy <https://twitter.com/omguy>`_
* drop us an email <support@parisson.com>

Thanks for your help!
