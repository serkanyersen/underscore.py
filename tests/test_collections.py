import unittest
from unittesthelper import init
init()  # will let you import modules from upper folder
from src.underscore import _


class TestCollections(unittest.TestCase):

    eachList = []

    def test_each_list(self):
        def eachTest(val, *args):
            self.eachList.append(val + 1)

        _([1, 2, 3, 4]).each(eachTest)
        self.assertEqual([2, 3, 4, 5], self.eachList,
                         "each for lists did not work for all")
        # test alias
        self.eachList = []
        _([1, 2, 3, 4]).forEach(eachTest)
        self.assertEqual([2, 3, 4, 5], self.eachList,
                         "forEach for lists did not work for all")

    eachSet = set()

    def test_each_dict(self):
        def eachTest(val, key, *args):
            self.eachSet.add(val)
            self.eachSet.add(key)

        _({"foo": "bar", "fizz": "buzz"}).each(eachTest)
        self.assertEqual({"foo", "bar", "fizz", "buzz"},
                         self.eachSet, "each for dicts did not work for all")
        # alias
        self.eachSet = set()
        _({"foo": "bar", "fizz": "buzz"}).forEach(eachTest)
        self.assertEqual({"foo", "bar", "fizz", "buzz"},
                         self.eachSet, "forEach for dicts did"
                         "not work for all")

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
        self.assertEqual({"BAR", "FOO"}, set(map),
                         "map for dicts did not work")
        # alias
        map = _({"foo": "bar", "bar": "foo"}).collect(mapTest)
        self.assertEqual({"BAR", "FOO"}, set(map),
                         "collect for dicts did not work")

    def test_reduce(self):
        res = _([1, 2, 3, 4, 5, 6]).reduce(
            lambda sum, num, *args: sum + num, 0)
        self.assertEqual(21, res, "did not reduced correctly")
        # alias
        res = _([1, 2, 3, 4, 5, 6]).foldl(lambda sum, num, *args: sum + num, 0)
        self.assertEqual(21, res, "did not foldl correctly")
        # alias
        res = _([1, 2, 3, 4, 5, 6]).inject(
            lambda sum, num, *args: sum + num, 0)
        self.assertEqual(21, res, "did not inject correctly")

    def test_reduce_right(self):
        res = _(["foo", "bar", "baz"]).reduceRight(
            lambda sum, num, *args: sum + num)
        self.assertEqual("bazbarfoo", res, "did not reducedRight correctly")
        # alias
        res = _(["foo", "bar", "baz"]).foldr(lambda sum, num, *args: sum + num)
        self.assertEqual("bazbarfoo", res, "did not foldr correctly")

    def test_find(self):
        res = _([1, 2, 3, 4, 5]).find(lambda x, *args: x > 2)
        self.assertEqual(3, res, "find didn't work")
        # alias
        res = _([1, 2, 3, 4, 5]).detect(lambda x, *args: x > 2)
        self.assertEqual(3, res, "detect didn't work")

    def test_filter(self):
        res = _(["foo", "hello", "bar", "world"]
                ).filter(lambda x, *args: len(x) > 3)
        self.assertEqual(["hello", "world"], res, "filter didn't work")
        # alias
        res = _(["foo", "hello", "bar", "world"]
                ).select(lambda x, *args: len(x) > 3)
        self.assertEqual(["hello", "world"], res, "select didn't work")

    def test_reject(self):
        res = _(["foo", "hello", "bar", "world"]
                ).reject(lambda x, *args: len(x) > 3)
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
        self.assertEqual(["FOO", "BAR"], res,
                         "invoke with lambda did not work")
        res = _(["foo", "bar"]).invoke("upper")
        self.assertEqual(["FOO", "BAR"], res, "invoke with name did not work")

    def test_pluck(self):
        res = _([{"name": "foo", "age": "29"}, {"name": "bar", "age": "39"},
                {"name": "baz", "age": "49"}]).pluck('age')
        self.assertEqual(["29", "39", "49"], res, "pluck did not work")

    def test_min(self):
        res = _([5, 10, 15, 4, 8]).min()
        self.assertEqual(4, res, "min did not work")

    def test_max(self):
        res = _([5, 10, 15, 4, 8]).max()
        self.assertEqual(15, res, "max did not work")

    def test_sortBy(self):
        res = _([{'age': '59', 'name': 'foo'},
                 {'age': '39', 'name': 'bar'},
                 {'age': '49', 'name': 'baz'}]).sortBy('age')
        self.assertEqual([{'age': '39', 'name': 'bar'},
                          {'age': '49', 'name': 'baz'},
                          {'age': '59', 'name': 'foo'}], res,
                         "filter by key did not work")

        res = _([{'age': '59', 'name': 'foo'},
                 {'age': '39', 'name': 'bar'},
                 {'age': '49', 'name': 'baz'}]).sortBy(lambda x: x['age'])
        self.assertEqual(
            [{'age': '39', 'name': 'bar'}, {'age': '49', 'name': 'baz'},
             {'age': '59', 'name': 'foo'}], res,
            "filter by lambda did not work")

        res = _([50, 78, 30, 15, 90]).sortBy()
        self.assertEqual([15, 30, 50, 78, 90], res, "filter list did not work")

    def test_groupby(self):
        parity = _.groupBy([1, 2, 3, 4, 5, 6], lambda num, *args: num % 2)
        self.assertTrue(0 in parity and 1 in parity,
                        'created a group for each value')
        self.assertEqual(_(parity[0]).join(', '), '2, 4, 6',
                         'put each even number in the right group')

        self.assertEqual(_.groupBy([1], lambda num, *args: num), [1])

        llist = ["one", "two", "three", "four", "five",
                 "six", "seven", "eight", "nine", "ten"]
        grouped = _.groupBy(llist, lambda x, *args: len(x))
        self.assertEqual(_(grouped[3]).join(' '), 'one two six ten')
        self.assertEqual(_(grouped[4]).join(' '), 'four five nine')
        self.assertEqual(_(grouped[5]).join(' '), 'three seven eight')

    def test_countby(self):
        parity = _.countBy([1, 2, 3, 4, 5], lambda num, *args: num % 2 == 0)
        self.assertEqual(parity[True], 2)
        self.assertEqual(parity[False], 3)

        self.assertEqual(_.countBy([1], lambda num, *args: num), 1)

        llist = ["one", "two", "three", "four", "five",
                 "six", "seven", "eight", "nine", "ten"]
        grouped = _.countBy(llist, lambda x, *args: len(x))
        self.assertEqual(grouped[3], 4)
        self.assertEqual(grouped[4], 3)
        self.assertEqual(grouped[5], 3)

    def test_sortedindex(self):
        numbers = [10, 20, 30, 40, 50]
        num = 35
        indexForNum = _.sortedIndex(numbers, num)
        self.assertEqual(3, indexForNum, '35 should be inserted at index 3')

        indexFor30 = _.sortedIndex(numbers, 30)
        self.assertEqual(2, indexFor30, '30 should be inserted at index 2')

    def test_shuffle(self):
        res = _([5, 10, 15, 4, 8]).shuffle()
        self.assertNotEqual([5, 10, 15, 4, 8], res,
                            "shuffled array was the same")

    def test_size(self):
        self.assertEqual(_.size({"one": 1, "two": 2, "three": 3}),
                         3, 'can compute the size of an object')
        self.assertEqual(_.size([1, 2, 3]), 3,
                         'can compute the size of an array')

    def test_where(self):
        List = [{"a": 1, "b": 2}, {"a": 2, "b": 2},
                {"a": 1, "b": 3}, {"a": 1, "b": 4}]
        result = _.where(List, {"a": 1})
        self.assertEqual(_.size(result), 3)
        self.assertEqual(result[-1]['b'], 4)

        result = _.where(List, {"a": 1}, True)
        self.assertEqual(result["b"], 2)

        result = _.where(List, {"a": 1}, False)
        self.assertEqual(_.size(result), 3)

    def test_findWhere(self):
        List = [{"a": 1, "b": 2}, {"a": 2, "b": 2},
                {"a": 1, "b": 3}, {"a": 1, "b": 4}]
        result = _.findWhere(List, {"a": 1})
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"], 2)

        result = _.findWhere(List, {"b": 4})
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"], 4)

        result = _.findWhere(List, {"c": 1})
        self.assertEqual(result, None)

        result = _.findWhere([], {"c": 1})
        self.assertEqual(result, None)

    def test_indexBy(self):
        parity = _.indexBy([1, 2, 3, 4, 5], lambda num, *args: num % 2 == 0)
        self.assertEqual(parity[True], 4)
        self.assertEqual(parity[False], 5)

        self.assertEqual(_.indexBy([1], lambda num, *args: num), 1)

        llist = ["one", "two", "three", "four", "five",
                 "six", "seven", "eight", "nine", "ten"]
        grouped = _.indexBy(llist, lambda x, *args: len(x))
        self.assertEqual(grouped[3], 'ten')
        self.assertEqual(grouped[4], 'nine')
        self.assertEqual(grouped[5], 'eight')

        array = [1, 2, 1, 2, 3]
        grouped = _.indexBy(array)
        self.assertEqual(grouped[1], 1)
        self.assertEqual(grouped[2], 2)
        self.assertEqual(grouped[3], 3)

    def test_partition(self):

        list = [0, 1, 2, 3, 4, 5]

        self.assertEqual(_.partition(list, lambda x, *args: x < 4),
                         [[0, 1, 2, 3], [4, 5]], 'handles bool return values')
        self.assertEqual(_.partition(list, lambda x, *args: x & 1),
                         [[1, 3, 5], [0, 2, 4]],
                         'handles 0 and 1 return values')
        self.assertEqual(_.partition(list, lambda x, *args: x - 3),
                         [[0, 1, 2, 4, 5], [3]],
                         'handles other numeric return values')
        self.assertEqual(
            _.partition(list, lambda x, *args: None if x > 1 else True),
            [[0, 1], [2, 3, 4, 5]], 'handles null return values')

        # Test an object
        result = _.partition({"a": 1, "b": 2, "c": 3}, lambda x, *args: x > 1)
        # Has to handle difference between python3 and python2
        self.assertTrue(
            (result == [[3, 2], [1]] or result == [[2, 3], [1]]),
            'handles objects')

        # Default iterator
        self.assertEqual(_.partition([1, False, True, '']),
                         [[1, True], [False, '']], 'Default iterator')
        self.assertEqual(_.partition([{"x": 1}, {"x": 0}, {"x": 1}], 'x'),
                         [[{"x": 1}, {"x": 1}], [{"x": 0}]], 'Takes a string')


if __name__ == "__main__":
    print("run these tests by executing `python -m unittest"
          " discover` in unittests folder")
    unittest.main()
