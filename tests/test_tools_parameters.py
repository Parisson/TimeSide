#! /usr/bin/env python
# -*- coding: utf-8 -*-

from unit_timeside import unittest, TestRunner
from timeside.tools.parameters import HasParam, HasTraits
from timeside.tools.parameters import Unicode, Int, Float, Range

import simplejson as json


class TestHasParam(unittest.TestCase):

    def setUp(self):
        class ParamClass(HasParam):
            class _Param(HasTraits):
                param1 = Unicode(desc='first or personal name',
                                 label='First Name')
                param2 = Int()
                param3 = Float()
                param4 = Range(low=0, high=10, value=3)

        self.param_dict = {"param1": "", "param2": 0, "param3": 0.0,
                           "param4": 3}
        self.has_param_cls = ParamClass()

    def test_get_parameters(self):
        "get_parameters method"
        param_json = self.has_param_cls.get_parameters()
        self.assertEqual(json.loads(param_json),
                         self.param_dict)

    def test_set_parameters(self):
        "set_parameters method"
        new_param_dict = {"param1": "plop", "param2": 7,
                          "param3": 0.5, "param4": 8}
        new_param_json = json.dumps(new_param_dict)
        # Set from dict
        self.has_param_cls.set_parameters(new_param_dict)
        param_json = self.has_param_cls.get_parameters()
        param_dict = json.loads(param_json)
        self.assertEqual(param_dict, new_param_dict)
        for name, value in new_param_dict.items():
            self.assertEqual(self.has_param_cls.__getattribute__(name), value)
        # set from JSON
        self.has_param_cls.set_parameters(new_param_json)
        param_json = self.has_param_cls.get_parameters()
        param_dict = json.loads(param_json)
        self.assertEqual(param_dict, new_param_dict)
        for name, value in new_param_dict.items():
            self.assertEqual(self.has_param_cls.__getattribute__(name), value)

    def test_param_view(self):
        "param_view method"
        view = self.has_param_cls.param_view()
        self.assertIsInstance(view, str)
        self.assertEqual(view,
                         ('{"param4": {"default": 3, "type": "range"}, '
                          '"param3": {"default": 0.0, "type": "float"}, '
                          '"param2": {"default": 0, "type": "int"}, '
                          '"param1": {"default": "", "type": "str"}}'))

    def test_setattr_on_traits(self):
        "Set a trait attribute"
        name = 'param1'
        value = 'a_trait'

        self.has_param_cls.__setattr__(name, value)

        # check that 'has_param'  regular attribute has been set
        set_value = self.has_param_cls.__getattribute__(name)
        self.assertEqual(set_value, value)
        # check that 'has_param' traits has been set
        _parameters = self.has_param_cls.__getattribute__('_parameters')
        set_parameters_value = _parameters.__getattribute__(name)
        self.assertEqual(set_parameters_value, value)

    def test_setattr_on_non_traits(self):
        "Set a regular attribute (non traits)"
        name = 'param5'
        value = 'not_a_trait'
        self.has_param_cls.__setattr__(name, value)

        # check that 'has_param'  regular attribute has been set
        set_value = self.has_param_cls.__getattribute__(name)
        self.assertEqual(set_value, value)

        # check that no such traits has been set
        _parameters = self.has_param_cls.__getattribute__('_parameters')
        self.assertRaises(AttributeError, _parameters.__getattribute__, name)
        self.assertNotIn(name, _parameters.trait_names())

    def test_validate_True(self):
        "Validate parameters with good format"
        # Validate from dict
        self.assertEqual(self.param_dict,
                         self.has_param_cls.validate_parameters(
                             self.param_dict))
        # Validate from JSON
        param_json = json.dumps(self.param_dict)
        self.assertEqual(self.param_dict,
                         self.has_param_cls.validate_parameters(param_json))

    def test_validate_False(self):
        "Validate parameters with bad format"
        bad_param = {"param1": "", "param2": 0, "param3": 0.0,
                     "param4": 3.3}  # Param4 is a Float (it should be a int)
        # Validate from dict
        self.assertRaises(ValueError, self.has_param_cls.validate_parameters,
                          bad_param)
        # Validate from JSON
        bad_param_json = json.dumps(bad_param)
        self.assertRaises(ValueError, self.has_param_cls.validate_parameters,
                          bad_param_json)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
