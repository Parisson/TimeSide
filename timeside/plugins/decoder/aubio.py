# -*- coding: utf-8 -*-

""" decoder plugin based on aubio """

from timeside.core.decoder import Decoder, IDecoder, implements, interfacedoc
from timeside.plugins.decoder.utils import get_sha1
import aubio
import mimetypes

class AubioDecoder(Decoder):
    """ File decoder based on aubio """
    implements(IDecoder)

    output_blocksize = 8 * 1024

    def __init__(self, uri, start=0, duration=None, sha1=None):
        super().__init__(start=start, duration=duration)
        self.uri = uri

        # create the source with default settings
        self.source = aubio.source(self.uri, hop_size=self.output_blocksize)
        self.input_samplerate = self.source.samplerate
        self.input_channels = self.source.channels

        # get the original file duration
        self.input_totalframes = self.source.duration
        self.input_duration = self.input_totalframes / self.input_samplerate
        self.uri_duration = self.input_duration

        # FIXME
        self.mimetype = mimetypes.guess_type(uri)[0]
        self.input_width = 8

        if sha1 is not None:
            self._sha1 = sha1
        else:
            self._sha1 = get_sha1(uri)

    def setup(self, channels=None, samplerate=None, blocksize=None):
        kwargs = {}
        if channels is not None:
            kwargs.update ({'channels': channels})
        if samplerate is not None:
            kwargs.update ({'samplerate': samplerate})
        if blocksize is not None and blocksize != self.source.hop_size:
            kwargs.update ({'hop_size': blocksize})
        if len(kwargs):
            self.source = aubio.source(self.uri, **kwargs)

        self.output_blocksize = self.source.hop_size
        self.output_channels = self.source.channels
        self.output_samplerate  = self.source.samplerate

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_decoder"

    @staticmethod
    @interfacedoc
    def version():
        return "1.0"

    @interfacedoc
    def process(self):
        frames, read = self.source.do_multi()
        self.eod = (read < self.output_blocksize)
        frames = frames[:, :read].T
        return frames, self.eod

    @interfacedoc
    def mime_type(self):
        return self.mimetype

    @interfacedoc
    def resolution(self):
        return 0

    @interfacedoc
    def metadata(self):
        return {}
