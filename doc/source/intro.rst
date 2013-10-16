==============================================
TimeSide : open web audio processing framework
==============================================

.. image:: https://secure.travis-ci.org/yomguy/TimeSide.png?branch=master
    :target: http://travis-ci.org/yomguy/TimeSide/

TimeSide is a set of python components enabling audio analysis, imaging, transcoding and streaming. Its high-level API has been designed to enable complex processing on big media data corpus. Its simple plugin architecture can be adapted to various usecases.

It also includes a smart HTML5 interactive user interface embeddable in any web application to provide various media format playback, on the fly transcoding and streaming, fancy waveforms and spectrograms, various low and high level audio analyzers, semantic labelling and segmentation.


Goals
=====

We just **need** a python library to:

* **Do** asynchronous and fast audio processing with Python,
* **Decode** audio frames from ANY format into numpy arrays,
* **Analyze** audio content with some state-of-the-art audio feature extraction libraries,
* **Organize**, serialize and save analysis metadata through various formats,
* **Draw** various fancy waveforms, spectrograms and other cool graphers,
* **Transcode** audio data in various media formats and stream them through web apps,
* **Playback** and **interact** **on demand** through a smart high-level HTML5 extensible player,
* **Index**, **tag** and **organize semantic metadata** (see `Telemeta <http://telemeta.org>`_ which embed TimeSide).

Here is a schematic diagram of the TimeSide engine architecture:

.. image:: http://timeside.googlecode.com/git/doc/img/timeside_schema.png


Available plugins
=================

* Decoder:
     - Takes ALL known media formats thanks to GStreamer

* Analyzers:
     - Levels : max level, mean level, DC
     - Yaafe : all data flows
     - Aubio : BPM, beats, pitch, various spectral descriptors
     - VAMP : all default plugins from simple host
     - IRIT : 4Hz modulation and entropy speech detectors

* Graphers:
     - Waveform
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

