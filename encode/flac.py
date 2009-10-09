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
from tempfile import NamedTemporaryFile

class FlacEncoder(EncoderCore):
    """Defines methods to encode to FLAC"""

    implements(IEncoder)

    def __init__(self):
        self.quality_default = '-5'

    def format(self):
        return 'FLAC'

    def file_extension(self):
        return 'flac'

    def mime_type(self):
        return 'application/flac'

    def description(self):
        return """
        Free Lossless Audio Codec (FLAC) is a file format for lossless audio
        data compression. During compression, FLAC does not lose quality from
        the audio stream, as lossy compression formats such as MP3, AAC, and
        Vorbis do. Josh Coalson is the primary author of FLAC.
        (source Wikipedia)
        """

    def get_file_info(self):
        try:
            file1, file2 = os.popen4('metaflac --list "'+self.dest+'"')
            info = []
            for line in file2.readlines():
                info.append(clean_word(line[:-1]))
            self.info = info
            return self.info
        except:
            raise IOError('EncoderError: metaflac is not installed or ' + \
                           'file does not exist.')

    def write_tags(self, file):
        from mutagen.flac import FLAC
        media = FLAC(file)
        for tag in self.metadata:
            name = tag[0]
            value = clean_word(tag[1])
            if name == 'COMMENT':
                media['DESCRIPTION'] = unicode(value)
            else:
                media[name] = unicode(value)
        try:
            media.save()
        except:
            raise IOError('EncoderError: cannot write tags.')

    def get_args(self,options=None):
        """Get process options and return arguments for the encoder"""
        args = []
        if not options is None:
            self.options = options
            if not ('verbose' in self.options and self.options['verbose'] != '0'):
                args.append('-s')
            if 'flac_quality' in self.options:
                args.append('-f ' + self.options['flac_quality'])
            else:
                args.append('-f ' + self.quality_default)
        else:
            args.append('-s -f ' + self.quality_default)

        #for tag in self.metadata.keys():
            #value = clean_word(self.metadata[tag])
            #args.append('-c %s="%s"' % (tag, value))
            #if tag in self.dub2args_dict.keys():
                #arg = self.dub2args_dict[tag]
                #args.append('-c %s="%s"' % (arg, value))

        return args

    def process(self, source, metadata, options=None):
        buffer_size = 0xFFFF
        self.options = options
        args = self.get_args()
        args = ' '.join(args)
        ext = self.file_extension()
        command = 'flac -c %s -' % args

        stream = self.core_process(command, source)
        temp_file = NamedTemporaryFile()
        for __chunk in stream:
            temp_file.write(__chunk)
            temp_file.flush()

        #self.write_tags(temp_file)

        while True:
            __chunk = temp_file.read(buffer_size)
            if len(__chunk) == 0:
                break
            yield __chunk

        temp_file.close()


