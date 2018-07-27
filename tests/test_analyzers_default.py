#! /usr/bin/env python

# Author : Thomas Fillon <thomas@parisson.com>
from unit_timeside import unittest, TestRunner
import numpy as np

import timeside.core
from timeside.plugins.decoder.file import FileDecoder
from timeside.core.tools.test_samples import samples
from jsonschema import Draft4Validator

import tempfile

class TestAnalyzers_parameters(unittest.TestCase):
    """Test analyzer parameters and schema specification"""

    def _perform_test(self, analyzer_cls, source_file):
        """Internal function that test analyzer schema and default parameters"""

        analyzer = analyzer_cls()
        self.assertEqual(analyzer.get_parameters(),
                         analyzer.get_parameters_default_from_argspec())

        analyzer.check_schema()


class TestAnalyzers_with_default(unittest.TestCase):
    """Test analyzer with default parameters"""

    def _perform_test(self, analyzer_cls, source_file):
        """Internal function that test if there is NaN in the results
        of a given analyzer"""
        decoder = FileDecoder(source_file)
        analyzer = analyzer_cls()
        pipe = (decoder | analyzer)
        pipe.run()
        for result in analyzer.results.values():
            if 'value' in result.data_object.keys():
                # Test for NaN
                self.assertFalse(np.any(np.isnan(result.data)),
                                 'NaN in %s data value' % result.name)
                # Test for Inf
                self.assertFalse(np.any(np.isinf(result.data)),
                                 'Inf in %s data value' % result.name)
        # Try to serialize as hdf5
        h5_file = tempfile.NamedTemporaryFile(suffix='.h5', delete=True)
        analyzer.results.to_hdf5(h5_file.name)

def _tests_factory(test_class, test_doc, list_analyzers, sources, skip_reasons={}):
    """Define a test for each analyzer provided in the list"""
    for analyzer in list_analyzers:
        for source_type, source_file in sources.items():
            def test_func_factory(analyzer):
                test_func = lambda self: self._perform_test(analyzer, source_file)
                test_func.__doc__ = test_doc % analyzer.__name__ + '_' + source_type
                return test_func

        test_func_name = "test_%s" % analyzer.__name__
        test_func = test_func_factory(analyzer)

        if analyzer.__name__ not in skip_reasons:
            setattr(test_class, test_func_name, test_func)
        else:  # Decorate with unittest.skip to skip test
            setattr(test_class, test_func_name,
                    unittest.skip(skip_reasons[analyzer.__name__])(test_func))

sources = {'mono': samples["C4_scale.wav"],
           'stereo': samples["sweep.mp3"]}
            
# Define test to skip and corresponding reasons
skip_reasons = {}
# For each analyzer in TimeSide, test default parameters and schema
_tests_factory(test_class=TestAnalyzers_parameters,
               test_doc="Test analyzer %s schema and default parameters",
               list_analyzers=timeside.core.processor.processors(timeside.core.api.IAnalyzer),
               sources={'mono': samples["C4_scale.wav"]},
               skip_reasons=skip_reasons)


# Define test to skip and corresponding reasons
skip_reasons = {  # 'IRITDiverg': 'IRIT_Diverg has to be fixed',
    #'IRITMusicSLN': 'IRITMusicSLN has to be fixed',
    #'IRITMusicSNB': 'IRITMusicSNB has to be fixed',
    'IRITSinging': 'IRITSingings has to be fixed',
    'IRITHarmoTracker': 'IRIT_HarmoTracker fails the stress test',
    'IRITHarmoCluster': 'IRIT_HarmoCluster fails the stress test',
    'LABRIInstru': 'LABRIInstru has to be fixed',
    'LABRIMultipitch': 'LABRIMultipitch has to be fixed',
    'VampSimpleHost': 'Vamp Simple Host become obsolete in favor of Vampy Host'
}

# For each analyzer in TimeSide, test with constant input
_tests_factory(test_class=TestAnalyzers_with_default,
               test_doc="Test analyzer %s with default parameters",
               list_analyzers=timeside.core.processor.processors(timeside.core.api.IAnalyzer),
               sources=sources,
               skip_reasons=skip_reasons)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
