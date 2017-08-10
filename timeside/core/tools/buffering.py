# -*- coding: utf-8 -*-

# Copyright (c) 2014 Parisson SARL
# Copyright (c) 2014 Thomas Fillon <thomas@parisson.com>

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
#
# Author : Thomas Fillon <thomas@parisson.com>

import tables
from tempfile import NamedTemporaryFile
import numpy as np


class BufferTable(object):

    def __init__(self, array_names=None):
        self._tempfile = NamedTemporaryFile(mode='w', suffix='.h5',
                                            prefix='ts_buf_',
                                            delete=True)
        self.fileh = tables.open_file(self._tempfile.name, mode='w')

        if not array_names:
            array_names = []
        if isinstance(array_names, list):
            self.array_names = array_names
        else:
            self.array_names = [array_names]
        for name in array_names:
            if not isinstance(name, basestring):
                raise(TypeError, 'String argument require in array_names')

    def __getitem__(self, name):
        return self.fileh.root.__getattr__(name)

    # def __set_item__(self, name, value):
    #    self.fileh.root.__setattr__(name, value)

    def append(self, name, new_array):
        try:
            if new_array.shape:
                self.fileh.root.__getattr__(name).append(new_array[np.newaxis,
                                                                   :])
            else:
                self.fileh.root.__getattr__(name).append([new_array])
        except tables.exceptions.NoSuchNodeError:
            if name not in self.array_names:
                self.array_names.append(name)
            # The following is compatible with pytables 3 only
            self.fileh.create_earray(where=self.fileh.root,
                                     name=name,
                                     obj=[new_array])
            # Pytables 2 compatible version
            # atom = tables.Atom.from_dtype(new_array.dtype)
            # dim_list = [0]
            # dim_list.extend([dim for dim in new_array.shape])
            # shape = tuple(dim_list)

            # self.fileh.create_earray(where=self.fileh.root,
            #                         name=name,
            #                         atom=atom,
            #                         shape=shape)
            self.append(name, new_array)

    def close(self):
        for name in self.array_names:
            self.fileh.remove_node(self.fileh.root, name)
        self.fileh.close()
        self._tempfile.close()
