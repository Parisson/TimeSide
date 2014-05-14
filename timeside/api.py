# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2013 Parisson SARL
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
from __future__ import absolute_import


from .component import Interface


class IProcessor(Interface):

    """Common processor interface"""

    @staticmethod
    def id():
        """Short alphanumeric, lower-case string which uniquely identify this
        processor, suitable for use as an HTTP/GET argument value, in filenames,
        etc..."""

        # implementation: only letters and digits are allowed. An exception will
        # be raised by MetaProcessor if the id is malformed or not unique amongst
        # registered processors.

    def setup(self, channels=None, samplerate=None, blocksize=None, totalframes=None):
        """Allocate internal resources and reset state, so that this processor is
        ready for a new run.

        The channels, samplerate and/or blocksize and/or totalframes arguments
        may be required by processors which accept input. An error will occur if any of
        these arguments is passed to an output-only processor such as a decoder.
        """

        # implementations should always call the parent method

    def channels(self):
        """Number of channels in the data returned by process(). May be different from
        the number of channels passed to setup()"""

    def samplerate(self):
        """Samplerate of the data returned by process(). May be different from
        the samplerate passed to setup()"""

    def blocksize():
        """The total number of frames that this processor can output for each step
        in the pipeline, or None if the number is unknown."""

    def totalframes():
        """The total number of frames that this processor will output, or None if
        the number is unknown."""

    def process(self, frames=None, eod=False):
        """Process input frames and return a (output_frames, eod) tuple.
        Both input and output frames are 2D numpy arrays, where columns are
        channels, and containing an undetermined number of frames.  eod=True
        means that the end-of-data has been reached.

        Output-only processors (such as decoders) will raise an exception if the
        frames argument is not None. All processors (even encoders) return data,
        even if that means returning the input unchanged.

        Warning: it is required to call setup() before this method."""

    def post_process(self):
        '''
        Post-Process data after processign the input frames with process()

        Processors such as analyzers will produce Results during the Post-Process
        '''

    def release(self):
        """Release resources owned by this processor. The processor cannot
        be used anymore after calling this method."""

        # implementations should always call the parent method

    def mediainfo(self):
        """
        Information about the media object
        uri
        start
        duration
        """

    @staticmethod
    def uuid():
        """Return the UUID of the processor"""


class IEncoder(IProcessor):

    """Encoder driver interface. Each encoder is expected to support a specific
    format."""

    def __init__(self, output):
        """Create a new encoder. output can either be a filename or a python callback
        function/method for streaming mode.

        The streaming callback prototype is: callback(data, eod)
        Where data is a block of binary data of an undetermined size, and eod
        True when end-of-data is reached."""

        # implementation: the constructor must always accept the output argument. It may
        # accept extra arguments such as bitrate, depth, etc.., but these must
        # be optionnal

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
        """Set the metadata to be embedded in the encoded output.

        In non-streaming mode, this method updates the metadata directly into the
        output file, without re-encoding the audio data, provided this file already
        exists.

        It isn't required to call this method, but if called, it must be before
        process()."""


class IDecoder(IProcessor):

    """Decoder driver interface. Decoders are different of encoders in that
    a given driver may support several input formats, hence this interface doesn't
    export any static method, all informations are dynamic."""

    def __init__(self, filename):
        """Create a new decoder for filename."""
        # implementation: additional optionnal arguments are allowed

    def format():
        """Return a user-friendly file format string"""

    def encoding():
        """Return a user-friendly encoding string"""

    def resolution():
        """Return the sample width (8, 16, etc..) of original audio file/stream,
           or None if not applicable/known"""

    def metadata(self):
        """Return the metadata embedded into the encoded stream, if any."""

    def mime_type():
        """Return the mime type corresponding to this decoded format"""


class IGrapher(IProcessor):

    """Media item visualizer driver interface"""

    # implementation: graphers which need to know the total number of frames
    # should raise an exception in setup() if the totalframes argument is None

    def __init__(self, width, height):
        """Create a new grapher. width and height are generally
        in pixels but could be something else for eg. svg rendering, etc.. """

        # implementation: additional optionnal arguments are allowed

    @staticmethod
    def name():
        """Return the graph name, such as "Waveform", "Spectral view",
        etc..  """

    def set_colors(self, background=None, scheme=None):
        """Set the colors used for image generation. background is a RGB tuple,
        and scheme a a predefined color theme name"""

    def render(self, output=None):
        """Return a PIL Image object visually representing all of the data passed
        by repeatedly calling process() and write the image to the output if specified"""


class IAnalyzer(IProcessor):

    """Media item analyzer driver interface. This interface is abstract, it doesn't
    describe a particular type of analyzer but is rather meant to group analyzers.
    In particular, the way the result is returned may greatly vary from sub-interface
    to sub-interface. For example the IValueAnalyzer returns a final single numeric
    result at the end of the whole analysis. But some other analyzers may return
    numpy arrays, and this, either at the end of the analysis, or from process()
    for each block of data (as in Vamp)."""

    def __init__(self):
        """Create a new analyzer."""
        # implementation: additional optionnal arguments are allowed

    @staticmethod
    def name():
        """Return the analyzer name, such as "Mean Level", "Max level",
        "Total length, etc..  """

    @staticmethod
    def unit():
        """Return the unit of the data such as "dB", "seconds", etc...  """


class IValueAnalyzer(IAnalyzer):

    """Interface for analyzers which return a single numeric value from result()"""

    def result():
        """Return the final result of the analysis performed over the data passed by
        repeatedly calling process()"""

    def results():
        """Return the final results of the analysis performed over the data passed by
        repeatedly calling process()"""

    def __str__(self):
        """Return a human readable string containing both result and unit
        ('5.30dB', '4.2s', etc...)"""


class IEffect(IProcessor):

    """Effect processor interface"""

    def __init__(self):
        """Create a new effect."""
        # implementation: additional optionnal arguments are allowed

    @staticmethod
    def name():
        """Return the effect name"""
