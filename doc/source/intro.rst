==============================================
TimeSide : open web audio processing framework
==============================================

.. image:: https://secure.travis-ci.org/yomguy/TimeSide.png?branch=master
    :target: https://travis-ci.org/yomguy/TimeSide/

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

.. image:: https://raw.github.com/yomguy/TimeSide/master/doc/slides/img/timeside_schema.png


Processors
==========

IEncoder
---------

  * VorbisEncoder [gst_vorbis_enc]
  * WavEncoder [gst_wav_enc]
  * Mp3Encoder [gst_mp3_enc]
  * FlacEncoder [gst_flac_enc]
  * AacEncoder [gst_aac_enc]
  * WebMEncoder [gst_webm_enc]

IDecoder
---------

  * FileDecoder [gst_dec]
  * ArrayDecoder [array_dec]

IGrapher
---------

  * Waveform [waveform_simple]
  * WaveformCentroid [waveform_centroid]
  * WaveformTransparent [waveform_transparent]
  * WaveformContourBlack [waveform_contour_black]
  * WaveformContourWhite [waveform_contour_white]
  * SpectrogramLog [spectrogram_log]
  * SpectrogramLinear [spectrogram_linear]

IAnalyzer
---------

  * Level [level]
  * MeanDCShift [mean_dc_shift]
  * AubioTemporal [aubio_temporal]
  * AubioPitch [aubio_pitch]
  * AubioMfcc [aubio_mfcc]
  * AubioMelEnergy [aubio_melenergy]
  * AubioSpecdesc [aubio_specdesc]
  * Yaafe [yaafe]
  * Spectrogram [spectrogram_analyzer]
  * Waveform [waveform_analyzer]
  * VampSimpleHost [vamp_simple_host]
  * IRITSpeechEntropy [irit_speech_entropy]
  * IRITSpeech4Hz [irit_speech_4hz]
  * OnsetDetectionFunction [odf]

