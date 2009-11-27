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
import re

__all__ = ['Processor', 'Component', 'implements', 'processors', 'TimeSideError']

class TimeSideError(Exception):
    """Exception base class for errors in TimeSide."""
    # FIXME: is this redundant with Django's error handling ?

_processors = {}

class MetaProcessor(MetaComponent):
    """Metaclass of the Processor class, used mainly for ensuring that processor
    id's are wellformed and unique"""

    valid_id = re.compile("^[a-z][a-z0-9]*$")

    def __new__(cls, name, bases, d):
        new_class = MetaComponent.__new__(cls, name, bases, d)
        if new_class in implementations(IProcessor):
            id = str(new_class.id())
            if _processors.has_key(id):
                raise TimeSideError("%s and %s have the same id: '%s'"
                    % (new_class.__name__, _processors[id].__name__, id))
            if not MetaProcessor.valid_id.match(id):
                raise TimeSideError("%s has a malformed id: '%s'"
                    % (new_class.__name__, id))
                

            _processors[id] = new_class

        return new_class

class Processor(Component):
    """Base component class of all processors"""
    __metaclass__ = MetaProcessor

def processors(interface=IProcessor, recurse=True):
    """Returns the processors implementing a given interface and, if recurse,
    any of the descendants of this interface."""
    return implementations(interface, recurse)
    
