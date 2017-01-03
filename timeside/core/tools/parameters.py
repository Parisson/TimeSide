# -*- coding: utf-8 -*-

#
# Copyright (c) 2007-2016 Parisson SARL

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


import jsonschema
import inspect
import functools
import decorator
from copy import deepcopy

TRAIT_TYPES = {Unicode: 'str',
               Int: 'int',
               Float: 'float',
               Range: 'range',
               Enum: 'enum',
               ListUnicode: 'list of str',
               List: 'list'}


@decorator.decorator
def store_parameters(__init__func, *args):
    self = args[0]
    argsname, _, _, _ = inspect.getargspec(__init__func)

    parameters = {key: value
                  for key, value in zip(argsname, args)}
    del parameters['self']
    __init__func(*args)
    self._parameters = parameters


def DEFAULT_SCHEMA():
    return {"type": "object",
            "properties": {},
            "$schema": "http://json-schema.org/schema#"}


class HasParam(object):
    """Abstract class for handling parameters
    """
    _schema = None

    @classmethod
    def get_parameters_schema(cls):
        if cls._schema is None:
            cls._schema = DEFAULT_SCHEMA()
        argspec_schema = cls.schema_from_argspec()['properties']
        if argspec_schema and cls._schema['properties']:
            for key in argspec_schema:
                if key in cls._schema['properties']:
                    argspec_schema[key].update(cls._schema['properties'][key])
        cls._schema['properties'] = argspec_schema

        return cls._schema

    def get_parameters(self):
        return self._parameters

    @classmethod
    def get_parameters_default_from_argspec(cls):
        args, _, _, defaults = inspect.getargspec(cls.__init__)
        args.remove('self')  # remove 'self' from arguments list
        if defaults:
            return {arg: default for arg, default
                    in zip(args[-len(defaults):], defaults)}
        else:
            return {}

    @classmethod
    def get_parameters_default(cls):
        schema = cls.get_parameters_schema()
        return {key: schema['properties'][key]['default']
                for key in schema['properties']}

    @classmethod
    def validate_parameters(cls, parameters, schema=None):
        """Validate parameters format against schema specification
        Raises:
          - ValidationError if the instance is invalid
          - SchemaError if the schema itself is invalid
        """
        if schema is None:
            schema = cls.get_parameters_schema()
        jsonschema.validate(parameters, schema)

    @classmethod
    def schema_from_argspec(cls):
        default_param = cls.get_parameters_default_from_argspec()
        schema = DEFAULT_SCHEMA()
        for key, value in default_param.items():
            if isinstance(value, basestring):
                val_type = "string"
            elif isinstance(value, bool):
                val_type = "boolean"  # warning : boolean is an int instance
            elif isinstance(value, float):
                val_type = "number"
            elif isinstance(value, (int, long)):
                val_type = "integer"
            elif isinstance(value, list):
                val_type = "array"
            else:
                val_type = "Unknown_type"
            schema['properties'].update({key: {"type": val_type,
                                               "default": value}})
        return schema

    @classmethod
    def check_schema(cls):
        """Validate the class schema against the Draft 4 meta-schema"""
        jsonschema.Draft4Validator.check_schema(cls.get_parameters_schema())

if __name__ == "__main__":
    import doctest
    doctest.testmod()
