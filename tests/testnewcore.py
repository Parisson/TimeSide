
from timeside.newcore import *
from sys import stdout

class I1(Interface):
    pass

class I2(Interface):
    pass

class I3(Interface):
    pass

class I4(Interface):
    pass

class I5(Interface):
    pass

class I6(I5):
    pass

class I7(Interface):
    pass

class I8(Interface):
    pass

class C1(Component):
    implements(I1)

class C2(Component):
    implements(I2, I3)

class C3(Component):
    implements(I4)

class C4(Component):
    implements(I4)

class C5(Component):
    implements(I6)

class C6(Component):
    implements(I7)

class C7(C6):
    pass

class C8(Component):
    implements(I8)

class C9(C8):
    implements(I8)

def list_equals(list1, list2):
    if len(list1) != len(list2):
        return False

    for item in list1:
        if not item in list2:
            return False

    for item in list2:
        if not item in list1:
            return False

    return True            

def test(desc, actual, expected):
    stdout.write(desc + ": ")
    if list_equals(actual, expected):
        stdout.write("OK\n")
    else:
        stdout.write("FAILED\n")
        stdout.write("actual:   " + str(actual) + "\n")
        stdout.write("expected: " + str(expected) + "\n")
    

test("Test a component implementing one interface", implementations(I1), [C1])
test("Test a component implementing two interfaces (1/2)", implementations(I2), [C2])
test("Test a component implementing two interfaces (2/2)", implementations(I3), [C2])
test("Test an interface implemented by two components", implementations(I4), [C3, C4])
test("Test whether a component implements an interface's parent", implementations(I5), [C5])
test("Test whether a child component implements the interface implemented by its parent", implementations(I7), [C6, C7])
test("Test implementation redundancy across descendants", implementations(I8), [C8, C9])
