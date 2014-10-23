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

    """Gstreamer-based Audio Sink

    This encoder plays the decoded audio stream to the sound card

    Parameters
    ----------
    output_sink : str, optional
        Gstreamer sink element
        Default to 'autoaudiosink'
        Possible values : 'autoaudiosink', 'alsasink', 'osssink'

    >>> import timeside
    >>> from timeside.core import get_processor
    >>> from timeside.tools.test_samples import samples
    >>> wav_file = samples['sine440Hz_mono_1s.wav']
    >>> d = get_processor('file_decoder')(wav_file)
    >>> e = get_processor('live_encoder')()
    >>> (d|e).run()
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
        return "live_encoder"

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


if __name__ == "__main__":
    import doctest
    import timeside
    doctest.testmod(timeside.decoder.live, verbose=True)
