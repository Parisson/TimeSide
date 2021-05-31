# -*- coding: utf-8 -*-

""" decoder plugin based on aubio """

from timeside.core.decoder import Decoder, IDecoder, implements, interfacedoc
from timeside.plugins.decoder.utils import get_sha1, get_media_uri_info
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
        try:
            self.source = aubio.source(self.uri, hop_size=self.output_blocksize)
        except RuntimeError as e:
            raise IOError(e)
        self.input_samplerate = self.source.samplerate
        self.input_channels = self.source.channels

        # get the original file duration
        self.input_totalframes = self.source.duration
        self.input_duration = self.input_totalframes / self.input_samplerate
        self.uri_duration = self.input_duration

        self.start = start
        self.duration = duration

        # FIXME
        self.mimetype = mimetypes.guess_type(uri)[0]
        self.input_width = 8

        if sha1 is not None:
            self._sha1 = sha1
        else:
            self._sha1 = get_sha1(uri)

    def setup(self, channels=None, samplerate=None, blocksize=None):
        if self.start or self.duration:
            if self.start > self.uri_duration:
                raise ValueError ('Segment start time exceeds media duration')
            if self.duration is None:
                self.duration = self.uri_duration - self.start
            if self.start + self.duration > self.uri_duration:
                raise ValueError ('Segment duration exceeds media duration')

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
        self.output_samplerate = self.source.samplerate

        self.frames_read = 0
        self.start_frame = int(self.start * self.output_samplerate)
        if self.duration:
            seconds_to_read = self.duration
            self.frames_to_read = int (seconds_to_read * self.output_samplerate)

        if self.duration:
            self.input_duration = self.duration
            self.input_totalframes = self.frames_to_read

        if self.start > 0:
            self.source.seek(self.start_frame)

    @staticmethod
    @interfacedoc
    def id():
        return "aubio_decoder"

    @staticmethod
    @interfacedoc
    def version():
        return "1.0"

    @interfacedoc
    def process(
        self,
        task=None,
        experience=None,
        item=None,
        sample_cursor=None
    ):
        frames, read = self.source.do_multi()
        self.eod = (read < self.output_blocksize)
        if self.duration and self.frames_read + read >= self.frames_to_read:
            extra_read = self.frames_read + read - self.frames_to_read
            read = self.source.hop_size - extra_read
            self.eod = True
        self.frames_read += read
        frames = frames[:, :read].T
        super(AubioDecoder, self).process(
            frames.copy(),
            self.eod,
            task=task,
            experience=experience,
            item=item,
            sample_cursor=sample_cursor
        )
        return frames.copy(), self.eod

    @interfacedoc
    def mime_type(self):
        return self.mimetype

    @interfacedoc
    def resolution(self):
        return 0

    @interfacedoc
    def metadata(self):
        return {}

    @interfacedoc
    def totalframes(self):
        if self.input_samplerate == self.output_samplerate:
            return self.input_totalframes
        else:
            ratio = self.output_samplerate / self.input_samplerate
            return int(self.input_totalframes * ratio)
