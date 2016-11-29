# -*- coding: utf-8 -*-

#
# Copyright (c) 2007-2014 Parisson SARL

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

# Authors:
#   Thomas Fillon <thomas  at parisson.com>


from traits.api import HasTraits, Unicode, Int, Float, Range, Enum, Bool
from traits.api import ListUnicode, List, Tuple
from traits.api import TraitError

import inspect
import simplejson as json
import jsonschema

TRAIT_TYPES = {Unicode: 'str',
               Int: 'int',
               Float: 'float',
               Range: 'range',
               Enum: 'enum',
               ListUnicode: 'list of str',
               List: 'list'}


class HasParam(object):
    """Abstract class for handling parameters
    """
    _schema = {"type": "object",
               "properties": {}
               }

    @classmethod
    def get_parameters_schema(cls):
        # TODO : add default values
        return cls._schema

    def get_parameters(self, schema=None):
        if schema is None:
            schema = self._schema

        try:
            keys = schema["properties"].keys()
        except KeyError:
            keys = schema.keys()

        return {key: self.__getattribute__(key)
                for key in keys}

    def validate_parameters(self, parameters, schema=None):
        """Validate parameters format against schema specification
        Raises:	
          - ValidationError if the instance is invalid
          - SchemaError if the schema itself is invalid
        """
        if schema is None:
            schema = self._schema
        jsonschema.validate(parameters, schema)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
