# -*- coding: utf-8 -*-

""" decoder plugin based on aubio """

from timeside.core.decoder import Decoder, IDecoder, implements, interfacedoc
from timeside.plugins.decoder.utils import get_sha1, get_media_uri_info
import aubio
import mimetypes
import numpy as np


class NullDecoder(Decoder):
    """ File decoder based on aubio """
    implements(IDecoder)

    output_blocksize = 1

    @staticmethod
    @interfacedoc
    def id():
        return "null_decoder"

    @staticmethod
    @interfacedoc
    def version():
        return "1.0"

    @interfacedoc
    def process(self):
        return np.zeros(self.output_blocksize), True

