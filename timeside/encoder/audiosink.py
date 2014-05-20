# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2014 Guillaume Pellerin <yomguy@parisson.com>
# Copyright (c) 2013-2014 Thomas Fillon <thomas.fillon@parisson.com>

# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

# Author: Thomas Fillon <thomas.fillon@parisson.com>

from timeside.core import implements, interfacedoc
from timeside.encoder.core import GstEncoder
from timeside.api import IEncoder


class AudioSink(GstEncoder):

    """gstreamer-based Audio Sink

    This encoder plays the decoded audio stream to the sound card


    >>> import timeside
    >>> wav_file = 'tests/samples/guitar.wav' # doctest: +SKIP
    >>> d = timeside.decoder.file.FileDecoder(wav_file)
    >>> e = timeside.encoder.audiosink.AudioSink()
    >>> (d|e).run() # doctest: +SKIP
    """

    implements(IEncoder)

    def __init__(self, output_sink='autoaudiosink'):

        super(GstEncoder, self).__init__()
        self.streaming = False

        self.output_sink = output_sink

        import threading
        self.end_cond = threading.Condition(threading.Lock())

        self.eod = False
        self.metadata = None
        self.num_samples = 0

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None,
              totalframes=None):
        super(AudioSink, self).setup(channels, samplerate, blocksize,
                                     totalframes)

        self.pipe = ''' appsrc name=src ! audioconvert
                        ! %s ''' % self.output_sink

        self.start_pipeline(channels, samplerate)

    @staticmethod
    @interfacedoc
    def id():
        return "gst_audio_sink_enc"

    @staticmethod
    @interfacedoc
    def description():
        return "GStreamer based audio sink encoder"

    @staticmethod
    @interfacedoc
    def format():
        return ""

    @staticmethod
    @interfacedoc
    def file_extension():
        return ""

    @staticmethod
    @interfacedoc
    def mime_type():
        return 'audio/x-raw'

    @interfacedoc
    def set_metadata(self, metadata):
        self.metadata = metadata


# Define global variables for use with doctest
DOCTEST_ALIAS = {'wav_file':
                 'https://github.com/yomguy/timeside-samples/raw/master/samples/guitar.wav'}

if __name__ == "__main__":
    import doctest

    doctest.testmod(extraglobs=DOCTEST_ALIAS)
