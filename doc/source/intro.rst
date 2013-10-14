==============
 Introduction
==============

TimeSide is a set of python components enabling audio analysis, imaging, transcoding and streaming. Its high-level API has been designed to enable complex processing on big media data corpus. Its simple plugin architecture can be adapted to various usecases.

It also includes a smart HTML5 interactive user interface embeddable in any web application to provide various media format playback, on the fly transcoding and streaming, fancy waveforms and spectrograms, various low and high level audio analyzers, semantic labelling and segmentation.


Goals
=====

We just *need* a python library to:

 * Do asynchronous and fast audio processing with Python,
 * Decode audio frames from ANY format into numpy arrays,
 * Analyze audio content with some state-of-the-art audio feature extraction libraries,
 * Organize, serialize and save analysis metadata through various formats,
 * Draw various fancy waveforms, spectrograms and other cool graphers,
 * Transcode audio data in various media formats and stream them through web apps,
 * Playback and interact *on demand* through a smart high-level HTML5 extensible player,
 * Index, tag and organize semantic metadata (see `Telemeta <http://telemeta.org>`_ which embed TimeSide).

Here is a schematic diagram of the TimeSide engine architecture:

.. image:: http://timeside.googlecode.com/git/doc/img/timeside_schema.png


Available plugins
=================

 * Decoder:
     - ALL known media formats thanks to Gstreamer

 * Analyzers:
     - MaxLevel, MeanLevel
     - DC
     - any Yaafe data flow
     - Aubio BPM, Beats, MFCC, ...

 * Graphers:
     - WaveForm
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
