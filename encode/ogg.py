# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2009 Guillaume Pellerin <yomguy@parisson.com>

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

# Author: Guillaume Pellerin <yomguy@parisson.com>

import os
import string
import subprocess

from timeside.encode.core import *
from timeside.encode.api import IEncoder

class OggVorbisEncoder(EncoderCore):
    """Defines methods to encode to OGG Vorbis"""

    implements(IEncoder)

    def __init__(self):
        self.description = self.description()
        self.format = self.format()
        self.mime_type = self.mime_type()
        self.bitrate_default = '192'
        self.dub2args_dict = {'creator': 'artist',
                             'relation': 'album'
                             }

    def format(self):
        return 'OggVorbis'

    def file_extension(self):
        return 'ogg'

    def mime_type(self):
        return 'application/ogg'

    def description(self):
        return """
        Vorbis is a free software / open source project headed by the Xiph.Org Foundation (formerly Xiphophorus company). The project produces an audio format specification and software implementation (codec) for lossy audio compression. Vorbis is most commonly used in conjunction with the Ogg container format and it is therefore often referred to as Ogg Vorbis. (source Wikipedia)
        """

    def get_file_info(self, file):
        try:
            file_out1, file_out2 = os.popen4('ogginfo "' + file + '"')
            info = []
            for line in file_out2.readlines():
                info.append(clean_word(line[:-1]))
            self.info = info
            return self.info
        except:
            raise IOError('EncoderError: file does not exist.')

    def write_tags(self, file):
        from mutagen.oggvorbis import OggVorbis
        media = OggVorbis(file)
        for tag in self.metadata.keys():
            media[tag] = str(self.metadata[tag])
        media.save()

    def get_args(self):
        """Get process options and return arguments for the encoder"""
        args = []
        if not self.options is None:
            if not ('verbose' in self.options and self.options['verbose'] != '0'):
                args.append('-Q ')
            if 'ogg_bitrate' in self.options:
                args.append('-b '+self.options['ogg_bitrate'])
            elif 'ogg_quality' in self.options:
                args.append('-q '+self.options['ogg_quality'])
            else:
                args.append('-b '+self.bitrate_default)
        else:
            args.append('-Q -b '+self.bitrate_default)

        for tag in self.metadata:
            name = tag[0]
            value = clean_word(tag[1])
            args.append('-c %s="%s"' % (name, value))
            if name in self.dub2args_dict.keys():
                arg = self.dub2args_dict[name]
                args.append('-c %s="%s"' % (arg, value))
        return args

    def process(self, source, metadata, options=None):
        self.metadata = metadata
        self.options = options
        args = self.get_args(options)
        args = ' '.join(args)
        command = 'oggenc %s -' % args

        stream = self.core_process(command, source)
        for __chunk in stream:
            yield __chunk


