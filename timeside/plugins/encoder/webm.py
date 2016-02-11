# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Paul Brossier <piem@piem.org>
# Copyright (c) 2010 Guillaume Pellerin <yomguy@parisson.com>

# This file is part of TimeSide.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from timeside.core import implements, interfacedoc
from timeside.core.encoder import GstEncoder
from timeside.core.api import IEncoder


class WebMEncoder(GstEncoder):

    """WebM encoder based on Gstreamer"""

    implements(IEncoder)

    def __init__(self, output, streaming=False, overwrite=False, video=False):
        super(WebMEncoder, self).__init__(output, streaming, overwrite)
        self.video = video

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None,
              totalframes=None):
        super(WebMEncoder, self).setup(channels, samplerate, blocksize,
                                       totalframes)
        from numpy import ceil
        framerate = 30
        num_buffers = ceil(self.mediainfo()['duration'] *
                           framerate).astype(int)
        self.pipe = ''
        if self.video:
            self.pipe += '''videotestsrc pattern=black num_buffers=%d ! ffmpegcolorspace ! queue ! vp8enc speed=2 threads=4 quality=9.0 ! queue ! mux.
                         ''' % num_buffers
        self.pipe += '''
              appsrc name=src ! queue ! audioconvert ! vorbisenc quality=0.9 ! queue ! mux.
              webmmux streamable=true name=mux
                  '''
        if self.filename and self.streaming:
            self.pipe += ''' ! tee name=t
            ! queue ! filesink location=%s
            t. ! queue ! appsink name=app sync=False
            ''' % self.filename

        elif self.filename:
            self.pipe += '! filesink location=%s async=False sync=False ' % self.filename
        else:
            self.pipe += '! queue ! appsink name=app sync=False '

        self.start_pipeline(channels, samplerate)

    @staticmethod
    @interfacedoc
    def id():
        return "webm_encoder"

    @staticmethod
    @interfacedoc
    def format():
        return "WebM"

    @staticmethod
    @interfacedoc
    def file_extension():
        return "webm"

    @staticmethod
    @interfacedoc
    def mime_type():
        return "video/webm"

    @interfacedoc
    def set_metadata(self, metadata):
        self.metadata = metadata

if __name__ == "__main__":
    import doctest
    doctest.testmod()
