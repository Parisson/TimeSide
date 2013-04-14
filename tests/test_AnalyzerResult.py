#! /usr/bin/env python

from unit_timeside import *
from timeside.decoder import *
from timeside.analyzer.core import *

verbose = 0

class TestAnalyzerResult(TestCase):
    """ test AnalyzerResult """

    def setUp(self):
        self.result = AnalyzerResult(id = "foo_bar", name = "Foo bar", unit = "foo")

    def testOnFloat(self):
        "float result"
        self.result.value = 1.2

    def testOnInt(self):
        "integer result"
        self.result.value = 1

    def testOnList(self):
        "list result"
        self.result.value = [1., 2.]

    def testOnString(self):
        "string result"
        self.result.value = "hello"

    def testOnListOfString(self):
        "list of strings result"
        self.result.value = ["hello", "hola"]

    def testOnListOfList(self):
        "list of lists result"
        self.result.value = [[0,1], [0,1,2]]

    def tearDown(self):
        pass

class TestAnalyzerResultNumpy(TestAnalyzerResult):
    """ test AnalyzerResult numpy serialize """

    def tearDown(self):
        results = [self.result]
        r_numpy = data_to_numpy(results, '/tmp/t.npy')
        d_numpy = data_from_numpy('/tmp/t.npy')
        if verbose:
            print '%15s' % 'from numpy:',
            print d_numpy
        for i in range(len(d_numpy)):
            self.assertEquals(d_numpy[i], results[i])

class TestAnalyzerResultYaml(TestAnalyzerResult):
    """ test AnalyzerResult yaml serialize """
    def tearDown(self):
        results = [self.result]
        r_yaml = data_to_yaml(results)
        if verbose:
            print 'to yaml:'
            print r_yaml
        d_yaml = data_from_yaml(r_yaml)
        if verbose:
            print '%15s' % 'from yaml:',
            print d_yaml
        for i in range(len(d_yaml)):
            self.assertEquals(results[i], d_yaml[i])

class TestAnalyzerResultXml(TestAnalyzerResult):
    """ test AnalyzerResult xml serialize """
    def tearDown(self):
        results = [self.result]
        r_xml = data_to_xml(results)
        if verbose:
            print 'to xml:'
            print r_xml

        d_xml = data_from_xml(r_xml)
        if verbose:
            print '%15s' % 'from xml:',
            print d_xml

        for i in range(len(d_xml)):
            self.assertEquals(d_xml[i], results[i])

class TestAnalyzerResultJson(TestAnalyzerResult):
    """ test AnalyzerResult json serialize """
    def tearDown(self):
        results = [self.result]
        r_json = data_to_json(results)
        if verbose:
            print 'to json:'
            print r_json

        d_json = data_from_json(r_json)
        if verbose:
            print d_json
            print '%15s' % 'from yaml:',

        for i in range(len(d_json)):
            self.assertEquals(d_json[i], results[i])

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
