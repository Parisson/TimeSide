# -*- coding: utf-8 -*-
#
# Copyright (c) 2009 Olivier Guilyardi <olivier@samalyse.com>
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

from timeside.component import *
from timeside.api import IProcessor
from timeside.exceptions import Error, ApiError
import re

__all__ = ['Processor', 'MetaProcessor', 'implements', 'abstract', 
           'interfacedoc', 'processors', 'get_processor']

_processors = {}

class MetaProcessor(MetaComponent):
    """Metaclass of the Processor class, used mainly for ensuring that processor
    id's are wellformed and unique"""

    valid_id = re.compile("^[a-z][_a-z0-9]*$")

    def __new__(cls, name, bases, d):
        new_class = MetaComponent.__new__(cls, name, bases, d)
        if new_class in implementations(IProcessor):
            id = str(new_class.id())
            if _processors.has_key(id):
                raise ApiError("%s and %s have the same id: '%s'"
                    % (new_class.__name__, _processors[id].__name__, id))
            if not MetaProcessor.valid_id.match(id):
                raise ApiError("%s has a malformed id: '%s'"
                    % (new_class.__name__, id))

            _processors[id] = new_class

        return new_class

class Processor(Component):
    """Base component class of all processors"""
    __metaclass__ = MetaProcessor

    abstract()
    implements(IProcessor)

    DEFAULT_BUFFERSIZE = 0x10000
    MIN_BUFFERSIZE = 0x1000

    __buffersize = DEFAULT_BUFFERSIZE

    @interfacedoc
    def buffersize(self):
        return self.__buffersize

    def set_buffersize(self, value):
        """Set the buffer size used by this processor. The buffersize must be a 
        power of 2 and greater than or equal to MIN_BUFFERSIZE or an exception will 
        be raised."""
        if value < self.MIN_BUFFERSIZE:
            raise Error("Invalid buffer size: %d. Must be greater than or equal to %d",
                        value, MIN_BUFFERSIZE);
        v = value                        
        while v > 1:
            if v & 1:
                raise Error("Invalid buffer size: %d. Must be a power of two",
                            value, MIN_BUFFERSIZE);
            v >>= 1                            

        self.__buffersize = value

    @interfacedoc
    def set_input_format(self, nchannels=None, samplerate=None):
        self.input_channels   = nchannels
        self.input_samplerate = samplerate

    @interfacedoc
    def input_format(self):
        return (self.input_channels, self.input_samplerate)

    @interfacedoc
    def output_format(self):        
        return (self.input_channels, self.input_samplerate)

    @interfacedoc
    def process(self, frames):
        return frames

def processors(interface=IProcessor, recurse=True):
    """Returns the processors implementing a given interface and, if recurse,
    any of the descendants of this interface."""
    return implementations(interface, recurse)
    

def get_processor(processor_id):
    """Return a processor by its id"""
    if not _processors.has_key(processor_id):
        raise Error("No processor registered with id: '%s'" 
              % processor_id)

    return _processors[processor_id]

