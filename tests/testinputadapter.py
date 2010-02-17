from timeside.core import FixedSizeInputAdapter
from sys import stdout
import numpy

def test(adapter, data, eod, expected):
    expected.reverse()
    for buffer, _eod in adapter.process(data, eod):
        a = expected.pop()
        if not numpy.array_equiv(buffer, a):
            raise Exception("\n-- Actual --\n%s\n -- Expected -- \n%s\n" % (str(buffer), str(a)))

    if expected:
        raise Exception("trailing expected data: %s" % expected)

    stdout.write(".")            

data = numpy.arange(44).reshape(2,22).transpose()

adapter = FixedSizeInputAdapter(4, 2)
stdout.write("%s simple test" % adapter.__class__.__name__)

expected = len(data)
actual   = adapter.nframes(len(data))
if actual != expected:
    raise Exception("%d != %d nframes", (actual, expected))

test(adapter, data[0:1], False, [])
test(adapter, data[1:5], False, [data[0:4]])
test(adapter, data[5:12], False, [data[4:8], data[8:12]])
test(adapter, data[12:13], False, [])
test(adapter, data[13:14], False, [])
test(adapter, data[14:18], False, [data[12:16]])
test(adapter, data[18:20], False, [data[16:20]])
test(adapter, data[20:21], False, [])
test(adapter, data[21:22], True, [data[20:22]])
stdout.write(" OK\n")

adapter = FixedSizeInputAdapter(4, 2, pad=True)
stdout.write("%s padding test" % adapter.__class__.__name__)

expected = len(data) + 2
actual   = adapter.nframes(len(data))
if actual != expected:
    raise Exception("%d != %d nframes", (actual, expected))

test(adapter, data[0:21], False, [data[0:4], data[4:8], data[8:12], data[12:16], data[16:20]])
test(adapter, data[21:22], True, [[
    [20, 42],
    [21, 43],
    [0, 0],
    [0, 0]
]])
stdout.write(" OK\n")
