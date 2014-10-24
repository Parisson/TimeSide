Processors
==========

IEncoder
--------

   * **live_encoder** : Gstreamer-based Audio Sink
   * **flac_encoder** : FLAC encoder based on Gstreamer
   * **aac_encoder** : AAC encoder based on Gstreamer
   * **mp3_encoder** : MP3 encoder based on Gstreamer
   * **vorbis_encoder** : OGG Vorbis encoder based on Gstreamer
   * **opus_encoder** : Opus encoder based on Gstreamer
   * **wav_encoder** : WAV encoder based on Gstreamer
   * **webm_encoder** : WebM encoder based on Gstreamer

IDecoder
--------

   * **array_decoder** : Decoder taking Numpy array as input
   * **file_decoder** : File Decoder based on Gstreamer
   * **live_decoder** : Live source Decoder based on Gstreamer

IGrapher
--------

   * **grapher_aubio_pitch** : Image representing Aubio Pitch
   * **grapher_onset_detection_function** : Image representing Onset detection function
   * **grapher_waveform** : Image representing Waveform from Analyzer
   * **grapher_irit_speech_4hz_segments** : Image representing Irit 4Hz Speech Segmentation
   * **grapher_irit_speech_4hz_segments_median** : Image representing Irit 4Hz Speech Segmentation with median filter
   * **grapher_monopoly_segments** : Image representing Irit Monopoly Segmentation
   * **grapher_limsi_sad_etape** : Image representing LIMSI SAD with ETAPE model
   * **grapher_limsi_sad_maya** : Image representing LIMSI SAD with Mayan model
   * **grapher_irit_startseg** : Image representing IRIT Start Noise
   * **spectrogram_log** : Logarithmic scaled spectrogram (level vs. frequency vs. time).
   * **spectrogram_lin** : Linear scaled spectrogram (level vs. frequency vs. time).
   * **waveform_simple** : Simple monochrome waveform image.
   * **waveform_centroid** : Waveform where peaks are colored relatively to the spectral centroids of each frame buffer.
   * **waveform_contour_black** : Black amplitude contour waveform.
   * **waveform_contour_white** : an white amplitude contour wavform.
   * **waveform_transparent** : Transparent waveform.

IAnalyzer
---------

   * **mean_dc_shift** : Mean DC shift analyzer
   * **level** : Audio level analyzer
   * **aubio_melenergy** : Aubio Mel Energy analyzer
   * **aubio_mfcc** : Aubio MFCC analyzer
   * **aubio_pitch** : Aubio Pitch estimation analyzer
   * **aubio_specdesc** : Aubio Spectral Descriptors collection analyzer
   * **aubio_temporal** : Aubio Temporal analyzer
   * **yaafe** : Yaafe feature extraction library interface analyzer
   * **irit_monopoly** : Segmentor Monophony/Polyphony based on the analysis of yin confidence.
   * **irit_startseg** : Segmentation of recording sessions into 'start' and 'session' segments
   * **irit_speech_4hz** : Speech Segmentor based on the 4Hz energy modulation analysis.
   * **irit_speech_entropy** : Speech Segmentor based on Entropy analysis.
   * **limsi_sad** : Limsi Speech Activity Detection Systems
   * **spectrogram_analyzer** : Spectrogram image builder with an extensible buffer based on tables
   * **onset_detection_function** : Onset Detection Function analyzer
   * **spectrogram_analyzer_buffer** : Spectrogram image builder with an extensible buffer based on tables
   * **waveform_analyzer** : Waveform analyzer

IEffect
-------

   * **fx_gain** : Gain effect processor

