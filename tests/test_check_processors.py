#! /usr/bin/env python
# -*- coding: utf-8 -*-


# Author : Thomas Fillon <thomas at parisson.com>


from unit_timeside import unittest, TestRunner
import timeside.core
import inspect

#@unittest.skip


class TestCheckProcessorsParam(unittest.TestCase):

    def _check_param_test(self, processor_cls):
        """Internal function that test if a given processor
        has schema parameters as __init__ arguments"""

        argspec = inspect.getargspec(processor_cls.__init__)
        argspec.args.remove('self')  # remove 'self' from arguments list

        # print argspec.args
        parameters = processor_cls.get_parameters_schema()['properties'].keys()
        # print traits_parameters
        self.assertTrue(set(parameters).issubset(argspec.args))


def _tests_factory(test_class, test_doc, list_processors, skip_reasons={}):
    """Define a test for each analyzer provided in the list"""
    for proc in list_processors:

        def test_func_factory(proc):
            test_func = lambda self: self._check_param_test(proc)
            test_func.__doc__ = test_doc % proc.__name__
            return test_func

        test_func_name = "test_%s" % proc.__name__
        test_func = test_func_factory(proc)

        if proc.__name__ not in skip_reasons:
            setattr(test_class, test_func_name, test_func)
        else:  # Decorate with unittest.skip to skip test
            setattr(test_class, test_func_name,
                    unittest.skip(skip_reasons[proc.__name__])(test_func))


# Define test to skip and corresponding reasons
skip_reasons = {}

# For each processor in TimeSide, test with constant input
list_processors = timeside.core.processor.processors(timeside.core.api.IAnalyzer)

_tests_factory(test_class=TestCheckProcessorsParam,
               test_doc="Check processor %s parameters validity as Traits",
               list_processors=list_processors,
               skip_reasons=skip_reasons)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
