#! /usr/bin/env python

# Author : Thomas Fillon <thomas@parisson.com>


from unit_timeside import unittest, TestRunner
import timeside
import numpy as np


class TestAnalyzers_with_zeros(unittest.TestCase):
    """Stress test for analyzer with null input"""

    def setUp(self):
        samplerate = 16000  # LimsiSad require Fs = 16000 Hz
        duration = 10
        samples = np.zeros((duration * samplerate, 1))
        decoder_cls = timeside.core.get_processor('array_decoder')
        self.decoder = decoder_cls(samples, samplerate=samplerate)

    def _perform_test(self, analyzer_cls):
        """Internal function that test if there is NaN in the results
        of a given analyzer"""

        analyzer = analyzer_cls()
        pipe = (self.decoder | analyzer)
        pipe.run()
        for key, result in analyzer.results.items():
            if 'value' in result.data_object.keys():
                # Test for NaN
                print result.data_mode
                print result.data.dtype, result.data 
                self.assertFalse(np.any(np.isnan(result.data)),
                                 'NaN in %s data value' % result.name)
                # Test for Inf
                self.assertFalse(np.any(np.isinf(result.data)),
                                 'Inf in %s data value' % result.name)


class TestAnalyzers_withDC(TestAnalyzers_with_zeros):
    """Stress test for analyzer with constant input"""

    def setUp(self):
        samplerate = 16000  # LimsiSad require Fs = 16000 Hz
        duration = 10
        samples = -1000 * np.ones((duration * samplerate, 1))
        decoder_cls = timeside.core.get_processor('array_decoder')
        self.decoder = decoder_cls(samples, samplerate=samplerate)


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
skip_reasons = {'VampSimpleHost': ('VampSimpleHost bypasses the decoder '
                                   'and requires a file input'),

                'VampTempo': ' VampTemo has no output for stress signal',
                'IRITDiverg': 'IRIT_Diverg fails the stress test',
                'IRITSinging': 'IRITSingings has to be fixed',
                'IRITHarmoTracker': 'IRIT_HarmoTracker fails the stress test',
                'IRITHarmoCluster': 'IRIT_HarmoCluster fails the stress test',
                'IRITTempogram': 'IRIT_Tempogram fails the stress test (because of Irit Diverg)',
                'IRITMusicSLN': 'IRITMusicSLN fails the stress test',
                'IRITMusicSNB': 'IRITMusicSNB fails the stress test'}


# For each analyzer in TimeSide, test with constant input
_tests_factory(test_class=TestAnalyzers_withDC,
               test_doc="Stress test for %s",
               list_analyzers=timeside.core.processor.processors(timeside.core.api.IAnalyzer),
               skip_reasons=skip_reasons)

# For each analyzer in TimeSide, test with null input
_tests_factory(test_class=TestAnalyzers_with_zeros,
               test_doc="Stress test for %s",
               list_analyzers=timeside.core.processor.processors(timeside.core.api.IAnalyzer),
               skip_reasons=skip_reasons)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
