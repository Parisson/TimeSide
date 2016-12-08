#! /usr/bin/env python
# -*- coding: utf-8 -*-

from unit_timeside import unittest, TestRunner
from timeside.core.tools.parameters import HasParam, HasTraits
from timeside.core.tools.parameters import Unicode, Int, Float, Range
from timeside.core.tools.parameters import store_parameters
from timeside.core.tools.parameters import DEFAULT_SCHEMA

import simplejson as json
from jsonschema import ValidationError


class TestHasParam(unittest.TestCase):

    def setUp(self):
        self.schema = DEFAULT_SCHEMA()
        self.schema['properties'].update(
            {"param1": {"type": "string", "default": "default"},
             "param2": {"type": "integer", "default": 3},
             "param3": {"type": "number", "default": 5.9},
             "param4": {"type": "integer", "default": 33,
                        "minimum": 0,
                        "maximum": 100, },
             "param5": {"type": "boolean", "default": True}}
        )

        self.param_default = {"param1": "default",
                              "param2": 3,
                              "param3": 5.9,
                              "param4": 33,
                              "param5": True}

        class ParamClass(HasParam):
            _schema = self.schema

            @store_parameters
            def __init__(self,
                         param1=self.param_default["param1"],
                         param2=self.param_default["param2"],
                         param3=self.param_default["param3"],
                         param4=self.param_default["param4"],
                         param5=self.param_default["param5"]):
                super(ParamClass, self).__init__()

        self.param_dict = {"param1": "", "param2": 0, "param3": 0.0,
                           "param4": 3, "param5": False}
        self.has_param_cls = ParamClass

    def test_get_parameters(self):
        "get_parameters method"
        cls_instance = self.has_param_cls(**self.param_dict)
        param_dict = cls_instance.get_parameters()
        self.assertEqual(param_dict,
                         self.param_dict)

    def test_get_parameters_default(self):
        "get_parameters method with default values"
        cls_instance = self.has_param_cls()
        param_dict = cls_instance.get_parameters()
        self.assertDictEqual(param_dict,
                             self.param_default)
        self.assertDictEqual(self.param_default,
                             cls_instance.get_parameters_default())

    def test_get_parameters_schema(self):
        "get_parameters schema"

        self.assertEqual(self.schema,
                         self.has_param_cls.get_parameters_schema())

        incomplete_schema = self.schema
        del incomplete_schema['properties']['param1']['default']
        del incomplete_schema['properties']['param2']['default']
        del incomplete_schema['properties']['param3']
        del incomplete_schema['properties']['param5']

        has_param_cls = self.has_param_cls()
        has_param_cls._schema = incomplete_schema
        self.assertEqual(self.schema,
                         has_param_cls.get_parameters_schema())

    def test_validate_True(self):
        "Validate parameters with good format"
        # Validate from dict
        cls_instance = self.has_param_cls()
        cls_instance.validate_parameters(self.param_dict)

    def test_validate_False(self):
        "Validate parameters with bad format"
        bad_param = {"param1": "good", "param2": 0, "param3": 0.0,
                     "param4": 102}  # Param4 should an integer in range 0-100
        cls_instance = self.has_param_cls()
        # Validate from dict
        self.assertRaises(ValidationError, cls_instance.validate_parameters,
                          bad_param)

    def test_schema_from_argspec(self):
        """
        Get schema from class __init__ arguments
        """
        schema = self.schema.copy()
        for param in schema['properties']:
            keys_to_delete = [key for key in schema['properties'][param]
                              if not key in ['type', 'default']]
            for key in keys_to_delete:
                del schema['properties'][param][key]
        self.assertDictEqual(self.has_param_cls.schema_from_argspec(),
                             schema)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
