from timeside.core import implements, interfacedoc
from timeside.core.aubio_encoder import AubioEncoder
from timeside.core.api import IEncoder

class WavEncoder(AubioEncoder):

    """Wav encoder based on aubio"""

    implements(IEncoder)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None,
              totalframes=None):
        super(WavEncoder, self).setup(
            channels, samplerate, blocksize, totalframes)

    @staticmethod
    @interfacedoc
    def id():
        return "wav_aubio_encoder"

    @staticmethod
    @interfacedoc
    def format():
        return "WAV"

    @staticmethod
    @interfacedoc
    def version():
        return "1.0"

    @staticmethod
    @interfacedoc
    def file_extension():
        return "wav"

    @staticmethod
    @interfacedoc
    def mime_type():
        return 'audio/x-wav'
