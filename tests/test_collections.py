import unittest
from unittesthelper import init
init()  # will let you import modules from upper folder
from src.underscore import _


class TestStructure(unittest.TestCase):

    eachList = []

    def test_each_list(self):
        def eachTest(val, *args):
            self.eachList.append(val + 1)

        _([1, 2, 3, 4]).each(eachTest)
        self.assertEqual([2, 3, 4, 5], self.eachList, "each for lists did not work for all")
        # test alias
        self.eachList = []
        _([1, 2, 3, 4]).forEach(eachTest)
        self.assertEqual([2, 3, 4, 5], self.eachList, "forEach for lists did not work for all")

    eachDict = ""

    def test_each_dict(self):
        def eachTest(val, key, *args):
            self.eachDict += (key + ":" + val + " ")

        _({"foo": "bar", "bar": "foo"}).each(eachTest)
        self.assertEqual("foo:bar bar:foo ", self.eachDict, "each for dicts did not work for all")
        # alias
        self.eachDict = ""
        _({"foo": "bar", "bar": "foo"}).forEach(eachTest)
        self.assertEqual("foo:bar bar:foo ", self.eachDict, "forEach for dicts did not work for all")

    def test_map_list(self):
        def mapTest(val, *args):
            return val * 2
        map = _([1, 2, 3, 4]).map(mapTest)
        self.assertEqual([2, 4, 6, 8], map, "map for list did not work")
        # alias
        map = _([1, 2, 3, 4]).collect(mapTest)
        self.assertEqual([2, 4, 6, 8], map, "collect for list did not work")

    def test_map_dict(self):
        def mapTest(val, key, *args):
            return val.upper()
        map = _({"foo": "bar", "bar": "foo"}).map(mapTest)
        self.assertEqual(["BAR", "FOO"], map, "map for dicts did not work")
        # alias
        map = _({"foo": "bar", "bar": "foo"}).collect(mapTest)
        self.assertEqual(["BAR", "FOO"], map, "collect for dicts did not work")

    def test_reduce(self):
        res = _([1, 2, 3, 4, 5, 6]).reduce(lambda sum, num: sum + num)
        self.assertEqual(21, res, "did not reduced correctly")
        # alias
        res = _([1, 2, 3, 4, 5, 6]).foldl(lambda sum, num: sum + num)
        self.assertEqual(21, res, "did not foldl correctly")
        # alias
        res = _([1, 2, 3, 4, 5, 6]).inject(lambda sum, num: sum + num)
        self.assertEqual(21, res, "did not inject correctly")

    def test_reduce_right(self):
        res = _(["foo", "bar", "baz"]).reduceRight(lambda sum, num: sum + num)
        self.assertEqual("bazbarfoo", res, "did not reducedRight correctly")
        # alias
        res = _(["foo", "bar", "baz"]).foldr(lambda sum, num: sum + num)
        self.assertEqual("bazbarfoo", res, "did not foldr correctly")

    def test_find(self):
        res = _([1, 2, 3, 4, 5]).find(lambda x, *args: x > 2)
        self.assertEqual(3, res, "find didn't work")
        # alias
        res = _([1, 2, 3, 4, 5]).detect(lambda x, *args: x > 2)
        self.assertEqual(3, res, "detect didn't work")

    def test_filter(self):
        res = _(["foo", "hello", "bar", "world"]).filter(lambda x, *args: len(x) > 3)
        self.assertEqual(["hello", "world"], res, "filter didn't work")
        # alias
        res = _(["foo", "hello", "bar", "world"]).select(lambda x, *args: len(x) > 3)
        self.assertEqual(["hello", "world"], res, "select didn't work")

    def test_reject(self):
        res = _(["foo", "hello", "bar", "world"]).reject(lambda x, *args: len(x) > 3)
        self.assertEqual(["foo", "bar"], res, "reject didn't work")

    def test_all(self):
        res = _([True, True, True, True]).all()
        self.assertTrue(res, "all was not true")
        res = _([True, True, False, True]).all()
        self.assertFalse(res, "all was not false")

    def test_any(self):
        res = _([False, False, False, True]).any()
        self.assertTrue(res, "any was not true")
        res = _([False, False, False, False]).any()
        self.assertFalse(res, "any was not false")

    def test_include(self):
        res = _(["hello", "world", "foo", "bar"]).include('foo')
        self.assertTrue(res, "include was not true")
        res = _(["hello", "world", "foo", "bar"]).include('notin')
        self.assertFalse(res, "include was not false")

    def test_include_dict(self):
        res = _({"foo": "bar", "hello": "world"}).include('bar')
        self.assertTrue(res, "include was not true")
        res = _({"foo": "bar", "hello": "world"}).include('notin')
        self.assertFalse(res, "include was not false")

    def test_invoke(self):
        res = _(["foo", "bar"]).invoke(lambda x, *args: x.upper())
        self.assertEqual(["FOO", "BAR"], res, "invoke with lambda did not work")
        res = _(["foo", "bar"]).invoke("upper")
        self.assertEqual(["FOO", "BAR"], res, "invoke with name did not work")

    def test_pluck(self):
        res = _([{"name": "foo", "age": "29"}, {"name": "bar", "age": "39"}, {"name": "baz", "age": "49"}]).pluck('age')
        self.assertEqual(["29", "39", "49"], res, "pluck did not work")

    def test_min(self):
        res = _([5, 10, 15, 4, 8]).min()
        self.assertEqual(4, res, "min did not work")

    def test_max(self):
        res = _([5, 10, 15, 4, 8]).max()
        self.assertEqual(15, res, "max did not work")

    def test_shuffle(self):
        res = _([5, 10, 15, 4, 8]).shuffle()
        self.assertNotEqual([5, 10, 15, 4, 8], res, "shuffled array was the same")

    def test_sortBy(self):
        res = _([{'age': '59', 'name': 'foo'},
                 {'age': '39', 'name': 'bar'},
                 {'age': '49', 'name': 'baz'}]).sortBy('age')
        self.assertEqual([{'age': '39', 'name': 'bar'},
                          {'age': '49', 'name': 'baz'},
                          {'age': '59', 'name': 'foo'}], res, "filter by key did not work")

        res = _([{'age': '59', 'name': 'foo'},
                 {'age': '39', 'name': 'bar'},
                 {'age': '49', 'name': 'baz'}]).sortBy(lambda x, y, *args: cmp(x, y))
        self.assertEqual([{'age': '39', 'name': 'bar'}, {'age': '49', 'name': 'baz'}, {'age': '59', 'name': 'foo'}], res, "filter by lambda did not work")

        res = _([50, 78, 30, 15, 90]).sortBy()
        self.assertEqual([15, 30, 50, 78, 90], res, "filter list did not work")

    def test_first(self):
        res = _([1, 2, 3, 4, 5]).first()
        self.assertEqual(1, res, "first one item did not work")
        res = _([1, 2, 3, 4, 5]).first(3)
        self.assertEqual([1, 2, 3], res, "first multi item did not wok")

    def test_initial(self):
        res = _([1, 2, 3, 4, 5]).initial()
        self.assertEqual([1, 2, 3, 4], res, "initial one item did not work")
        res = _([1, 2, 3, 4, 5]).initial(3)
        self.assertEqual([1, 2], res, "initial multi item did not wok")

    def test_last(self):
        res = _([1, 2, 3, 4, 5]).last()
        self.assertEqual(5, res, "last one item did not work")
        res = _([1, 2, 3, 4, 5]).last(3)
        self.assertEqual([3, 4, 5], res, "last multi item did not wok")

    def test_rest(self):
        res = _([1, 2, 3, 4, 5]).rest()
        self.assertEqual([2, 3, 4, 5], res, "rest one item did not work")
        res = _([1, 2, 3, 4, 5]).rest(3)
        self.assertEqual([4, 5], res, "rest multi item did not wok")

    def test_compact(self):
        res = _([False, 1, 0, "foo", None, -1]).compact()
        self.assertEqual([1, "foo", -1], res, "compact did not work")

    def test_without(self):
        tlist = [1, 2, 1, 0, 3, 1, 4]
        self.assertEqual([2, 3, 4], _.without(tlist, 0, 1), 'can remove all instances of an object')

        tlist = [{"one": 1}, {"two": 2}]
        # TODO: Get back to this
        # self.assertTrue(len(_.without(tlist, {"one": 1})) == 2, 'uses real object identity for comparisons.')
        self.assertTrue(len(_.without(tlist, tlist[0])) == 1, 'ditto.')

    def test_uniq(self):
        tlist = [1, 2, 1, 3, 1, 4]
        self.assertEqual([1, 2, 3, 4], _.uniq(tlist), 'can find the unique values of an unsorted array')

        tlist = [1, 1, 1, 2, 2, 3]
        self.assertEqual([1, 2, 3], _.uniq(tlist, True), 'can find the unique values of a sorted array faster')

        # tlist = [{"name": 'moe'}, {"name": 'curly'}, {"name": 'larry'}, {"name": 'curly'}]
        # iterator = lambda value: value.get('name')
        # self.assertEqual(["moe", "curly", "larry"], _.map(_.uniq(tlist, False, iterator), iterator), 'can find the unique values of an array using a custom iterator')

        # iterator = lambda value: value + 1
        # tlist = [1, 2, 2, 3, 4, 4]
        # self.assertEqual([1, 2, 3, 4], _.uniq(tlist, True, iterator), 'iterator works with sorted array')

if __name__ == "__main__":
    print "run these tests by executing `python -m unittest discover` in unittests folder"
    unittest.main()
