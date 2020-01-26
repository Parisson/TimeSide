from timeside.core import implements, interfacedoc
from timeside.core.aubio_encoder import AubioEncoder
from timeside.core.api import IEncoder

class VorbisEncoder(AubioEncoder):

    """OGG Vorbis encoder based on aubio"""

    implements(IEncoder)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None,
              totalframes=None):
        super(VorbisEncoder, self).setup(
            channels, samplerate, blocksize, totalframes)

    @staticmethod
    @interfacedoc
    def id():
        return "vorbis_aubio_encoder"

    @staticmethod
    @interfacedoc
    def format():
        return "OGG"

    @staticmethod
    @interfacedoc
    def version():
        return "1.0"

    @staticmethod
    @interfacedoc
    def file_extension():
        return "ogg"

    @staticmethod
    @interfacedoc
    def mime_type():
        return 'audio/ogg'
