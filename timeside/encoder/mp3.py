    # -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Parisson SARL
# Copyright (c) 2006-2007 Guillaume Pellerin <pellerin@parisson.com>

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

# Authors: Guillaume Pellerin <yomguy@parisson.com>
#          Paul Brossier <piem@piem.org>

from timeside.core import Processor, implements, interfacedoc
from timeside.api import IEncoder
from timeside.encoder.gstutils import *

import mutagen

class Mp3Encoder(GstEncoder):
    """ gstreamer-based mp3 encoder """
    implements(IEncoder)

    def __init__(self, output, streaming=False):
        if isinstance(output, basestring):
            self.filename = output
        else:
            self.filename = None

        self.streaming = streaming
        if not self.filename and not self.streaming:
            raise Exception('Must give an output')

        self.metadata = None
        self.eod = False

    @interfacedoc
    def setup(self, channels=None, samplerate=None, nframes=None):
        super(Mp3Encoder, self).setup(channels, samplerate, nframes)

        self.pipe = '''appsrc name=src
                  ! audioconvert
                  ! lamemp3enc target=quality quality=2 encoding-engine-quality=standard ! id3v2mux
                  '''
        if self.filename and self.streaming:
            self.pipe += ''' ! tee name=t
            ! queue ! filesink location=%s
            t. ! queue ! appsink name=app sync=False
            ''' % self.filename

        elif self.filename :
            self.pipe += '! filesink location=%s async=False sync=False ' % self.filename
        else:
            self.pipe += '! queue ! appsink name=app sync=False '

        self.start_pipeline(channels, samplerate)
    
    @staticmethod
    @interfacedoc
    def id():
        return "gst_mp3_enc"

    @staticmethod
    @interfacedoc
    def description():
        return "MP3 GStreamer based encoder"

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

    @interfacedoc
    def set_metadata(self, metadata):
        self.metadata = metadata

    def write_metadata(self):
        """Write all ID3v2.4 tags to file from self.metadata"""
        from mutagen import id3
        id3 = id3.ID3(self.filename)
        for tag in self.metadata.keys():
            value = self.metadata[tag]
            frame = mutagen.id3.Frames[tag](3,value)
            try:
                id3.add(frame)
            except:
                raise IOError('EncoderError: cannot tag "'+tag+'"')
        try:
            id3.save()
        except:
            raise IOError('EncoderError: cannot write tags')

class Mp3EncoderSubprocess(object):
    """MP3 encoder in a subprocess pipe"""

#    implements(IEncoder)

    def __init__(self):
        import os
        import string
        import subprocess
        self.bitrate_default = '192'
        self.dub2id3_dict = {'title': 'TIT2', #title2
                             'creator': 'TCOM', #composer
                             'creator': 'TPE1', #lead
                             'identifier': 'UFID', #Unique ID...
                             'identifier': 'TALB', #album
                             'type': 'TCON', #genre
                             'publisher': 'TPUB', #comment
                             #'date': 'TYER', #year
                             }
        self.dub2args_dict = {'title': 'tt', #title2
                             'creator': 'ta', #composerS
                             'relation': 'tl', #album
                             #'type': 'tg', #genre
                             'publisher': 'tc', #comment
                             'date': 'ty', #year
                             }

    @interfacedoc
    def setup(self, channels=None, samplerate=None, nframes=None):
        self.channels = channels
        super(Mp3EncoderSubprocess, self).setup(channels, samplerate, nframes)

    @staticmethod
    @interfacedoc
    def id():
        return "subprocess_mp3_enc"

    @staticmethod
    @interfacedoc
    def description():
        return "MP3 subprocess based encoder"

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

    @interfacedoc
    def set_metadata(self, metadata):
        self.metadata = metadata

    def get_file_info(self):
        try:
            file_out1, file_out2 = os.popen4('mp3info "'+self.dest+'"')
            info = []
            for line in file_out2.readlines():
                info.append(clean_word(line[:-1]))
            self.info = info
            return self.info
        except:
            raise IOError('EncoderError: file does not exist.')

    def write_tags(self):
        """Write all ID3v2.4 tags by mapping dub2id3_dict dictionnary with the
            respect of mutagen classes and methods"""
        from mutagen import id3
        id3 = id3.ID3(self.dest)
        for tag in self.metadata.keys():
            if tag in self.dub2id3_dict.keys():
                frame_text = self.dub2id3_dict[tag]
                value = self.metadata[tag]
                frame = mutagen.id3.Frames[frame_text](3,value)
                try:
                    id3.add(frame)
                except:
                    raise IOError('EncoderError: cannot tag "'+tag+'"')
        try:
            id3.save()
        except:
            raise IOError('EncoderError: cannot write tags')

    def get_args(self):
        """Get process options and return arguments for the encoder"""
        args = []
        if not self.options is None:
            if not ( 'verbose' in self.options and self.options['verbose'] != '0' ):
                args.append('-S')
            if 'mp3_bitrate' in self.options:
                args.append('-b ' + self.options['mp3_bitrate'])
            else:
                args.append('-b '+self.bitrate_default)
            #Copyrights, etc..
            args.append('-c -o')
        else:
            args.append('-S -c --tt "unknown" -o')

        for tag in self.metadata:
            name = tag[0]
            value = clean_word(tag[1])
            if name in self.dub2args_dict.keys():
                arg = self.dub2args_dict[name]
                args.append('--' + arg + ' "' + value + '"')
        return args

    def process(self, source, metadata, options=None):
        self.metadata = metadata
        self.options = options
        args = self.get_args()
        args = ' '.join(args)
        command = 'lame %s - -' % args

        stream = self.core_process(command, source)
        for __chunk in stream:
            yield __chunk
