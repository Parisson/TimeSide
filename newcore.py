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



# This file defines an object interface mechanism and a way to determine
# which components implements a given interface
#
# For example, the following defines the Music class as implementing the
# listenable interface.
#
# class Listenable(Interface):
#     pass
#
# class Music(Component):
#    implements(Listenable)
#
# Several class can implements a such interface, and it is possible to 
# discover which class implements it with implementations():
#
# list_of_classes = implementations(Listenable)
#
# This mechanism support inheritance of both interfaces and components:
#
# - all descendants of a class implementing a given interface are also considered
#   to implement this interface
# - a class implementing a given interface is also considered to implement all
#   the ascendants of this interface

__all__ = ['Component', 'implements', 'Interface', 'implementations', 'TimeSideError']

class TimeSideError(Exception):
    """Exception base class for errors in TimeSide."""
    # FIXME: is this redundant with Django's error handling ?
    # FIXME: this class doesn't belong to the core

class Interface(object):
    """Marker base class for interfaces."""

def implements(*interfaces):
    _implements.extend(interfaces)

def implementations(interface):
    result = []
    find_implementations(interface, result)
    return result

_implementations = []
_implements = []

class ComponentMeta(type):

    def __new__(cls, name, bases, d):
        new_class = type.__new__(cls, name, bases, d)
        if _implements:
            for i in _implements:
                _implementations.append((i, new_class))
        del _implements[:]
        return new_class

class Component(object):
    __metaclass__ = ComponentMeta 

def extend_unique(list1, list2):
    for item in list2:
        if item not in list1:
            list1.append(item)

def find_implementations(interface, result):
    for i, cls in _implementations:
        if (i == interface):
            extend_unique(result, [cls])
            extend_unique(result, cls.__subclasses__())

    subinterfaces = interface.__subclasses__()
    if subinterfaces:
        for i in subinterfaces:
            find_implementations(i, result)

