List of available processors
============================

Encoder
--------
* **flac_aubio_encoder** **1.0**: FLAC encoder based on aubio
* **vorbis_aubio_encoder** **1.0**: OGG Vorbis encoder based on aubio
* **wav_aubio_encoder** **1.0**: Wav encoder based on aubio
* **live_encoder** **1.0**: Gstreamer-based Audio Sink
* **flac_encoder** **1.0**: FLAC encoder based on Gstreamer
* **aac_encoder** **1.0**: AAC encoder based on Gstreamer
* **mp3_encoder** **1.0**: MP3 encoder based on Gstreamer
* **vorbis_encoder** **1.0**: OGG Vorbis encoder based on Gstreamer
* **opus_encoder** **1.0**: Opus encoder based on Gstreamer
* **wav_encoder** **1.0**: WAV encoder based on Gstreamer
* **webm_encoder** **1.0**: WebM encoder based on Gstreamer

Decoder
--------
* **array_decoder** **1.0**: Decoder taking Numpy array as input
* **aubio_decoder** **1.0**: File decoder based on aubio
* **file_decoder** **1.0**: File Decoder based on Gstreamer

Grapher
--------
* **grapher_aubio_pitch** **1.0**: Image representing Pitch
* **grapher_aubio_silence** **1.0**: Image representing Aubio Silence
* **grapher_dissonance** **1.0**: Image representing Dissonance
* **grapher_vamp_cqt** **1.0**: Image representing Constant Q Transform
* **grapher_loudness_itu** **1.0**: Image representing Loudness ITU
* **spectrogram** **1.0**: Image representing Linear Spectrogram
* **grapher_onset_detection_function** **1.0**: Image representing Onset detection
* **grapher_waveform** **1.0**: Image representing Waveform from Analyzer
* **spectrogram_log** **1.0**: Logarithmic scaled spectrogram (level vs. frequency vs. time).
* **spectrogram_lin** **1.0**: Linear scaled spectrogram (level vs. frequency vs. time).
* **waveform_simple** **1.0**: Simple monochrome waveform image.
* **waveform_centroid** **1.0**: Waveform where peaks are colored relatively to the spectral centroids of each frame buffer.
* **waveform_contour_black** **1.0**: Black amplitude contour waveform.
* **waveform_contour_white** **1.0**: an white amplitude contour wavform.
* **waveform_transparent** **1.0**: Transparent waveform.

Analyzer
---------
* **aubio_melenergy** **0.4.6**: Aubio Mel Energy analyzer
* **aubio_mfcc** **0.4.6**: Aubio MFCC analyzer
* **aubio_pitch** **0.4.6**: Aubio Pitch estimation analyzer
* **aubio_silence** **0.4.6**: Aubio Silence detection analyzer
* **aubio_specdesc** **0.4.6**: Aubio Spectral Descriptors collection analyzer
* **aubio_temporal** **0.4.6**: Aubio Temporal analyzer
* **essentia_dissonance** **2.1b5.dev416**: Dissonance from Essentia
* **vamp_constantq** **1.1.0**: Constant Q transform from QMUL vamp plugins
* **vamp_simple_host** **1.1.0**: Vamp plugins library interface analyzer
* **loudness_itu** **1.0**: Measure of audio loudness using standard ITU-R BS.1770-3
* **spectrogram_analyzer** **1.0**: Spectrogram image builder with an extensible buffer based on tables
* **onset_detection_function** **1.0**: Onset Detection Function analyzer
* **spectrogram_analyzer_buffer** **1.0**: Spectrogram image builder with an extensible buffer based on tables
* **waveform_analyzer** **1.0**: Waveform analyzer

ValueAnalyzer
--------------
* **mean_dc_shift** **1.0**: Mean DC shift analyzer
* **essentia_dissonance_value** **2.1b5.dev416**: Mean Dissonance Value from Essentia
* **vamp_tempo** **1.1.0**: Tempo from QMUL vamp plugins
* **vamp_tuning** **1.1.0**: Tuning from NNLS Chroma vamp plugins
* **level** **1.0**: Audio level analyzer

Effect
-------
* **fx_gain** **1.0**: Gain effect processor