#! /usr/bin/env python
from __future__ import division

from unit_timeside import unittest, TestRunner
import timeside
from timeside.core.tools.test_samples import samples
from tempfile import NamedTemporaryFile
import os

PLOT = False


class Test_graphers_analyzers(unittest.TestCase):
    """ test Graphers from analyzers"""

    def setUp(self):
        source = samples["C4_scale.wav"]
        decoder_cls = timeside.core.get_processor('file_decoder')
        self.decoder = decoder_cls(uri=source)

    def _perform_test(self, grapher_cls):
            """Internal function that test grapher for a given analyzer"""
            grapher = grapher_cls()
            pipe = (self.decoder | grapher)
            pipe.run()

            if PLOT:
                grapher.render().show()
            else:
                self.temp_file = NamedTemporaryFile(suffix='.png',
                                                    delete=False)
                grapher.render(self.temp_file.name)

    def tearDown(self):
        # Clean-up : delete temp file
        if not PLOT:
            os.unlink(self.temp_file.name)


def _tests_factory(grapher_analyzers):
    for grapher in grapher_analyzers:

        def _test_func_factory(grapher):
            test_func = lambda self: self._perform_test(grapher)
            test_func.__doc__ = 'Test Graphers: %s' % grapher.name()
            return test_func

        test_func_name = "test_%s" % grapher.name()
        test_func = _test_func_factory(grapher)

        setattr(Test_graphers_analyzers, test_func_name, test_func)

list_graphers = timeside.core.processor.processors(timeside.core.api.IGrapher)
from timeside.core.grapher import DisplayAnalyzer
grapher_analyzers = [grapher for grapher in list_graphers
                     if grapher.__base__ == DisplayAnalyzer]

_tests_factory(grapher_analyzers)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
