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

from timeside.decode import *
from timeside.core import *
import xml.dom.minidom
import xml.dom.ext


class SubProcessPipe:

    def __init__(self, command, stdin=None):
        """Read media and stream data through a generator.
        Taken from Telemeta (see http://telemeta.org)"""

        self.buffer_size = 0xFFFF

        if not stdin:
            stdin =  subprocess.PIPE

        self.proc = subprocess.Popen(command.encode('utf-8'),
                    shell = True,
                    bufsize = self.buffer_size,
                    stdin = stdin,
                    stdout = subprocess.PIPE,
                    close_fds = True)

        self.input = self.proc.stdin
        self.output = self.proc.stdout


class DecoderCore(Component):
    """Defines the main parts of the decoding tools :
    paths, metadata parsing, data streaming thru system command"""

    def __init__(self):
        self.command = 'sox "%s" -q -b 16 -r 44100 -t wav -c2 - '

    def process(self, source, options=None):
        """Encode and stream audio data through a generator"""

        command = self.command % source
        proc = SubProcessPipe(command)
        return proc.output

        #while True:
            #__chunk = proc.output.read(self.proc.buffer_size)
            #status = proc.poll()
            #if status != None and status != 0:
                #raise ExportProcessError('Command failure:', command, proc)
            #if len(__chunk) == 0:
                #break
            #yield __chunk



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
        raise IOError('DecoderError: path does not exist.')

def get_file_type_desc(path):
    """ Return the type of a file given by the 'file' command """
    try:
        file_out1, file_out2 = os.popen4('file "'+path+'"')
        for line in file_out2.readlines():
            description = line.split(': ')
            description = description[1].split(', ')
            return description
    except:
        raise IOError('DecoderError: path does not exist.')

def iswav(path):
    """ Tell if path is a WAV """
    try:
        mime = get_file_mime_type(path)
        return mime == 'audio/x-wav'
    except:
        raise IOError('DecoderError: path does not exist.')

def iswav16(path):
    """ Tell if path is a 16 bit WAV """
    try:
        file_type_desc = get_file_type_desc(path)
        return iswav(path) and '16 bit' in file_type_desc
    except:
        raise IOError('DecoderError: path does not exist.')

def get_file_name(path):
    """ Return the file name targeted in the path """
    return os.path.split(path)[1]

def split_file_name(file):
    """ Return main file name and its extension """
    try:
        return os.path.splitext(file)
    except:
        raise IOError('DecoderError: path does not exist.')

def clean_word(word) :
    """ Return the word without excessive blank spaces, underscores and
    characters causing problem to decodeers"""
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


