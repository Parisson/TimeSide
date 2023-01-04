===========================================================================
TimeSide : scalable audio processing framework and server written in Python
===========================================================================

TimeSide is a Python framework enabling low and high level audio analysis, imaging, transcoding, streaming and labelling. Its high-level API is designed to enable complex processing on very large datasets of any audio or video assets with a plug-in architecture and a secured scalable backend.


Introduction
=============

As the number of online audio applications and datasets increase, it becomes crucial for researchers and engineers to be able to prototype and test their own algorithms as fast as possible on various platforms and usecases like computational musicology and streaming services. On the other side, content providers and producers need to enhance user experiences on their platforms with more metadata based on cultural history but also audio feature analyses. Growing those metadata synchronously with the music published on the internet implies that the analysis and storage systems can be easily updated, scaled and deployed.

TimeSide has been developed in this sense to propose an online audio processing service. It provides:

- a core module as a python audio processing library to work from a shell or any Python based program
- a web server with a RESTful API on top of the core module so that web developers can then easily embed the remote processing service into their own applications.

A Javascript SDK based on OpenAPI is also available to easily connect to the server API.

Use cases
==========

- Scaled audio computing (filtering, machine learning, etc)
- Web audio visualization
- Audio process prototyping
- Realtime and on-demand transcoding and streaming over the web
- Automatic segmentation and labelling synchronized with audio events


Goals
=====

- **Do** asynchronous and fast audio processing with Python,
- **Decode** audio frames from **any** audio or video media format into numpy arrays,
- **Analyze** audio content with some state-of-the-art audio feature extraction libraries like Aubio, Yaafe and VAMP as well as some pure python processors
- **Visualize** sounds with various fancy waveforms, spectrograms and other cool graphers,
- **Transcode** audio data in various media formats and stream them through web apps,
- **Serialize** feature analysis data through various portable formats,
- **Provide** audio sources from plateform like YouTube or Deezer
- **Deliver** analysis and transcode on provided or uploaded tracks over the web through a REST API
- **Playback** and **interact** **on demand** through a smart high-level HTML5 extensible player,
- **Index**, **tag** and **annotate** audio archives with semantic metadata (see `Telemeta <http://telemeta.org>`__ which embed TimeSide).
- **Deploy** and **scale** your own audio processing engine through any infrastructure


Funding and support
===================

To fund the project and continue our fast development process, we need your explicit support. So if you use TimeSide in production or even in a development or experimental setup, please let us know by:

- staring or forking the project on `GitHub <https://github.com/Parisson/TimeSide>`_
- droping us an email at <wam@ircam.fr>

Thanks for your help and support!
