import unittest
from unittesthelper import init
init()  # will let you import modules from upper folder
from src.underscore import _
from threading import Timer


class TestStructure(unittest.TestCase):

    class Namespace:
        pass

    def test_bind(self):
        pass

    def test_bindAll(self):
        pass

    def test_memoize(self):
        def fib(n):
            return n if n < 2 else fib(n - 1) + fib(n - 2)

        fastFib = _.memoize(fib)
        self.assertEqual(fib(10), 55, 'a memoized version of fibonacci produces identical results')
        self.assertEqual(fastFib(10), 55, 'a memoized version of fibonacci produces identical results')
        self.assertEqual(fastFib(10), 55, 'a memoized version of fibonacci produces identical results')
        self.assertEqual(fastFib(10), 55, 'a memoized version of fibonacci produces identical results')

        def o(str):
            return str

        fastO = _.memoize(o)
        self.assertEqual(o('upper'), 'upper', 'checks hasOwnProperty')
        self.assertEqual(fastO('upper'), 'upper', 'checks hasOwnProperty')

    def test_delay(self):

        ns = self.Namespace()
        ns.delayed = False

        def func():
            ns.delayed = True

        _.delay(func, 50)

        def checkFalse():
            self.assertFalse(ns.delayed)

        def checkTrue():
            self.assertTrue(ns.delayed)

        Timer(0.03, checkFalse).start()
        Timer(0.07, checkTrue).start()

    def test_defer(self):
        pass

    def test_throttle(self):
        pass

    def test_debounce(self):
        ns = self.Namespace()
        ns.counter = 0

        def incr():
            ns.counter += 1

        debouncedIncr = _.debounce(incr, 50)
        debouncedIncr()
        debouncedIncr()
        debouncedIncr()
        Timer(0.03, debouncedIncr).start()
        Timer(0.06, debouncedIncr).start()
        Timer(0.09, debouncedIncr).start()
        Timer(0.12, debouncedIncr).start()
        Timer(0.15, debouncedIncr).start()

        def checkCounter():
            self.assertEqual(1, ns.counter, "incr was debounced")

        _.delay(checkCounter, 220)

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
