# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2013 Parisson SARL

# This file is part of TimeSide.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author:
#   Thomas Fillon <thomas  at parisson.com>


def dict_to_hdf5(dict_like, h5group):
    """
    Save a dictionnary-like object inside a h5 file group
    """
    # Write attributes
    for key, value in dict_like.items():
        if value is not None:
            h5group.attrs[str(key)] = value


def dict_from_hdf5(dict_like, h5group):
    """
    Load a dictionnary-like object from a h5 file group
    """
    # Read attributes
    for name, value in h5group.attrs.items():
        dict_like[name] = value
