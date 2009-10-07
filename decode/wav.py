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

from timeside.export.core import *
from timeside.export.api import IExporter

class WavExporter(ExporterCore):
    """Defines methods to export to WAV"""

    implements(IExporter)
    
    def __init__(self):
        self.item_id = ''
        self.metadata = {}
        self.description = ''
        self.info = []
        self.source = ''
        self.dest = ''
        self.options = {}
        self.buffer_size = 0xFFFF

    def get_format(self):
        return 'WAV'
    
    def get_file_extension(self):
        return 'wav'

    def get_mime_type(self):
        return 'audio/x-wav'

    def get_description(self):
        return 'FIXME'

    def get_file_info(self):
        try:
            file1, file2 = os.popen4('wavinfo "'+self.dest+'"')
            info = []
            for line in file2.readlines():
                info.append(clean_word(line[:-1]))
            self.info = info
            return self.info
        except:
            raise IOError('ExporterError: wavinfo id not installed or file does not exist.')

    def set_cache_dir(self,path):
        self.cache_dir = path

    def decode(self):
        try:
            file_name, ext = get_file_name(self.source)
            dest = self.cache_dir+os.sep+file_name+'.wav'
            os.system('sox "'+self.source+'" -s -r 44100 -t wav -c2 "'+ \
                      dest+'.wav"')
            self.source = dest
            return dest
        except:
            raise IOError('ExporterError: decoder is not compatible.')

    def write_tags(self):
        # Create metadata XML file !
        self.write_metadata_xml(self.dest+'.xml')
    
    def create_md5_key(self):
        """ Create the md5 keys of the dest """
        try:
            os.system('md5sum -b "'+self.dest+'" >"'+self.dest+'.md5"')
        except:
            raise IOError('ExporterError: cannot create the md5 key.')
    
    def create_par_key(self):
        """ Create the par2 keys of the dest """
        args = 'c -n1 '
        if 'verbose' in self.options and self.options['verbose'] != '0':
            args = args
        else:
            args = args + '-q -q '

        try:
            os.system('par2 '+args+' "'+self.dest+'"')
        except:
            raise IOError('ExporterError: cannot create the par2 key.')

    def process(self, item_id, source, metadata, options=None):
        self.item_id = item_id
        self.source = source
        self.metadata = metadata
        self.options = {}

        if not options is None:
            self.options = options

        # Pre-proccessing
        self.ext = self.get_file_extension()
        self.dest = self.pre_process(self.item_id,
                                        self.source,
                                        self.metadata,
                                        self.ext,
                                        self.cache_dir,
                                        self.options)

        # Initializing
        file_in = open(self.source,'rb')
        file_out = open(self.dest,'w')

        # Core Processing
        while True:
            chunk = file_in.read(self.buffer_size)
            if len(chunk) == 0:
                break
            yield chunk
            file_out.write(chunk)

        file_in.close()
        file_out.close()

        # Create the md5 key
        #if 'md5' in self.metadata and self.metadata['md5']:
        self.create_md5_key()

        # Create the par2 key
        #if 'par2' in self.metadata and self.metadata['par2']:
        #self.create_par_key()

        # Pre-proccessing
        self.post_process(self.item_id,
                        self.source,
                        self.metadata,
                        self.ext,
                        self.cache_dir,
                        self.options)



            #if self.compare_md5_key():
            #os.system('cp -a "'+self.source+'" "'+ self.dest+'"')
            #print 'COPIED'

