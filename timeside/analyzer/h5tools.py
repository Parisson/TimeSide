# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2013 Parisson SARL

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

# Author:
#   Thomas Fillon <thomas  at parisson.com>


def dict_to_hdf5(dict_like, h5group):
    """
    Save a dictionnary-like object inside a h5 file group
    """
    # Write attributes
    attrs = dict_like.keys()
    for name in attrs:
        if dict_like[name] is not None:
            h5group.attrs[str(name)] = dict_like[name]


def dict_from_hdf5(dict_like, h5group):
    """
    Load a dictionnary-like object from a h5 file group
    """
    # Read attributes
    for name, value in h5group.attrs.items():
        dict_like[name] = value
