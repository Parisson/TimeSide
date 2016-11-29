#! /usr/bin/env python
# -*- coding: utf-8 -*-

from unit_timeside import unittest, TestRunner
from timeside.core.tools.parameters import HasParam, HasTraits
from timeside.core.tools.parameters import Unicode, Int, Float, Range

import simplejson as json
from jsonschema import ValidationError


class TestHasParam(unittest.TestCase):

    def setUp(self):
        self.schema = {"type": "object",
                       "properties": {
                           "param1": {"type": "string"},
                           "param2": {"type": "integer"},
                           "param3": {"type": "number"},
                           "param4": {"type": "integer",
                                      "minimum": 0,
                                      "maximum": 100,
                                      },
                           "param5": {"type": "boolean"}
                       }
                       }
        self.param_default = {"param1": "default",
                              "param2": 3,
                              "param3": 5.9,
                              "param4": 33,
                              "param5": True}

        class ParamClass(HasParam):
            _schema = self.schema

            def __init__(self,
                         param1=self.param_default["param1"],
                         param2=self.param_default["param2"],
                         param3=self.param_default["param3"],
                         param4=self.param_default["param4"],
                         param5=self.param_default["param5"]):
                super(ParamClass, self).__init__()
                self.param1 = param1
                self.param2 = param2
                self.param3 = param3
                self.param4 = param4
                self.param5 = param5

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
        self.assertEqual(param_dict,
                         self.param_default)

        def test_get_parameters_schema(self):
            "get_parameters schema"

            self.assertEqual(self.schema,
                             self.has_param_cls.get_parameters_schema())

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


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
