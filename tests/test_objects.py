import unittest
from unittesthelper import init
init()  # will let you import modules from upper folder
from src.underscore import _


class TestObjects(unittest.TestCase):

    def test_keys(self):
        self.assertEqual(set(_.keys({"one": 1, "two": 2})),
                         {'two', 'one'}, 'can extract the keys from an object')

    def test_values(self):
        self.assertEqual(set(_.values({"one": 1, "two": 2})),
                         {2, 1}, 'can extract the values from an object')

    def test_functions(self):
        obj = {"a": 'dash', "b": _.map, "c": ("/yo/"), "d": _.reduce}
        self.assertEqual(['b', 'd'], _.functions(obj),
                         'can grab the function names of any passed-in object')

    def test_extend(self):

        self.assertEqual(_.extend({}, {"a": 'b'}).get("a"), 'b',
                         'can extend an object with the attributes of another')
        self.assertEqual(_.extend({"a": 'x'}, {"a": 'b'}).get(
            "a"), 'b', 'properties in source override destination')
        self.assertEqual(_.extend({"x": 'x'}, {"a": 'b'}).get(
            "x"), 'x', 'properties not in source dont get overriden')
        result = _.extend({"x": 'x'}, {"a": 'a'}, {"b": 'b'})
        self.assertEqual(result, {"x": 'x', "a": 'a', "b": 'b'},
                         'can extend from multiple source objects')
        result = _.extend({"x": 'x'}, {"a": 'a', "x": 2}, {"a": 'b'})
        self.assertEqual(result, {"x": 2, "a": 'b'},
                         'extending from multiple source'
                         ' objects last property trumps')
        result = _.extend({}, {"a": None, "b": None})
        self.assertEqual(set(_.keys(result)),
                         {"a", "b"}, 'extend does not copy undefined values')

    def test_pick(self):
        result = _.pick({"a": 1, "b": 2, "c": 3}, 'a', 'c')
        self.assertTrue(_.isEqual(result, {'a': 1, 'c': 3}),
                        'can restrict properties to those named')
        result = _.pick({"a": 1, "b": 2, "c": 3}, ['b', 'c'])
        self.assertTrue(_.isEqual(result, {"b": 2, "c": 3}),
                        'can restrict properties to those named in an array')
        result = _.pick({"a": 1, "b": 2, "c": 3}, ['a'], 'b')
        self.assertTrue(_.isEqual(result, {"a": 1, "b": 2}),
                        'can restrict properties to those named in mixed args')

    def test_omit(self):
        result = _.omit({"a": 1, "b": 2, "c": 3}, 'b')
        self.assertEqual(result, {"a": 1, "c": 3},
                         'can omit a single named property')
        result = _.omit({"a": 1, "b": 2, "c": 3}, 'a', 'c')
        self.assertEqual(result, {"b": 2}, 'can omit several named properties')
        result = _.omit({"a": 1, "b": 2, "c": 3}, ['b', 'c'])
        self.assertEqual(result, {"a": 1},
                         'can omit properties named in an array')

    def test_defaults(self):

        options = {"zero": 0, "one": 1, "empty":
                   "", "nan": None, "string": "string"}

        _.defaults(options, {"zero": 1, "one": 10, "twenty": 20})
        self.assertEqual(options["zero"], 0, 'value exists')
        self.assertEqual(options["one"], 1, 'value exists')
        self.assertEqual(options["twenty"], 20, 'default applied')

        _.defaults(options, {"empty": "full"},
                   {"nan": "none"}, {"word": "word"}, {"word": "dog"})
        self.assertEqual(options["empty"], "", 'value exists')
        self.assertTrue(_.isNone(options["nan"]), "NaN isn't overridden")
        self.assertEqual(options["word"], "word",
                         'new value is added, first one wins')

    def test_clone(self):
        moe = {"name": 'moe', "lucky": [13, 27, 34]}
        clone = _.clone(moe)
        self.assertEqual(clone["name"], 'moe',
                         'the clone as the attributes of the original')

        clone["name"] = 'curly'
        self.assertTrue(clone["name"] == 'curly' and moe["name"] == 'moe',
                        'clones can change shallow attributes'
                        ' without affecting the original')

        clone["lucky"].append(101)
        self.assertEqual(_.last(moe["lucky"]), 101,
                         'changes to deep attributes are'
                         ' shared with the original')

        self.assertEqual(_.clone(1), 1,
                         'non objects should not be changed by clone')
        self.assertEqual(_.clone(None), None,
                         'non objects should not be changed by clone')

    def test_isEqual(self):
        obj = {"a": 1, "b": 2}
        self.assertTrue(_.isEqual(obj, {"a": 1, "b": 2}), "Object is equal")
        obj = {"a": 1, "b": {"c": 2, "d": 3, "e": {"f": [1, 2, 3, 4, 5]}}}
        self.assertTrue(_.isEqual(
            obj, {"a": 1, "b": {"c": 2, "d": 3, "e": {"f": [1, 2, 3, 4, 5]}}}),
            "Object is equal")
        obj = [1, 2, 3, 4, [5, 6, 7, [[[[8]]]]]]
        self.assertTrue(
            _.isEqual(obj, [1, 2, 3, 4, [5, 6, 7, [[[[8]]]]]]),
            "Object is equal")
        obj = None
        self.assertTrue(_.isEqual(obj, None), "Object is equal")
        obj = 1
        self.assertTrue(_.isEqual(obj, 1), "Object is equal")
        obj = "string"
        self.assertTrue(_.isEqual(obj, "string"), "Object is equal")

    def test_isEmpty(self):
        self.assertTrue(not _([1]).isEmpty(), '[1] is not empty')
        self.assertTrue(_.isEmpty([]), '[] is empty')
        self.assertTrue(not _.isEmpty({"one": 1}), '{one : 1} is not empty')
        self.assertTrue(_.isEmpty({}), '{} is empty')
        self.assertTrue(_.isEmpty(None), 'null is empty')
        self.assertTrue(_.isEmpty(), 'undefined is empty')
        self.assertTrue(_.isEmpty(''), 'the empty string is empty')
        self.assertTrue(not _.isEmpty('moe'), 'but other strings are not')

        obj = {"one": 1}
        obj.pop("one")
        self.assertTrue(_.isEmpty(obj),
                        'deleting all the keys from an object empties it')
        pass

    def test_isType(self):
        # put all the types here and check each for true
        pass

    class Namespace:
        pass

    def test_tap(self):
        ns = self.Namespace()
        ns.intercepted = None

        def interceptor(obj):
            ns.intercepted = obj

        returned = _.tap(1, interceptor)
        self.assertEqual(ns.intercepted, 1,
                         "passes tapped object to interceptor")
        self.assertEqual(returned, 1, "returns tapped object")

        returned = _([1, 2, 3]).chain().map(
            lambda n, *args: n * 2).max().tap(interceptor).value()
        self.assertTrue(returned == 6 and ns.intercepted == 6,
                        'can use tapped objects in a chain')

    def test_pairs(self):
        r = _.pairs({"one": 1, "two": 2})
        self.assertEqual(sorted(r), [["one", 1], ["two", 2]],
                         'can convert an object into pairs')

    def test_invert(self):
        obj = {"first": 'Moe', "second": 'Larry', "third": 'Curly'}
        r = _(obj).chain().invert().keys().join(' ').value()
        self.assertEqual(set(r), set('Larry Moe Curly'),
                         'can invert an object')
        self.assertEqual(_.invert(_.invert(obj)), obj,
                         "two inverts gets you back where you started")

    def test_matches(self):
        moe = {"name": 'Moe Howard', "hair": True}
        curly = {"name": 'Curly Howard', "hair": False}
        stooges = [moe, curly]
        self.assertTrue(_.find(stooges, _.matches({"hair": False})) == curly,
                        "returns a predicate that can"
                        " be used by finding functions.")
        self.assertTrue(_.find(stooges, _.matches(moe)) == moe,
                        "can be used to locate an object"
                        " exists in a collection.")

if __name__ == "__main__":
    print("run these tests by executing `python -m unittest"
          " discover` in unittests folder")
    unittest.main()
