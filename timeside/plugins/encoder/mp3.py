# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2014 Parisson SARL
# Copyright (c) 2006-2014 Guillaume Pellerin <pellerin@parisson.com>
# Copyright (c) 2010-2014 Paul Brossier <piem@piem.org>
# Copyright (c) 2009-2010 Olivier Guilyardi <olivier@samalyse.com>
# Copyright (c) 2013-2014 Thomas Fillon <thomas@parisson.com>

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

# Authors: Guillaume Pellerin <yomguy@parisson.com>
#          Paul Brossier <piem@piem.org>
#          Thomas Fillon <thomas@parisson.com>

from timeside.core import implements, interfacedoc
from timeside.core.encoder import GstEncoder
from timeside.core.api import IEncoder


class Mp3Encoder(GstEncoder):

    """MP3 encoder based on Gstreamer"""

    implements(IEncoder)

    def __init__(self, output, streaming=False, overwrite=False, target="quality", target_value=2, cbr=False):
        super(Mp3Encoder, self).__init__(output, streaming=streaming, overwrite=overwrite)
        self.target = target
        self.target_value = target_value
        self.cbr = cbr

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None,
              totalframes=None):
        super(Mp3Encoder, self).setup(channels, samplerate, blocksize,
                                      totalframes)

        # http://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-ugly-plugins/html/gst-plugins-ugly-plugins-lamemp3enc.html#GstLameMP3Enc--cbr
        # cbr only makes sense when target is equal to `bitrate`
        str_cbr = ' cbr=%s' % self.cbr if self.target == 'bitrate' else ''
        self.pipe = '''appsrc name=src
                  ! audioconvert ! audioresample
                  ! lamemp3enc target=%(target)s %(target)s=%(target_value)d%(str_cbr)s encoding-engine-quality=standard
                  ! xingmux
                  ! id3v2mux
                  ''' % {'target': self.target, 'target_value': self.target_value, 'str_cbr': str_cbr}

        if self.filename and self.streaming:
            self.pipe += ''' ! tee name=t
            ! queue ! filesink location=%s
            t. ! queue! appsink name=app sync=False
            ''' % self.filename

        elif self.filename:
            self.pipe += '! filesink location=%s async=False sync=False ' % self.filename
        else:
            self.pipe += '! queue ! appsink name=app sync=False'

        self.start_pipeline(channels, samplerate)

    @staticmethod
    @interfacedoc
    def id():
        return "mp3_encoder"

    @staticmethod
    @interfacedoc
    def format():
        return "MP3"

    @staticmethod
    @interfacedoc
    def file_extension():
        return "mp3"

    @staticmethod
    @interfacedoc
    def mime_type():
        return "audio/mpeg"

    def write_metadata(self):
        """Write all ID3v2.4 tags to file from self.metadata"""
        import mutagen
        from mutagen import id3

        id3 = id3.ID3(self.filename)
        for tag in self.metadata.keys():
            value = self.metadata[tag]
            frame = mutagen.id3.Frames[tag](3, value)
            try:
                id3.add(frame)
            except:
                raise IOError('EncoderError: cannot tag "' + tag + '"')
        try:
            id3.save()
        except:
            raise IOError('EncoderError: cannot write tags')
