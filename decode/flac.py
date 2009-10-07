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
from mutagen.flac import FLAC
from tempfile import NamedTemporaryFile

class FlacExporter(ExporterCore):
    """Defines methods to export to FLAC"""

    implements(IExporter)
    
    def __init__(self):
        self.item_id = ''
        self.source = ''
        self.metadata = {}
        self.options = {}
        self.description = ''
        self.dest = ''
        self.quality_default = '-5'
        self.info = []
        self.buffer_size = 0xFFFF

    def get_format(self):
        return 'FLAC'
    
    def get_file_extension(self):
        return 'flac'

    def get_mime_type(self):
        return 'application/flac'

    def get_description(self):
        return 'FIXME'

    def get_file_info(self):
        try:
            file1, file2 = os.popen4('metaflac --list "'+self.dest+'"')
            info = []
            for line in file2.readlines():
                info.append(clean_word(line[:-1]))
            self.info = info
            return self.info
        except:
            raise IOError('ExporterError: metaflac is not installed or ' + \
                           'file does not exist.')

    def set_cache_dir(self,path):
        """Set the directory where cached files should be stored. Does nothing
        if the exporter doesn't support caching. 
       
        The driver shouldn't assume that this method will always get called. A
        temporary directory should be used if that's not the case.
        """
        self.cache_dir = path

    def decode(self):
        try:
            file_name, ext = get_file_name(self.source)
            dest = self.cache_dir+os.sep+file_name+'.wav'
            os.system('flac -d -o "'+dest+'" "'+self.source+'"')
            self.source = dest
            return dest
        except:
            raise IOError('ExporterError: decoder is not compatible.')

    def write_tags(self, file):
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
            raise IOError('ExporterError: cannot write tags.')

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

    def process(self, item_id, source, metadata, options=None):
        self.item_id = item_id
        self.source = source
        self.metadata = metadata
        self.args = self.get_args(options)
        self.ext = self.get_file_extension()
        self.args = ' '.join(self.args)
        self.command = 'sox "%s" -s -q -b 16 -r 44100 -t wav -c2 - | flac -c %s - ' % (self.source, self.args)

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
            pass

        self.write_tags(self.dest)
        file = open(self.dest,'r')
        
        while True:
            chunk = file.read(self.buffer_size)
            if len(chunk) == 0:
                break
            yield chunk

        file.close()

        # Post-proccessing
        #self.post_process(self.item_id,
                         #self.source,
                         #self.metadata,
                         #self.ext,
                         #self.cache_dir,
                         #self.options)

