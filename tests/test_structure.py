import unittest
from unittesthelper import init
init()  # will let you import modules from upper folder
from src.underscore import _


class TestStructure(unittest.TestCase):

    def test_oo(self):
        min = _([1, 2, 3, 4, 5]).min()
        self.assertEqual(1, min, "oo did not work")

    def test_static(self):
        min = _.min([1, 2, 3, 4, 5])
        self.assertEqual(1, min, "static did not work")

    def test_chaining(self):
        array = range(1, 11)
        u = _(array).chain().filter(lambda x: x > 5).min()
        self.assertTrue(isinstance(u, _.underscore),
                        "object is not an instanse of underscore")
        self.assertEqual(6, u.value(), "value should have returned")

if __name__ == "__main__":
    print("run these tests by executing `python -m unittest"
          "discover` in unittests folder")
    unittest.main()
