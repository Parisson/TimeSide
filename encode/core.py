#!/usr/bin/python
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
import re
import md5
import string
import subprocess
import mutagen

from timeside.export import *
from timeside.core import *
import xml.dom.minidom
import xml.dom.ext

class ExporterCore(Component):
    """Defines the main parts of the exporting tools :
    paths, metadata parsing, data streaming thru system command"""

    def __init__(self):
        self.source = ''
        self.collection = ''
        self.verbose = ''
        self.dest = ''
        self.metadata = []
        self.cache_dir = 'cache'
        self.buffer_size = 0xFFFF

    def set_cache_dir(self,path):
        self.cache_dir = path

    def normalize(self):
        """ Normalize the source and return its path """
        args = ''
        if self.verbose == '0':
            args = '-q'
        try:
            os.system('normalize-audio '+args+' "'+self.source+'"')
            return self.source
        except:
            raise IOError('ExporterError: cannot normalize, path does not exist.')

    def check_md5_key(self):
        """ Check if the md5 key is OK and return a boolean """
        try:
            md5_log = os.popen4('md5sum -c "'+self.dest+ \
                                '" "'+self.dest+'.md5"')
            return 'OK' in md5_log.split(':')
        except IOError:
            raise IOError('ExporterError: cannot check the md5 key.')
    
    def get_file_info(self):
        """ Return the list of informations of the dest """
        return self.export.get_file_info()

    def get_wav_length_sec(self) :
        """ Return the length of the audio source file in seconds """
        try:
            file1, file2 = os.popen4('wavinfo "'+self.source+ \
                                     '" | grep wavDataSize')
            for line in file2.readlines():
                line_split = line.split(':')
                value = int(int(line_split[1])/(4*44100))
                return value
        except:
            raise IOError('ExporterError: cannot get the wav length.')

    def compare_md5_key(self, source, dest):
        """ Compare source and dest files wih md5 method """
        f_source = open(source).read()
        f_dest = open(dest).read()
        return md5.new(f_source).digest() == md5.new(f_dest).digest()

    def write_metadata_xml(self,path):
        doc = xml.dom.minidom.Document()
        root = doc.createElement('timeside')
        doc.appendChild(root)
        for tag in self.metadata.keys() :
            value = self.metadata[tag]
            node = doc.createElement(tag)
            node.setAttribute('value', str(value))
            #node.setAttribute('type', get_type(value))
            root.appendChild(node)
        xml_file = open(path, "w")
        xml.dom.ext.PrettyPrint(doc, xml_file)
        xml_file.close()

    def pre_process(self, item_id, source, metadata, ext,
                    cache_dir, options=None):
        """ Pre processing : prepare the export path and return it"""
        self.item_id = str(item_id)
        self.source = source
        file_name = get_file_name(self.source)
        file_name_wo_ext, file_ext = split_file_name(file_name)
        self.cache_dir = cache_dir
        self.metadata = metadata
        #self.collection = self.metadata['Collection']
        #self.artist = self.metadata['Artist']
        #self.title = self.metadata['Title']

        # Normalize if demanded
        if not options is None:
            self.options = options
            if 'normalize' in self.options and \
                self.options['normalize'] == True:
                self.normalize()

        # Define the export directory
        self.ext = self.get_file_extension()
        export_dir = os.path.join(self.cache_dir,self.ext)

        if not os.path.exists(export_dir):
            export_dir_split = export_dir.split(os.sep)
            path = os.sep + export_dir_split[0]
            for _dir in export_dir_split[1:]:
                path = os.path.join(path,_dir)
                if not os.path.exists(path):
                    os.mkdir(path)
        else:
            path = export_dir

        # Set the target file
        target_file = self.item_id+'.'+self.ext
        dest = os.path.join(path,target_file)
        return dest

    def core_process(self, command, buffer_size, dest):
        """Encode and stream audio data through a generator"""

        __chunk = 0
        file_out = open(dest,'w')

        proc = subprocess.Popen(command.encode('utf-8'),
                    shell = True,
                    bufsize = buffer_size,
                    stdin = subprocess.PIPE,
                    stdout = subprocess.PIPE,
                    close_fds = True)

        # Core processing
        while True:
            __chunk = proc.stdout.read(buffer_size)
            status = proc.poll()
            if status != None and status != 0:
                raise ExportProcessError('Command failure:', command, proc)
            if len(__chunk) == 0:
                break
            yield __chunk
            file_out.write(__chunk)

        file_out.close()

    def post_process(self, item_id, source, metadata, ext, 
                     cache_dir, options=None):
        """ Post processing : write tags, print infos, etc..."""
        #self.write_tags()
        if not options is None:
            if 'verbose' in self.options and self.options['verbose'] != '0':
                print self.dest
                print self.get_file_info()


# External functions

def get_type(value):
    """ Return a String with the type of value """
    types = {bool : 'bool', int : 'int', str : 'str'}
    # 'bool' type must be placed *before* 'int' type, otherwise booleans are
    # detected as integers
    for type in types.keys():
        if isinstance(value, type) :
            return types[type]
    raise TypeError(str(value) + ' has an unsupported type')

def get_cast(value, type) :
    """ Return value, casted into type """
    if type == 'bool' :
        if value == 'True' :
            return True
        return False
    elif type == 'int' :
        return int(value)
    elif type == 'str' :
        return str(value)
    raise TypeError(type + ' is an unsupported type')

def get_file_mime_type(path):
    """ Return the mime type of a file """
    try:
        file_out1, file_out2 = os.popen4('file -i "'+path+'"')
        for line in file_out2.readlines():
            line_split = line.split(': ')
            mime = line_split[len(line_split)-1]
            return mime[:len(mime)-1]
    except:
        raise IOError('ExporterError: path does not exist.')

def get_file_type_desc(path):
    """ Return the type of a file given by the 'file' command """
    try:
        file_out1, file_out2 = os.popen4('file "'+path+'"')
        for line in file_out2.readlines():
            description = line.split(': ')
            description = description[1].split(', ')
            return description
    except:
        raise IOError('ExporterError: path does not exist.')

def iswav(path):
    """ Tell if path is a WAV """
    try:
        mime = get_file_mime_type(path)
        return mime == 'audio/x-wav'
    except:
        raise IOError('ExporterError: path does not exist.')

def iswav16(path):
    """ Tell if path is a 16 bit WAV """
    try:
        file_type_desc = get_file_type_desc(path)
        return iswav(path) and '16 bit' in file_type_desc
    except:
        raise IOError('ExporterError: path does not exist.')

def get_file_name(path):
    """ Return the file name targeted in the path """
    return os.path.split(path)[1]

def split_file_name(file):
    """ Return main file name and its extension """
    try:
        return os.path.splitext(file)
    except:
        raise IOError('ExporterError: path does not exist.')

def clean_word(word) :
    """ Return the word without excessive blank spaces, underscores and
    characters causing problem to exporters"""
    word = re.sub("^[^\w]+","",word)    #trim the beginning
    word = re.sub("[^\w]+$","",word)    #trim the end
    word = re.sub("_+","_",word)        #squeeze continuous _ to one _
    word = re.sub("^[^\w]+","",word)    #trim the beginning _
    #word = string.replace(word,' ','_')
    #word = string.capitalize(word)
    dict = '&[];"*:,'
    for letter in dict:
        word = string.replace(word,letter,'_')
    return word

def recover_par_key(path):
    """ Recover a file with par2 key """
    os.system('par2 r "'+path+'"')

def verify_par_key(path):
    """ Verify a par2 key """
    os.system('par2 v "'+path+'.par2"')


