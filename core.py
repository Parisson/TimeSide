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
           'interfacedoc', 'processors', 'get_processor', 'ProcessPipe']

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

    @interfacedoc
    def setup(self, channels=None, samplerate=None):
        self.input_channels   = channels
        self.input_samplerate = samplerate

    @interfacedoc
    def channels(self):
        # default implementation returns the input channels, but processors may change
        # this behaviour by overloading this method
        return self.input_channels

    @interfacedoc
    def samplerate(self):
        # default implementation returns the input samplerate, but processors may change
        # this behaviour by overloading this method
        return self.input_samplerate

    @interfacedoc
    def process(self, frames):
        return frames

    @interfacedoc
    def release(self):
        pass

    def __or__(self, item):
        return ProcessPipe(self, item)

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

class ProcessPipe(object):
    """Handle a pipe of processors"""

    def __init__(self, *processors):
        self.processors = processors

    def __or__(self, processor):
        p = []
        p.extend(self.processors)
        p.append(processor)
        return ProcessPipe(*p)

    def run(self):
        """Setup/reset all processors in cascade and stream audio data along
        the pipe"""

        source = self.processors[0]
        items  = self.processors[1:]

        # setup/reset processors and configure channels and samplerate throughout the pipe
        source.setup()
        last = source
        for item in items:
            item.setup(last.channels(), last.samplerate())
            last = item

        # now stream audio data along the pipe
        eod = False
        while not eod:
            frames, eod = source.process()
            for item in items:
                frames, eod = item.process(frames, eod)

