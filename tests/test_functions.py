import unittest
from unittesthelper import init
init()  # will let you import modules from upper folder
from src.underscore import _


class TestStructure(unittest.TestCase):

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
        pass

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
        pass

    def test_after(self):
        pass

if __name__ == "__main__":
    print "run these tests by executing `python -m unittest discover` in unittests folder"
    unittest.main()
