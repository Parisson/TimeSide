#! /usr/bin/env python

from timeside.core import FixedSizeInputAdapter
from unit_timeside import *
import numpy

class TestFixedSizeInputAdapter(TestCase):
    "Test the fixed-sized input adapter"

    def assertIOEquals(self, adapter, input, input_eod, output, output_eod=None):
        output = output[:]
        output.reverse()
        _eod = None
        for buffer, _eod in adapter.process(input, input_eod):
            a = output.pop()
            if not numpy.array_equiv(buffer, a):
                self.fail("\n-- Actual --\n%s\n -- Expected -- \n%s\n" % (str(buffer), str(a)))

        if _eod != output_eod:
            self.fail("eod do not match: %s != %s", (str(_eod), str(output_eod)))

        if output:
            self.fail("trailing expected data: %s" % output)

    def setUp(self):
        self.data = numpy.arange(44).reshape(2,22).transpose()

    def testTwoChannels(self):
        "Test simple stream with two channels"
        adapter = FixedSizeInputAdapter(4, 2)

        self.assertEquals(len(self.data), adapter.blocksize(len(self.data)))

        self.assertIOEquals(adapter, self.data[0:1], False, [])
        self.assertIOEquals(adapter, self.data[1:5], False, [self.data[0:4]], False)
        self.assertIOEquals(adapter, self.data[5:12], False, [self.data[4:8], self.data[8:12]], False)
        self.assertIOEquals(adapter, self.data[12:13], False, [])
        self.assertIOEquals(adapter, self.data[13:14], False, [])
        self.assertIOEquals(adapter, self.data[14:18], False, [self.data[12:16]], False)
        self.assertIOEquals(adapter, self.data[18:20], False, [self.data[16:20]], False)
        self.assertIOEquals(adapter, self.data[20:21], False, [])
        self.assertIOEquals(adapter, self.data[21:22], True, [self.data[20:22]], True)

    def testPadding(self):
        "Test automatic padding support"
        adapter = FixedSizeInputAdapter(4, 2, pad=True)

        self.assertEquals(len(self.data) + 2, adapter.blocksize(len(self.data)))

        self.assertIOEquals(adapter, self.data[0:21], False,
            [self.data[0:4], self.data[4:8], self.data[8:12], self.data[12:16], self.data[16:20]],
            False)

        self.assertIOEquals(adapter, self.data[21:22], True, [[
            [20, 42],
            [21, 43],
            [0, 0],
            [0, 0]
        ]], True)

    def testSizeMultiple(self):
        "Test a stream which contain a multiple number of buffers"
        adapter = FixedSizeInputAdapter(4, 2)

        self.assertIOEquals(adapter, self.data[0:20], True,
            [self.data[0:4], self.data[4:8], self.data[8:12], self.data[12:16], self.data[16:20]],
            True)


if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())

