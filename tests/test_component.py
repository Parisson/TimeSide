from timeside.component import *
from unit_timeside import *

__all__ = ['TestComponentArchitecture']

class TestComponentArchitecture(TestCase):
    "Test the component and interface system"
   
    def testOneInterface(self):
        "Test a component implementing one interface"
        self.assertSameList(implementations(I1), [C1])

    def testTwoInterfaces(self):        
        "Test a component implementing two interfaces"
        self.assertSameList(implementations(I2), [C2])
        self.assertSameList(implementations(I3), [C2])

    def testTwoImplementations(self):
        "Test an interface implemented by two components"
        self.assertSameList(implementations(I4), [C3, C4])

    def testInterfaceInheritance(self):
        "Test whether a component implements an interface's parent"
        self.assertSameList(implementations(I5), [C5])

    def testImplementationInheritance(self):
        "Test that a component doesn't implement the interface implemented by its parent" 
        self.assertSameList(implementations(I7), [C6])

    def testImplementationRedundancy(self):
        "Test implementation redundancy across inheritance" 
        self.assertSameList(implementations(I8), [C8, C9])

    def testAbstractImplementation(self):    
        "Test abstract implementation"
        self.assertSameList(implementations(I11), [])
        self.assertSameList(implementations(I11, abstract=True), [C11])

    def testInterfaceDoc(self):        
        "Test @interfacedoc decorator"
        self.assertEquals(C10.test.__doc__, "testdoc")

    def testInterfaceDocStatic(self):        
        "Test @interfacedoc decorator on static method"
        self.assertEquals(C10.teststatic.__doc__, "teststaticdoc")

    def testIntefaceDocReversed(self):
        "Test @interfacedoc on static method (decorators reversed)"

        try:

            class BogusDoc1(Component):
                implements(I10)

                @interfacedoc
                @staticmethod        
                def teststatic(self):
                    pass

            self.fail("No error raised with reversed decorators")

        except ComponentError:
            pass
   
    def testInterfaceDocBadMethod(self):
        "Test @interfacedoc with unexistant method in interface"

        try:
            class BogusDoc2(Component):
                implements(I10)

                @interfacedoc
                def nosuchmethod(self):
                    pass

            self.fail("No error raised when decorating an unexistant method")

        except ComponentError:
            pass

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

class I9(I8):
    pass

class I10(Interface):
    def test(self):
        """testdoc"""

    @staticmethod        
    def teststatic(self):
        """teststaticdoc"""

class I11(Interface):
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

class C9(Component):
    implements(I8, I9)

class C10(Component):
    implements(I10)

    @interfacedoc
    def test(self):
        pass

    @staticmethod        
    @interfacedoc
    def teststatic(self):
        pass

class C11(Component):
    abstract()
    implements(I11)

if __name__ == '__main__':
    unittest.main(testRunner=TestRunner())

