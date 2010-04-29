import unittest
import inspect

class MagicTest(unittest.TestCase):
    @classmethod
    def testfuncs(cls):
        testcase_methods = dir(unittest.TestCase)
        for m in inspect.classify_class_attrs(cls):
            if m.kind == 'method' and m.defining_class == cls \
                    and m.name not in testcase_methods:
                yield inspect.findsource(getattr(cls,m.name))[1], m.name

    @classmethod
    def toSuite(cls):
        suite = unittest.TestSuite()
        for lineno, name in sorted(cls.testfuncs()):
            suite.addTest(cls(name))
        return suite

    @classmethod
    def runSuite(cls):
        unittest.TextTestRunner(verbosity=2).run(cls.toSuite())

