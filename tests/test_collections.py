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
        res = _([1, 2, 3, 4, 5, 6]).reduce(lambda sum, num, *args: sum + num, 0)
        self.assertEqual(21, res, "did not reduced correctly")
        # alias
        res = _([1, 2, 3, 4, 5, 6]).foldl(lambda sum, num, *args: sum + num, 0)
        self.assertEqual(21, res, "did not foldl correctly")
        # alias
        res = _([1, 2, 3, 4, 5, 6]).inject(lambda sum, num, *args: sum + num, 0)
        self.assertEqual(21, res, "did not inject correctly")

    def test_reduce_right(self):
        res = _(["foo", "bar", "baz"]).reduceRight(lambda sum, num, *args: sum + num)
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
        # TODO: Get back to this, I should use "is" for comparison but cannot find a way to do it with "in"
        # self.assertTrue(len(_.without(tlist, {"one": 1})) == 2, 'uses real object identity for comparisons.')
        self.assertTrue(len(_.without(tlist, tlist[0])) == 1, 'ditto.')

    def test_uniq(self):
        tlist = [1, 2, 1, 3, 1, 4]
        self.assertEqual([1, 2, 3, 4], _.uniq(tlist), 'can find the unique values of an unsorted array')

        tlist = [1, 1, 1, 2, 2, 3]
        self.assertEqual([1, 2, 3], _.uniq(tlist, True), 'can find the unique values of a sorted array faster')

        tlist = [{"name": 'moe'}, {"name": 'curly'}, {"name": 'larry'}, {"name": 'curly'}]
        iterator = lambda value, *args: value.get('name')
        self.assertEqual(["moe", "curly", "larry"], _.uniq(tlist, False, iterator), 'can find the unique values of an array using a custom iterator')

        tlist = [1, 2, 2, 3, 4, 4]
        iterator = lambda value, *args: value + 1
        self.assertEqual([2, 3, 4, 5], _.uniq(tlist, True, iterator), 'iterator works with sorted array')

    def test_groupby(self):
        parity = _.groupBy([1, 2, 3, 4, 5, 6], lambda num, *args: num % 2)
        self.assertTrue(0 in parity and 1 in parity, 'created a group for each value')
        self.assertEqual(_(parity[0]).join(', '), '2, 4, 6', 'put each even number in the right group')

        llist = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
        grouped = _.groupBy(llist, lambda x, *args: len(x))
        self.assertEqual(_(grouped[3]).join(' '), 'one two six ten')
        self.assertEqual(_(grouped[4]).join(' '), 'four five nine')
        self.assertEqual(_(grouped[5]).join(' '), 'three seven eight')

    def test_countby(self):
        parity = _.countBy([1, 2, 3, 4, 5], lambda num, *args: num % 2 == 0)
        self.assertEqual(parity[True], 2)
        self.assertEqual(parity[False], 3)

        llist = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
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

    def test_intersection(self):
        stooges = ['moe', 'curly', 'larry'],
        leaders = ['moe', 'groucho']
        self.assertEqual(['moe'], _.intersection(stooges, leaders), 'can take the set intersection of two arrays')
        self.assertEqual(['moe'], _(stooges).intersection(leaders), 'can perform an OO-style intersection')

    def test_union(self):
        result = _.union([1, 2, 3], [2, 30, 1], [1, 40])
        self.assertEqual([40, 1, 2, 3, 30], result, 'takes the union of a list of arrays')

        # There is a problem with nested lists
        # result = _.union([1, 2, 3], [2, 30, 1], [1, 40, [1]])
        # self.assertEqual([1, 2, 3, 30, 40, 1], result, 'takes the union of a list of nested arrays')

    def test_difference(self):
        result = _.difference([1, 2, 3], [2, 30, 40])
        self.assertEqual([1, 3], result, 'takes the difference of two arrays')

        result = _.difference([1, 2, 3, 4], [2, 30, 40], [1, 11, 111])
        self.assertEqual([3, 4], result, 'takes the difference of three arrays')

    def test_zip(self):
        names = ['moe', 'larry', 'curly']
        ages = [30, 40, 50]
        leaders = [True]
        stooges = _(names).zip(ages, leaders)
        self.assertEqual("[('moe', 30, True), ('larry', 40, None), ('curly', 50, None)]", str(stooges), 'zipped together arrays of different lengths')

    def test_zipObject(self):
        result = _.zipObject(['moe', 'larry', 'curly'], [30, 40, 50])
        shouldBe = {"moe": 30, "larry": 40, "curly": 50}
        self.assertEqual(result, shouldBe, "two arrays zipped together into an object")

if __name__ == "__main__":
    print "run these tests by executing `python -m unittest discover` in unittests folder"
    unittest.main()
