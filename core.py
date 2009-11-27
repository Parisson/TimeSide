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

__all__ = ['Processor', 'Component', 'implements', 'processors', 'TimeSideError']

class TimeSideError(Exception):
    """Exception base class for errors in TimeSide."""
    # FIXME: is this redundant with Django's error handling ?

_processors = []

class MetaProcessor(MetaComponent):
    """Metaclass of the Processor class, used mainly for ensuring uniqueness of 
    processor id's"""
    def __new__(cls, name, bases, d):
        new_class = MetaComponent.__new__(cls, name, bases, d)
        id = "fixme"
        _processors.append((id, new_class))
        return new_class

class Processor(Component):
    """Base component class of all processors"""
    __metaclass__ = MetaProcessor

def processors(interface=IProcessor, recurse=True):
    """Returns the processors implementing a given interface and, if recurse,
    any of the descendants of this interface."""
    return implementations(interface, recurse)
    
