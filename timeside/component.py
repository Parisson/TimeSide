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


# This file defines a generic object interface mechanism and
# a way to determine which components implements a given interface.
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
# This mechanism support inheritance of interfaces: a class implementing a given
# interface is also considered to implement all the ascendants of this interface.
#
# However, inheritance is not supported for components. The descendants of a class
# implementing a given interface are not automatically considered to implement this
# interface too.

__all__ = ['Component', 'MetaComponent', 'implements', 'abstract',
           'interfacedoc', 'Interface', 'implementations', 'ComponentError']


class Interface(object):

    """Marker base class for interfaces."""


def implements(*interfaces):
    """Registers the interfaces implemented by a component when placed in the
    class header"""
    MetaComponent.implements.extend(interfaces)


def abstract():
    """Declare a component as abstract when placed in the class header"""
    MetaComponent.abstract = True


def implementations(interface, recurse=True, abstract=False):
    """Returns the components implementing interface, and if recurse, any of
    the descendants of interface. If abstract is True, also return the
    abstract implementations."""
    result = []
    find_implementations(interface, recurse, abstract, result)
    return result


def interfacedoc(func):
    if isinstance(func, staticmethod):
        raise ComponentError(
            "@interfacedoc can't handle staticmethod (try to put @staticmethod above @interfacedoc)")

    if not func.__doc__:
        func.__doc__ = "@interfacedoc"
        func._interfacedoc = True
    return func


class MetaComponent(type):

    """Metaclass of the Component class, used mainly to register the interface
    declared to be implemented by a component."""

    implementations = []
    implements = []
    abstract = False

    def __new__(cls, name, bases, d):
        new_class = type.__new__(cls, name, bases, d)

        # Register implementations
        if MetaComponent.implements:
            for i in MetaComponent.implements:
                MetaComponent.implementations.append({
                    'interface': i,
                    'class': new_class,
                    'abstract': MetaComponent.abstract})

        # Propagate @interfacedoc
        for name in new_class.__dict__:
            member = new_class.__dict__[name]
            if isinstance(member, staticmethod):
                member = getattr(new_class, name)

            if member.__doc__ == "@interfacedoc":
                if_member = None
                for i in MetaComponent.implements:
                    if hasattr(i, name):
                        if_member = getattr(i, name)
                if not if_member:
                    raise ComponentError("@interfacedoc: %s.%s: no such member in implemented interfaces: %s"
                                         % (new_class.__name__, name, str(MetaComponent.implements)))
                member.__doc__ = if_member.__doc__

        MetaComponent.implements = []
        MetaComponent.abstract = False

        return new_class


class Component(object):

    """Base class of all components"""
    __metaclass__ = MetaComponent


def extend_unique(list1, list2):
    """Extend list1 with list2 as list.extend(), but doesn't append duplicates
    to list1"""
    for item in list2:
        if item not in list1:
            list1.append(item)


def find_implementations(interface, recurse, abstract, result):
    """Find implementations of an interface or of one of its descendants and
    extend result with the classes found."""
    for item in MetaComponent.implementations:
        if (item['interface'] == interface and (abstract or not item['abstract'])):
            extend_unique(result, [item['class']])

    if recurse:
        subinterfaces = interface.__subclasses__()
        if subinterfaces:
            for i in subinterfaces:
                find_implementations(i, recurse, abstract, result)


class ComponentError(Exception):
    pass
