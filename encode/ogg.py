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

from timeside.export.core import *
from timeside.export.api import IExporter
from mutagen.oggvorbis import OggVorbis

class OggExporter(ExporterCore):
    """Defines methods to export to OGG Vorbis"""

    implements(IExporter)
    
    def __init__(self):
        self.item_id = ''
        self.metadata = {}
        self.description = ''
        self.info = []
        self.source = ''
        self.dest = ''
        self.options = {}
        self.bitrate_default = '192'
        self.buffer_size = 0xFFFF
        self.dub2args_dict = {'creator': 'artist',
                             'relation': 'album'
                             }
        
    def get_format(self):
        return 'OGG'
    
    def get_file_extension(self):
        return 'ogg'

    def get_mime_type(self):
        return 'application/ogg'

    def get_description(self):
        return 'FIXME'

    def get_file_info(self):
        try:
            file_out1, file_out2 = os.popen4('ogginfo "'+self.dest+'"')
            info = []
            for line in file_out2.readlines():
                info.append(clean_word(line[:-1]))
            self.info = info
            return self.info
        except:
            raise IOError('ExporterError: file does not exist.')

    def set_cache_dir(self,path):
       self.cache_dir = path

    def decode(self):
        try:
            os.system('oggdec -o "'+self.cache_dir+os.sep+self.item_id+
                      '.wav" "'+self.source+'"')
            return self.cache_dir+os.sep+self.item_id+'.wav'
        except:
            raise IOError('ExporterError: decoder is not compatible.')

    def write_tags(self):
        media = OggVorbis(self.dest)
        for tag in self.metadata.keys():
            media[tag] = str(self.metadata[tag])
        media.save()

    def get_args(self,options=None):
        """Get process options and return arguments for the encoder"""
        args = []
        if not options is None:
            self.options = options
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

    def process(self, item_id, source, metadata, options=None):
        self.item_id = item_id
        self.source = source
        self.metadata = metadata
        self.args = self.get_args(options)
        self.ext = self.get_file_extension()
        self.args = ' '.join(self.args)
        self.command = 'sox "%s" -s -q -b 16 -r 44100 -t wav -c2 - | oggenc %s -' % (self.source, self.args)

        # Pre-proccessing
        self.dest = self.pre_process(self.item_id,
                                        self.source,
                                        self.metadata,
                                        self.ext,
                                        self.cache_dir,
                                        self.options)

        # Processing (streaming + cache writing)
        stream = self.core_process(self.command, self.buffer_size, self.dest)
        for chunk in stream:
            yield chunk
    
        # Post-proccessing
        #self.post_process(self.item_id,
                        #self.source,
                        #self.metadata,
                        #self.ext,
                        #self.cache_dir,
                        #self.options)

