#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
from timeside.analyzer.core import AnalyzerResult, AnalyzerResultContainer
from timeside import __version__
import numpy as np
from math import pi


verbose = 0


class TestAnalyzerResult(unittest.TestCase):
    """ test AnalyzerResult """

    def setUp(self):
        self.result = AnalyzerResult.factory(data_mode='value',
                                             time_mode='framewise')

        from datetime import datetime
        res_date = datetime.now().replace(microsecond=0).isoformat(' ')
        self.result.id_metadata = dict(date=res_date,
                                       version=__version__,
                                       author='TimeSide',
                                       id="foo_bar",
                                       name="Foo bar",
                                       unit="foo")
        self.result.audio_metadata = dict(uri='Foo.wav',
                                          start=0, duration=20,
                                          channels=2)

    def tearDown(self):
        pass

# Get good and bad types for AnalyzerResult.data_object.data.value
from timeside.analyzer.core import numpy_data_types as good_dtypes
good_numpy_data_types = [str(dtype)[13:-2] for dtype in good_dtypes]
bad_numpy_data_types = [
    # not understood by json or yaml
    'float128',
    # Not supported by h5py for version < 2.2
    'float16',
    # complex can not be serialized in json
    'complex256',
    'complex128',
    'complex64',
    # ?
    'datetime64',
    'timedelta64',
    'unicode_',
    'string_'
    ]


class TestAnalyzerResultBadType(TestAnalyzerResult):
    """ test AnalyzerResult on bad numpy data type"""

    def method(self, numpy_data_type):
        try:
            data = getattr(np, numpy_data_type)(pi)
        except ValueError:
            data = getattr(np, numpy_data_type)()

        self.assertRaises(TypeError,
                          self.result.data_object.__setattr__,
                          'value', data)

    @classmethod
    def add_method(cls, numpy_data_type):
        test_method = lambda self: self.method(numpy_data_type)
        test_method.__name__ = 'testOnNumpy_%s' % numpy_data_type
        test_method.__doc__ = 'TypeError on numpy %s' % numpy_data_type
        setattr(cls, test_method.__name__, test_method)

# Add tests for each type in bad_numpy_data_types
for numpy_data_type in bad_numpy_data_types:
    TestAnalyzerResultBadType.add_method(numpy_data_type)


class TestAnalyzerResultGoodType(TestAnalyzerResult):
    """ test AnalyzerResult on good numpy data type"""
    def testOnFloat(self):
        "float result"
        self.result.data_object.value = 1.2

    def testOnInt(self):
        "integer result"
        self.result.data_object.value = 1

    def testOnList(self):
        "list result"
        self.result.data_object.value = [1., 2.]

    @unittest.skip("String have to be handled through label metadata")
    def testOnString(self):
        "string result"
        self.result.data_object.value = "hello"

    @unittest.skip("String have to be handled through label metadata")
    def testOnListOfString(self):
        "list of strings result"
        self.result.data_object.value = ["hello", "hola"]

    def testOnListOfList(self):
        "list of lists result"
        self.result.data_object.value = [[0, 1], [0, 1, 2]]

    def testOnNumpyVectorOfFloat(self):
        "numpy vector of float"
        self.result.data_object.value = np.ones(2, dtype='float') * pi

    def testOnNumpy2DArrayOfFloat64(self):
        "numpy 2d array of float64"
        self.result.data_object.value = np.ones([2, 3], dtype='float64') * pi

    def testOnNumpy3DArrayOfInt32(self):
        "numpy 3d array of int32"
        self.result.data_object.value = np.ones([2, 3, 2], dtype='int32')

    @unittest.skip("String have to be handled through label metadata")
    def testOnNumpyArrayOfStrings(self):
        "numpy array of strings"
        self.result.data_object.value = np.array(['hello', 'hola'])

    def testOnEmptyList(self):
        "empty list"
        self.result.data_object.value = []

    def testOnNone(self):
        "None"
        self.result.data_object.value = None

    @unittest.skip("String have to be handled through label metadata")
    def testOnUnicode(self):
        "Unicode"
        self.result.data_object.value = u'\u0107'

    def method(self, numpy_data_type):
        """Good numpy data type"""
        self.result.data_object.value = getattr(np, numpy_data_type)(pi)

    @classmethod
    def add_method(cls, numpy_data_type):
        test_method = lambda self: self.method(numpy_data_type)
        test_method.__name__ = 'testOnNumpy_%s' % numpy_data_type
        test_method.__doc__ = 'Support numpy %s' % numpy_data_type
        setattr(cls, test_method.__name__, test_method)

# Add tests for each type in good_numpy_data_types
for numpy_data_type in good_numpy_data_types:
    TestAnalyzerResultGoodType.add_method(numpy_data_type)


class TestAnalyzerResultNumpy(TestAnalyzerResultGoodType):
    """ test AnalyzerResult numpy serialize """

    def tearDown(self):
        results = AnalyzerResultContainer([self.result])
        results.to_numpy('/tmp/t.npy')
        d_numpy = results.from_numpy('/tmp/t.npy')
        if verbose:
            print '%15s' % 'from numpy:',
            print d_numpy
        self.assertEqual(d_numpy, results)


class TestAnalyzerResultHdf5(TestAnalyzerResultGoodType):
    """ test AnalyzerResult hdf5 serialize """

    def tearDown(self):
        results = AnalyzerResultContainer([self.result])
        results.to_hdf5('/tmp/t.h5')
        res_hdf5 = results.from_hdf5('/tmp/t.h5')
        if verbose:
            print '%15s' % 'from hdf5:',
            print res_hdf5
        self.assertEqual(results, res_hdf5)


class TestAnalyzerResultYaml(TestAnalyzerResultGoodType):
    """ test AnalyzerResult yaml serialize """
    def tearDown(self):
        results = AnalyzerResultContainer(self.result)
        r_yaml = results.to_yaml()
        if verbose:
            print 'to yaml:'
            print r_yaml
        d_yaml = results.from_yaml(r_yaml)
        if verbose:
            print '%15s' % 'from yaml:',
            print d_yaml
        #for i in range(len(d_yaml)):
        self.assertEqual(results, d_yaml)


class TestAnalyzerResultXml(TestAnalyzerResultGoodType):
    """ test AnalyzerResult xml serialize """
    def tearDown(self):
        results = AnalyzerResultContainer([self.result])
        r_xml = results.to_xml()
        if verbose:
            print 'to xml:'
            print r_xml

        d_xml = results.from_xml(r_xml)
        if verbose:
            print '%15s' % 'from xml:',
            print d_xml

        #for i in range(len(d_xml)):
        self.assertEqual(d_xml, results)


class TestAnalyzerResultJson(TestAnalyzerResultGoodType):
    """ test AnalyzerResult """
    def tearDown(self):
        results = AnalyzerResultContainer([self.result])
        try:
            r_json = results.to_json()
        except TypeError:
            print('TYPE ERROR IN JSON')
        if verbose:
            print 'to json:'
            print r_json

        d_json = results.from_json(r_json)
        if verbose:
            print d_json
            print '%15s' % 'from json:',

        #for i in range(len(d_json)):
        self.assertEqual(d_json, results)


class TestAnalyzerResultAsDict(TestAnalyzerResultGoodType):
    """ test AnalyzerResult as Dictionnary"""

    def tearDown(self):

        self.assertIsInstance(self.result.as_dict(), dict)
        self.assertItemsEqual(self.result.keys() + ['data_mode', 'time_mode'],
                              self.result.as_dict().keys())

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
