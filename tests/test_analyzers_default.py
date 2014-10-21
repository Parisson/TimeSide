#! /usr/bin/env python

# Author : Thomas Fillon <thomas@parisson.com>


from unit_timeside import unittest, TestRunner
import timeside
from timeside.decoder.file import FileDecoder
import numpy as np
from timeside.tools.data_samples import samples as ts_samples


class TestAnalyzers_with_default(unittest.TestCase):
    """Test analyzer with default parameters"""

    def setUp(self):
        source = ts_samples["C4_scale.wav"]

        self.decoder = FileDecoder(source)

    def _perform_test(self, analyzer_cls):
        """Internal function that test if there is NaN in the results
        of a given analyzer"""

        analyzer = analyzer_cls()
        pipe = (self.decoder | analyzer)
        pipe.run()
        for key, result in analyzer.results.items():
            if 'value' in result.data_object.keys():
                # Test for NaN
                self.assertFalse(np.any(np.isnan(result.data)),
                                 'NaN in %s data value' % result.name)
                # Test for Inf
                self.assertFalse(np.any(np.isinf(result.data)),
                                 'Inf in %s data value' % result.name)


def _tests_factory(test_class, test_doc, list_analyzers, skip_reasons={}):
    """Define a test for each analyzer provided in the list"""
    for analyzer in list_analyzers:

        def test_func_factory(analyzer):
            test_func = lambda self: self._perform_test(analyzer)
            test_func.__doc__ = test_doc % analyzer.__name__
            return test_func

        test_func_name = "test_%s" % analyzer.__name__
        test_func = test_func_factory(analyzer)

        if analyzer.__name__ not in skip_reasons:
            setattr(test_class, test_func_name, test_func)
        else:  # Decorate with unittest.skip to skip test
            setattr(test_class, test_func_name,
                    unittest.skip(skip_reasons[analyzer.__name__])(test_func))


# Define test to skip and corresponding reasons
skip_reasons = {}

# For each analyzer in TimeSide, test with constant input
_tests_factory(test_class=TestAnalyzers_with_default,
               test_doc="Test analyzer %s with default parameters",
               list_analyzers=timeside.core.processors(timeside.api.IAnalyzer),
               skip_reasons=skip_reasons)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
