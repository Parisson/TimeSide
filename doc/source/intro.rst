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

  * FileDecoder [file_decoder]
  * ArrayDecoder [array_decoder]
  * LiveDecoder [live_decoder]

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
  *  OnsetDetectionFunction [onset_detection_function]
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
  *  Display.onset_detection_function [grapher_odf]
  *  Display.waveform_analyzer [grapher_waveform]
  *  Display.irit_speech_4hz.segments [grapher_irit_speech_4hz_segments]

IEncoder
---------

  * VorbisEncoder [vorbis_encoder]
  * WavEncoder [wav_encoder]
  * Mp3Encoder [mp3_encoder]
  * FlacEncoder [flac_encoder]
  * AacEncoder [aac_encoder]
  * WebMEncoder [webm_encoder]
  * OpusEncoder [opus_encoder]
  * AudioSink [live_encoder]

