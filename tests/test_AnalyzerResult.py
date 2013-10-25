#! /usr/bin/env python

from unit_timeside import *
from timeside.analyzer.core import *
from timeside.__init__ import __version__
from numpy import ones, array
from math import pi


verbose = 0


class TestAnalyzerResult(TestCase):
    """ test AnalyzerResult """

    def setUp(self):
        self.result = analyzer_result_factory(data_mode='value', time_mode='framewise')
        from datetime import datetime
        self.result.id_metadata = dict(date=datetime.now().replace(microsecond=0).isoformat(' '),
                                       version=__version__,
                                       author='TimeSide',
                                       id="foo_bar",
                                       name="Foo bar",
                                       unit="foo")
        self.result.audio_metadata = dict(uri='Foo.wav',
                                         start=0, duration=20,
                                         channels=2)

    def testOnFloat(self):
        "float result"
        self.result.data_object.value = 1.2

    def testOnInt(self):
        "integer result"
        self.result.data_object.value = 1

    def testOnList(self):
        "list result"
        self.result.data_object.value = [1., 2.]

    def testOnString(self):
        "string result"
        self.result.data_object.value = "hello"

    def testOnListOfString(self):
        "list of strings result"
        self.result.data_object.value = ["hello", "hola"]

    def testOnListOfList(self):
        "list of lists result"
        self.result.data_object.value = [[0, 1], [0, 1, 2]]

    def testOnNumpyVectorOfFloat(self):
        "numpy vector of float"
        self.result.data_object.value = ones(2, dtype='float') * pi

    def testOnNumpy2DArrayOfFloat64(self):
        "numpy 2d array of float64"
        self.result.data_object.value = ones([2, 3], dtype='float64') * pi

    def testOnNumpy3DArrayOfInt32(self):
        "numpy 3d array of int32"
        self.result.data_object.value = ones([2, 3, 2], dtype='int32')

    def testOnNumpyArrayOfStrings(self):
        "numpy array of strings"
        self.result.data_object.value = array(['hello', 'hola'])

    def testOnEmptyList(self):
        "empty list"
        self.result.data_object.value = []

    def testOnNone(self):
        "None"
        self.result.data_object.value = None

    def testOnUnicode(self):
        "None"
        self.result.data_object.value = None

    def tearDown(self):
        pass

#good_numpy_data_types = [
#    'float64',
#    'float32',
##    'float16',
#    'int64',
#    'int16',
#    'int32',
#    'int8',
#    'uint16',
#    'uint32',
#    'uint64',
#    'uint8',
#]
from timeside.analyzer.core import numpy_data_types as good_numpy_data_types

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
    ]


def create_good_method_func(numpy_data_type):
    def method(self):
        "numpy %s" % str(numpy_data_type)[7:-1]
        import numpy
        self.result.data_object.value = numpy_data_type(pi)
    return method


def create_bad_method_func(numpy_data_type):
    def method(self):
        "numpy %s" % numpy_data_type
        import numpy
        try:
            data = getattr(numpy, numpy_data_type)(pi)
        except ValueError:
            data = getattr(numpy, numpy_data_type)()
        self.assertRaises(TypeError, self.result.data_object.__setattr__, 'value', data)
    return method

for numpy_data_type in good_numpy_data_types:
    test_method = create_good_method_func(numpy_data_type)
    str_type = str(numpy_data_type)[13:-2] # keep only type string
    test_method.__name__ = 'testOnNumpy_%s' % str_type
    test_method.__doc__ = 'groks a numpy %s' % str_type
    setattr(TestAnalyzerResult, test_method.__name__, test_method)

for numpy_data_type in bad_numpy_data_types:
    test_method = create_bad_method_func(numpy_data_type)
    test_method.__name__ = 'testOnNumpy_%s' % numpy_data_type
    test_method.__doc__ = 'gasps on numpy %s' % numpy_data_type
    setattr(TestAnalyzerResult, test_method.__name__, test_method)


class TestAnalyzerResultNumpy(TestAnalyzerResult):
    """ test AnalyzerResult numpy serialize """

    def tearDown(self):
        results = AnalyzerResultContainer([self.result])
        r_numpy = results.to_numpy('/tmp/t.npy')
        d_numpy = results.from_numpy('/tmp/t.npy')
        if verbose:
            print '%15s' % 'from numpy:',
            print d_numpy
        self.assertEquals(d_numpy, results)


class TestAnalyzerResultHdf5(TestAnalyzerResult):
    """ test AnalyzerResult hdf5 serialize """

    def tearDown(self):
        results = AnalyzerResultContainer([self.result])
        results.to_hdf5('/tmp/t.h5')
        res_hdf5 = results.from_hdf5('/tmp/t.h5')
        if verbose:
            print '%15s' % 'from hdf5:',
            print res_hdf5
        self.assertEquals(res_hdf5, results)


class TestAnalyzerResultYaml(TestAnalyzerResult):
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
        self.assertEquals(results, d_yaml)


class TestAnalyzerResultXml(TestAnalyzerResult):
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
        self.assertEquals(d_xml, results)


class TestAnalyzerResultJson(TestAnalyzerResult):
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
            print '%15s' % 'from yaml:',

        #for i in range(len(d_json)):
        self.assertEquals(d_json, results)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())