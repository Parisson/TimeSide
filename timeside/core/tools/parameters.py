# -*- coding: utf-8 -*-

#
# Copyright (c) 2007-2014 Parisson SARL

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

# Authors:
#   Thomas Fillon <thomas  at parisson.com>


from traits.api import HasTraits, Unicode, Int, Float, Range, Enum
from traits.api import ListUnicode, List, Tuple
from traits.api import TraitError

import simplejson as json


TRAIT_TYPES = {Unicode: 'str',
               Int: 'int',
               Float: 'float',
               Range: 'range',
               Enum: 'enum',
               ListUnicode: 'list of str',
               List: 'list'}


class HasParam(object):
    """
    >>> class ParamClass(HasParam):
    ...    class _Param(HasTraits):
    ...        param1 = Unicode(desc='first or personal name',
    ...                      label='First Name')
    ...        param2 = Int()
    ...        param3 = Float()
    ...        param4 = Range(low=0, high=10, value=3)
    >>>
    >>> p = ParamClass()
    >>> param_json = p.get_parameters()
    >>> print param_json
    {"param4": 3, "param3": 0.0, "param2": 0, "param1": ""}
    >>> new_param_json = '{"param1": "plop", "param2": 7, "param3": 0.5, \
    "param4": 8}'
    >>> p.set_parameters(new_param_json)
    >>> print p.get_parameters()
    {"param4": 8, "param3": 0.5, "param2": 7, "param1": "plop"}
    >>> v = p.param_view()
    >>> print v
    {"param4": {"default": 3, "type": "range"}, \
"param3": {"default": 0.0, "type": "float"}, \
"param2": {"default": 0, "type": "int"}, \
"param1": {"default": "", "type": "str"}}
    """
    class _Param(HasTraits):
        pass

    def __init__(self):
        super(HasParam, self).__init__()
        self._parameters = self._Param()

    def __setattr__(self, name, value):
        if name is '_parameters':
            super(HasParam, self).__setattr__(name, value)
        elif name in self._parameters.trait_names():
            self._parameters.__setattr__(name, value)
            # Copy attributes as a regular attribute at class level
            _value = self._parameters.__getattribute__(name)
            super(HasParam, self).__setattr__(name, _value)
        else:
            super(HasParam, self).__setattr__(name, value)

    def get_parameters(self):
        list_traits = self._parameters.editable_traits()
        param_dict = self._parameters.get(list_traits)
        return json.dumps(param_dict)

    def set_parameters(self, parameters):
        if isinstance(parameters, basestring):
            self.set_parameters(json.loads(parameters))
        else:
            for name, value in parameters.items():
                self.__setattr__(name, value)

    def validate_parameters(self, parameters):
        """Validate parameters format against Traits specification
        Input can be either a dictionary or a JSON string
        Returns the validated parameters or raises a ValueError"""

        if isinstance(parameters, basestring):
            return self.validate_parameters(json.loads(parameters))
        # Check key against traits name
        traits_name = self._parameters.editable_traits()
        for name in parameters:
            if name not in traits_name:
                raise KeyError(name)

        try:
            valid_params = {name: self._parameters.validate_trait(name, value)
                            for name, value in parameters.items()}
        except TraitError as e:
            raise ValueError(str(e))

        return valid_params

    def param_view(self):
        list_traits = self._parameters.editable_traits()
        view = {}
        for key in list_traits:
            trait_type = self._parameters.trait(key).trait_type.__class__
            default = self._parameters.trait(key).default
            d = {'type': TRAIT_TYPES[trait_type],
                 'default': default}
            view[key] = d
        return json.dumps(view)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
