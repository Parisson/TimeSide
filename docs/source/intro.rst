===========================================================================
TimeSide : scalable audio processing framework and server written in Python
===========================================================================

TimeSide is a python framework enabling low and high level audio analysis, imaging, transcoding, streaming and labelling. Its high-level API is designed to enable complex processing on very large datasets of any audio or video assets with a plug-in architecture, a secure scalable backend and an extensible dynamic web frontend.


Introduction
=============

As the number of online audio applications and datasets increase, it becomes crucial for researchers and engineers to be able to prototype and test their own algorithms as fast as possible on various platforms and usecases like computational musicology and streaming services. On the other side, content providers and producers need to enhance user experiences on their platforms with more metadata based on cultural history but also audio feature analyses. Growing those metadata synchronously with the music published on the internet implies that the analysis and storage systems can be easily updated, scaled and deployed.

TimeSide has been developed in this sense to propose an online audio processing service. It provides a REST API as well as a javascript SDK so that web developers can easily embed the service into their own applications without requesting to much local resources on the user side to compute audio features.

Use cases
==========

- Scaled audio computing (filtering, machine learning, etc)
- Web audio visualization
- Audio process prototyping
- Realtime and on-demand transcoding and streaming over the web
- Automatic segmentation and labelling synchronized with audio events


Goals
=====

- **Do*- asynchronous and fast audio processing with Python,
- **Decode*- audio frames from **any*- audio or video media format into numpy arrays,
- **Analyze*- audio content with some state-of-the-art audio feature extraction libraries like Aubio, Yaafe and VAMP as well as some pure python processors
- **Visualize*- sounds with various fancy waveforms, spectrograms and other cool graphers,
- **Transcode*- audio data in various media formats and stream them through web apps,
- **Serialize*- feature analysis data through various portable formats,
- **Provide*- audio sources from plateform like YouTube or Deezer
- **Deliver*- analysis and transcode on provided or uploaded tracks over the web through a REST API
- **Playback*- and **interact*- **on demand*- through a smart high-level HTML5 extensible player,
- **Index**, **tag*- and **annotate*- audio archives with semantic metadata (see `Telemeta <http://telemeta.org>`__ which embed TimeSide).
- **Deploy*- and **scale*- your own audio processing engine through any infrastructure


Funding and support
===================

To fund the project and continue our fast development process, we need your explicit support. So if you use TimeSide in production or even in a development or experimental setup, please let us know by:

- staring or forking the project on `GitHub <https://github.com/Parisson/TimeSide>`_
- tweeting something to `@parisson_studio <https://twitter.com/parisson_studio>`_ or `@telemeta <https://twitter.com/telemeta>`_
- drop us an email on <support@parisson.com> or <pow@ircam.fr>

Thanks for your help!
