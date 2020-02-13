from timeside.core import implements, interfacedoc
from timeside.core.aubio_encoder import AubioEncoder
from timeside.core.api import IEncoder

class FlacEncoder(AubioEncoder):

    """FLAC encoder based on aubio"""

    implements(IEncoder)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None,
              totalframes=None):
        super(FlacEncoder, self).setup(
            channels, samplerate, blocksize, totalframes)

    @staticmethod
    @interfacedoc
    def id():
        return "flac_aubio_encoder"

    @staticmethod
    @interfacedoc
    def format():
        return "FLAC"

    @staticmethod
    @interfacedoc
    def version():
        return "1.0"

    @staticmethod
    @interfacedoc
    def file_extension():
        return "flac"

    @staticmethod
    @interfacedoc
    def mime_type():
        return 'audio/flac'
