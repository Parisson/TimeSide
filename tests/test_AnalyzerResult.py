#! /usr/bin/env python

from unit_timeside import unittest, TestRunner
from timeside.core.analyzer import AnalyzerResult, AnalyzerResultContainer
from timeside.core import __version__
import numpy as np
from math import pi
import pandas as pd
from functools import wraps

verbose = 0


class TestAnalyzerResult(unittest.TestCase):
    """ test AnalyzerResult """

    def setUp(self):
        self.result = AnalyzerResult(data_mode='value',
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

        self.result_value = None

    def tearDown(self):
        pass

# Get good and bad types for AnalyzerResult.data_object.data.value
from timeside.core.analyzer import NUMPY_DATA_TYPES as GOOD_DTYPES
GOOD_NUMPY_DATA_TYPES = [str(dtype)[13:-2] for dtype in GOOD_DTYPES]
BAD_NUMPY_DATA_TYPES = [
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


@unittest.skip
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
# for numpy_data_type in BAD_NUMPY_DATA_TYPES:
#    TestAnalyzerResultBadType.add_method(numpy_data_type)


class TestAnalyzerResultGoodType(TestAnalyzerResult):
    """ test AnalyzerResult on good numpy data type"""

    def check_data_assignment(func):
        @wraps(func)
        def wrapper(self):
            func(self)
            self.result.data_object['value'] = pd.DataFrame(self.result_value)
        return wrapper

    @check_data_assignment
    def testOnFloat(self):
        "float result"
        self.result_value = [1.2]

    @check_data_assignment
    def testOnInt(self):
        "integer result"
        self.result_value = [1]

    @check_data_assignment
    def testOnList(self):
        "list result"
        self.result_value = [1., 2.]

    @unittest.skip("String have to be handled through label metadata")
    @check_data_assignment
    def testOnString(self):
        "string result"
        self.result_value = ["hello"]

    @unittest.skip("String have to be handled through label metadata")
    @check_data_assignment
    def testOnListOfString(self):
        "list of strings result"
        self.result_value = ["hello", "hola"]

    @check_data_assignment
    def testOnListOfList(self):
        "list of lists result"
        self.result_value = [[0, 1], [0, 1, 2]]

    @check_data_assignment
    def testOnNumpyVectorOfFloat(self):
        "numpy vector of float"
        self.result_value = np.ones(2, dtype='float') * pi

    @check_data_assignment
    def testOnNumpy2DArrayOfFloat64(self):
        "numpy 2d array of float64"
        self.result_value = np.random.randn(10, 5)

    @check_data_assignment
    def testOnNumpy2DArrayOfInt32(self):
        "numpy 2D array of int32"
        self.result_value = np.random.randint(10, size=(10, 5))

    @unittest.skip("String have to be handled through label metadata")
    def testOnNumpyArrayOfStrings(self):
        "numpy array of strings"
        self.result_value = np.array(['hello', 'hola'])

    @check_data_assignment
    def testOnEmptyList(self):
        "empty list"
        self.result_value = []

    @check_data_assignment
    def testOnNone(self):
        "None"
        self.result_value = None

    @unittest.skip("String have to be handled through label metadata")
    def testOnUnicode(self):
        "Unicode"
        self.result_value = u'\u0107'

    def method(self, numpy_data_type):
        """Good numpy data type"""
        self.result.data_object['value'] = pd.DataFrame([getattr(np, numpy_data_type)(pi)])

    @classmethod
    def add_method(cls, numpy_data_type):
        test_method = lambda self: self.method(numpy_data_type)
        test_method.__name__ = 'testOnNumpy_%s' % numpy_data_type
        test_method.__doc__ = 'Support numpy %s' % numpy_data_type
        setattr(cls, test_method.__name__, test_method)

# Add tests for each type in good_numpy_data_types
for numpy_data_type in GOOD_NUMPY_DATA_TYPES:
    TestAnalyzerResultGoodType.add_method(numpy_data_type)


@unittest.skip
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


class LevelAnalyzer(object):

    def testOnLevelAnaylyzer(self):
        from timeside.core import get_processor
        from timeside.core.tools.test_samples import samples

        wav_file = samples['C4_scale.wav']
        decoder = get_processor('file_decoder')(uri=wav_file)
        analyzer = get_processor('level')()
        pipe = (decoder | analyzer)
        pipe.run()
        self.result = analyzer.results


@unittest.skip
class TestAnalyzerResultHdf5(TestAnalyzerResultGoodType, LevelAnalyzer):
    """ test AnalyzerResult hdf5 serialize """

    def tearDown(self):
        if isinstance(self.result, AnalyzerResult):
            results = AnalyzerResultContainer([self.result])
        elif isinstance(self.result, AnalyzerResultContainer):
            results = self.result
        else:
            raise(TypeError, "Wrong type for self.result")

        import tempfile
        h5_file = tempfile.NamedTemporaryFile(suffix='.h5', delete=True)
        results.to_hdf5(h5_file.name)

        from_results = AnalyzerResultContainer()
        from_results.from_hdf5(h5_file.name)

        if verbose:
            print '%15s' % 'from hdf5:',
            print from_results
        self.assertEqual(results, from_results)
        h5_file.close()


@unittest.skip
class TestAnalyzerResultXml(TestAnalyzerResultGoodType):
    """ test AnalyzerResult xml serialize """

    def tearDown(self):
        results = AnalyzerResultContainer([self.result])
        r_xml = results.to_xml()
        if verbose:
            print 'to xml:'
            print r_xml

        from_results = AnalyzerResultContainer()
        from_results.from_xml(r_xml)
        if verbose:
            print '%15s' % 'from xml:',
            print from_results

        # for i in range(len(d_xml)):
        self.assertEqual(results, from_results)


@unittest.skip
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

        from_results = AnalyzerResultContainer()
        from_results.from_json(r_json)
        if verbose:
            print from_results
            print '%15s' % 'from json:',

        self.assertEqual(results, from_results)


@unittest.skip
class TestAnalyzerResultAsDict(TestAnalyzerResultGoodType):
    """ test AnalyzerResult as Dictionnary"""

    def tearDown(self):

        self.assertIsInstance(self.result.as_dict(), dict)
        self.assertItemsEqual(self.result.keys() + ['data_mode', 'time_mode'],
                              self.result.as_dict().keys())

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())
