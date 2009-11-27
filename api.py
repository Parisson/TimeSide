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
    """Encoder driver interface. Each encoder is expected to support a specific
    format."""

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
        """Encode buffersize frames passed as a numpy array, where columns are channels.
        
           A number of frames less than buffersize means that the end of the data
           has been reached, and that the encoder should close the output file, stream,
           etc...

           In streaming mode the callback passed to the constructor is called whenever
           a block of encoded data is ready."""

class IDecoder(IProcessor):
    """Decoder driver interface. Decoders are different of encoders in that
    a given driver may support several input formats, hence this interface doesn't
    export any static method, all informations are dynamic."""

    def __init__(self, filename):
        """Create a new decoder for filename. Implementations of this interface 
        may accept optionnal arguments after filename."""

    def channels():
        """Return the number of channels"""

    def samplerate():
        """Return the samplerate"""

    def duration():
        """Return the duration in seconds"""

    def format():
        """Return a user-friendly file format string"""
   
    def encoding():
        """Return a user-friendly encoding string"""

    def resolution():
        """Return the sample depth"""

    def process(self):
        """Return a generator over the decoded data, as numpy arrays, where columns are
        channels, each array containing buffersize frames or less if the end of file
        has been reached."""

class IGrapher(IProcessor):
    """Media item visualizer driver interface"""

    def __init__(self, width, height):
        """Create a new grapher. Implementations of this interface 
        may accept optionnal arguments. width and height are generally
        in pixels but could be something else for eg. svg rendering, etc.."""

    @staticmethod
    def name():
        """Return the graph name, such as "Waveform", "Spectral view",
        etc..  """

    def set_colors(self, background=None, scheme=None):
        """Set the colors used for image generation. background is a RGB tuple,
        and scheme a a predefined color theme name"""
        pass

    def process(self, frames):
        """Process a block of buffersize frames passed as a numpy array, where 
        columns are channels. Passing less than buffersize frames means that
        the end of data has been reached"""

    def render(self):
        """Return a PIL Image object visually representing all of the data passed
        by repeatedly calling process()"""

class IAnalyzer(IProcessor):
    """Media item analyzer driver interface. This interface is abstract, it doesn't
    describe a particular type of analyzer but is rather meant to group analyzers.
    In particular, the way the result is returned may greatly vary from sub-interface
    to sub-interface. For example the IValueAnalyzer returns a final single numeric
    result at the end of the whole analysis. But some other analyzers may return
    numpy arrays, and this, either at the end of the analysis, or from process()
    for each block of data (as in Vamp)."""

    def __init__(self):
        """Create a new analyzer. Implementations of this interface 
        may accept optionnal arguments."""

    @staticmethod
    def name():
        """Return the analyzer name, such as "Mean Level", "Max level",
        "Total length, etc..  """

    @staticmethod
    def unit():
        """Return the unit of the data such as "dB", "seconds", etc...  """

    def process(self, frames):
        """Process a block of buffersize frames passed as a numpy array, where 
        columns are channels. Passing less than buffersize frames means that
        the end of data has been reached"""

class IValueAnalyzer(IAnalyzer):
    """Interface for analyzers which return a single numeric value from result()"""

    def result():
        """Return the final result of the analysis performed over the data passed by
        repeatedly calling process()"""

