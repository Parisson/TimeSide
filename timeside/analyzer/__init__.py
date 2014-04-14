# -*- coding: utf-8 -*-

# ----- Load external libraries ------
# Aubio
try:
    WITH_AUBIO = True
    from aubio_temporal import AubioTemporal
    from aubio_pitch import AubioPitch
    from aubio_mfcc import *
    from aubio_melenergy import *
    from aubio_specdesc import *
except ImportError:
    WITH_AUBIO = False

# Yaafe
try:
    WITH_YAAFE = True
    from yaafe import *

except ImportError:
    WITH_YAAFE = False

# Vamp Plugins
try:
    from vamp_plugin import VampSimpleHost
    VampSimpleHost.SimpleHostProcess(['-v'])
    WITH_VAMP = True
except OSError:
    WITH_VAMP = False


# ----- Load timeside analyzers ------
from level import Level
from dc import MeanDCShift
from spectrogram import Spectrogram
from waveform import Waveform
from irit_speech_entropy import IRITSpeechEntropy
from irit_speech_4hz import IRITSpeech4Hz
from odf import OnsetDetectionFunction
if WITH_YAAFE:
    from limsi_sad import LimsiSad
