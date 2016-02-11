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


class VorbisEncoder(GstEncoder):

    """OGG Vorbis encoder based on Gstreamer"""

    implements(IEncoder)

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None,
              totalframes=None):
        super(VorbisEncoder, self).setup(
            channels, samplerate, blocksize, totalframes)
        self.pipe = ''' appsrc name=src
                  ! audioconvert ! audioresample
                  ! vorbisenc quality=0.9
                  ! oggmux
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
        return "vorbis_encoder"

    @staticmethod
    @interfacedoc
    def format():
        return "OGG"

    @staticmethod
    @interfacedoc
    def file_extension():
        return "ogg"

    @staticmethod
    @interfacedoc
    def mime_type():
        return "application/ogg"

    @interfacedoc
    def set_metadata(self, metadata):
        self.metadata = metadata
