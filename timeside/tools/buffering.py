# -*- coding: utf-8 -*-

# Copyright (c) 2014 Parisson SARL
# Copyright (c) 2014 Thomas Fillon <thomas@parisson.com>

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
#
# Author : Thomas Fillon <thomas@parisson.com>

import tables
from tempfile import NamedTemporaryFile


class BufferTable(object):
    def __init__(self, array_names=None):
        self._tempfile = NamedTemporaryFile(mode='w', suffix='.h5',
                                            prefix='ts_buf_',
                                            delete=True)
        self.fileh = tables.openFile(self._tempfile.name, mode='w')

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

    #def __set_item__(self, name, value):
    #    self.fileh.root.__setattr__(name, value)

    def append(self, name, new_array):
        try:
            self.fileh.root.__getattr__(name).append([new_array])
        except tables.exceptions.NoSuchNodeError:
            if name not in self.array_names:
                self.array_names.append(name)
             # The following is compatible with pytables 3 only
             #self.fileh.create_earray(where=self.fileh.root,
             #                         name=name,
             #                         obj=[new_array])
            atom = tables.Atom.from_dtype(new_array.dtype)
            if len(new_array.shape) > 1:
                shape = (0, new_array.shape[1])
            else:
                shape = (0,)
            self.fileh.createEArray(where=self.fileh.root,
                                    name=name,
                                    atom=atom,
                                    shape=shape)
            self.append(name, new_array)

    def close(self):
        for name in self.array_names:
            self.fileh.removeNode(self.fileh.root, name)
        self.fileh.close()
        self._tempfile.close()
