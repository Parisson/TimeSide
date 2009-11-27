# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2009 Parisson
# Copyright (c) 2007 Olivier Guilyardi <olivier@samalyse.com>
# Copyright (c) 2007-2009 Guillaume Pellerin <pellerin@parisson.com>
#
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

from timeside.component import Interface

class IProcessor(Interface):
    """Base processor interface"""

    @staticmethod
    def id():
        """Return a short alphanumeric, lower-case string which uniquely
        identify this processor. Only letters and digits are allowed.
        An exception will be raised by MetaProcessor if the id is malformed or
        not unique amongst registered processors.
        
        Typically this identifier is likely to be used during HTTP requests
        and be passed as a GET parameter. Thus it should be as short as possible."""

class IEncoder(IProcessor):
    """Encoder driver interface"""

    def __init__(self, output, nchannels, samplerate):
        """The constructor must always accept the output, nchannels and samplerate 
        arguments.  It may accepts extra arguments such as bitrate, depth, etc.., 
        but these must be optionnal, that is have a default value.
        
        The output must either be a filepath or a callback function/method for 
        for the streaming mode. The callback must accept one argument which is 
        block of binary data.
        """

    @staticmethod
    def format():
        """Return the encode/encoding format as a short string
        Example: "MP3", "OGG", "AVI", ...
        """

    @staticmethod
    def description():
        """Return a string describing what this encode format provides, is good
        for, etc... The description is meant to help the end user decide what
        format is good for him/her
        """

    @staticmethod
    def file_extension():
        """Return the filename extension corresponding to this encode format"""

    @staticmethod
    def mime_type():
        """Return the mime type corresponding to this encode format"""

    def set_metadata(self, metadata):
        """metadata is a tuple containing tuples for each descriptor return by
        the dc.Ressource of the item, in the model order :
        ((name1, value1),(name2, value2),(name1, value3), ...)"""

    def update(self):
        """Updates the metadata into the file passed as the output argument
           to the constructor. This method can't be called in streaming
           mode."""

    def process(self, frames):
        """Encode the frames passed as a numpy array, where columns are channels.
        
           In streaming mode the callback passed to the constructor is called whenever
           a block of encoded data is ready."""

    def finish(self):
        """Flush the encoded data and close the output file/stream. Calling this method
        may cause the streaming callback to be called if in streaming mode."""
  

class IDecoder(IProcessor):
    """Decoder driver interface"""

    @staticmethod
    def format():
        """Return the decode/encoding format as a short string 
        Example: "MP3", "OGG", "AVI", ...
        """
   
    @staticmethod
    def description():
        """Return a string describing what this decode format provides, is good 
        for, etc... The description is meant to help the end user decide what 
        format is good for him/her
        """

    @staticmethod
    def file_extension():
        """Return the filename extension corresponding to this decode format"""

    @staticmethod
    def mime_type():
        """Return the mime type corresponding to this decode format"""

    def process(self, source, options=None):
        """Perform the decoding process and stream the result through a generator

        source is the audio/video source file absolute path.

        It is highly recommended that decode drivers implement some sort of
        cache instead of re-encoding each time process() is called.

        It should be possible to make subsequent calls to process() with
        different items, using the same driver instance.
        """

class IGrapher(IProcessor):
    """Media item visualizer driver interface"""

    @staticmethod
    def name():
        """Return the graph name, such as "Waveform", "Spectral view",
        etc..
        """

    def set_colors(self, background=None, scheme=None):
        """Set the colors used for image generation. background is a RGB tuple,
        and scheme a a predefined color theme name"""
        pass

    def render(self, media_item, width=None, height=None, options=None):
        """Generator that streams the graph output as a PNG image"""

class IAnalyzer(IProcessor):
    """Media item analyzer driver interface"""

    @staticmethod
    def name():
        """Return the analyzer name, such as "Mean Level", "Max level",
        "Total length, etc..
        """

    @staticmethod
    def unit():
        """Return the unit of the data such as "dB", "seconds", etc...
        """

    def render(self, media, options=None):
        """Return the result data of the process"""

