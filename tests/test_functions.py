import unittest
from unittesthelper import init
init()  # will let you import modules from upper folder
from src.underscore import _


class TestStructure(unittest.TestCase):

    class Namespace:
        pass

    def test_bind(self):
        pass

    def test_bindAll(self):
        pass

    def test_memoize(self):
        pass

    def test_delay(self):
        pass

    def test_defer(self):
        pass

    def test_throttle(self):
        pass

    def test_debounce(self):
        pass

    def test_once(self):
        ns = self.Namespace()
        ns.num = 0

        def add():
            ns.num += 1

        increment = _.once(add)
        increment()
        increment()
        increment()
        increment()
        self.assertEqual(ns.num, 1)

    def test_wrap(self):
        pass

    def test_compose(self):
        def greet(name):
            return "hi: " + name

        def exclaim(sentence):
            return sentence + '!'

        def upperize(full):
            return full.upper()

        composed_function = _.compose(exclaim, greet, upperize)

        self.assertEqual('HI: MOE!', composed_function('moe'), 'can compose a function that takes another')

    def test_after(self):

        def testAfter(afterAmount, timesCalled):
            ns = self.Namespace()
            ns.afterCalled = 0

            def afterFunc():
                ns.afterCalled += 1

            after = _.after(afterAmount, afterFunc)

            while (timesCalled):
                after()
                timesCalled -= 1

            return ns.afterCalled

        self.assertEqual(testAfter(5, 5), 1, "after(N) should fire after being called N times")
        self.assertEqual(testAfter(5, 4), 0, "after(N) should not fire unless called N times")
        self.assertEqual(testAfter(0, 0), 1, "after(0) should fire immediately")

if __name__ == "__main__":
    print "run these tests by executing `python -m unittest discover` in unittests folder"
    unittest.main()
