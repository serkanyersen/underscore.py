#!/usr/bin/env python
import inspect
try:
    import idc
    import idautils
    import idaapi
    #  from sftools import get_ea_by_any
except ImportError:
    pass
from types import *
import re
import functools
import random
import time
from threading import Timer
from collections import Sequence
import six
from six.moves import builtins

def oget(obj, key, default=None, call=False):
    """Get attribute or dictionary value of object
    Parameters
    ----------
    obj : object
        container with optional dict-like properties
    key : str
        key
    default : any
        value to return on failure
    call : bool
        call attr if callable

    Returns
    -------
    any
        similar to obj[key] or getattr(obj, key)

    See Also
    --------
    dotted : creates `path` from dotted string
    deep_get : uses `oget` to traverse deeply nested objects

    Examples
    --------
    >>> oget(sys.modules, '__main__')
    <module '__main__' (built-in)>
    >>> oget(sys.modules['__main__'], 'oget')
    <function oget at 0x000001A9A1920378>
    """
    if not isinstance(key, str):
        raise TypeError("oget(): attribute ('{}') name must be string".format(key))
    r = None

    if isinstance(obj, dict):
        return obj.get(key, default)
    try:
        r = obj[key] if key in obj else getattr(obj, key, default)
    except TypeError:
        # TypeError: 'module' object is not subscriptable
        r = getattr(obj, key, default)

    if call and callable(r):
        r = r()

    return r

# https://stackoverflow.com/questions/42095393/python-map-a-function-over-recursive-iterables
def _recursive_map(seq, func):
    for item in seq:
        if isinstance(item, Sequence):
            yield type(item)(_recursive_map(item, func))
        else:
            yield func(item)

def _recursive_obj_map(seq, func):
    for key, item in _.items(seq):
        if isinstance(item, Sequence):
            yield key, type(item)(_recursive_map(item, func))
        elif isinstance(item, Collection):
            yield key, type(item)(_recursive_map(item, func))
        else:
            yield func(item)

def _recursive_obj_map_wrapper(seq, func):
    return type(seq)(next(_recursive_obj_map(seq, func)))


def _makeSequenceMapper(f):
    def fmap(seq, iteratee):
        return _recursive_map(seq, iteratee)
    def function(item):
        if str(type(item)) == "<class 'generator'>":
            return [f(x) for x in item]
        if isinstance(item, Sequence):
            return type(item)(fmap(item, f))
        return [f(item)]
    return function

# An iterable object is an object that implements __iter__, which is expected
# to return an iterator object.
def _isIterable(o):
    return hasattr(o, '__iter__') and not hasattr(o, 'ljust')



__asList = _makeSequenceMapper(lambda x: x)
def _asList(o):
    l = []
    if _isIterable(o):
        l = [x for x in o]
    else:
        l = __asList(o)

    if not isinstance(l, list) or len(l) == 1 and l[0] == o:
        return [o]
    return l


def Array(o):
    if o is None:
        return []
    elif isinstance(o, list):
        return o
    else:
        return list([o])

def _us_xrefs_to(ea, types=None):

    if types is None:
        types = [ idc.fl_CF,
                         idc.fl_CN,
                         idc.fl_JF,
                         idc.fl_JN,
                       # idc.fl_F 
                       ]

    return [x.frm for x in idautils.XrefsTo(ea)]

class _IdCounter(object):

    """ Array Global Dictionary for uniq IDs
    """
    count = 0
    pass


class __(object):

    """
    Use this class to alter __repr__ of
    underscore object. So when you are using
    it on your project it will make sense
    """

    def __init__(self, repr, func):
        self._repr = repr
        self._func = func
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kw):
        return self._func(*args, **kw)

    def __repr__(self):
        return self._repr(self._func)


def u_withrepr(reprfun):
    """ Decorator to rename a function
    """
    def _wrap(func):
        return __(reprfun, func)
    return _wrap


@u_withrepr(lambda x: "<Underscore Object>")
def _(obj):
    """
    _ function, which creates an instance of the underscore object,
    We will also assign all methods of the underscore class as a method
    to this function so that it will be usable as a static object
    """
    return underscore(obj)


class underscore(object):

    fns = dict()

    """
    Instead of creating a class named _ (underscore) I created underscore
    So I can use _ function both statically and dynamically just as it
    is in the original underscore
    """

    _object = None
    """ Passed object
    """

    VERSION = "0.1.6"

    chained = False
    """ If the object is in a chained state or not
    """

    Null = "__Null__"
    """
    Since we are working with the native types
    I can't compare anything with None, so I use a Substitute type for checking
    """

    _wrapped = Null
    """
    When object is in chained state, This property will contain the latest
    processed Value of passed object, I assign it no Null so I can check
    against None results
    """

    def __init__(self, obj):
        """ Let there be light
        """
        self.chained = False
        self._object = obj

        class Namespace(object):

            """ For simulating full closure support
            """
            pass

        self.Namespace = Namespace

    def __str__(self):
        if self.chained is True:
            return "Underscore chained instance"
        else:
            return "Underscore instance"

    def __repr__(self):
        if self.chained is True:
            return "<Underscore chained instance>"
        else:
            return "<Underscore instance>"

    @property
    def obj(self):
        """
        Returns passed object but if chain method is used
        returns the last processed result
        """
        if self._wrapped is not self.Null:
            return self._wrapped
        else:
            return self._object

    @obj.setter
    def obj(self, value):
        """ New style classes requires setters for @propert methods
        """
        self._object = value
        return self._object

    def _wrap(self, ret):
        """
        Returns result but ig chain method is used
        returns the object itself so we can chain
        """
        if self.chained:
            self._wrapped = ret
            return self
        else:
            return ret

    @property
    def _clean(self):
        """
        creates a new instance for Internal use to prevent problems
        caused by chaining
        """
        return _(self.obj)

    def _toOriginal(self, val):
        """ Pitty attempt to convert itertools result into a real object
        """
        if self._clean.isTuple():
            return tuple(val)
        elif self._clean.isList():
            return list(val)
        elif self._clean.isDict():
            return dict(val)
        else:
            return val

    def _oget(self, obj, key, default=None, call=False):
        return oget(obj, key, default=default, call=call)
        """Get attribute or dictionary value of object
        Parameters
        ----------
        obj : object
            container with optional dict-like properties
        key : str
            key
        default : any
            value to return on failure
        call : bool
            call attr if callable

        Returns
        -------
        any
            similar to obj[key] or getattr(obj, key)

        See Also
        --------
        dotted : creates `path` from dotted string
        deep_get : uses `oget` to traverse deeply nested objects

        Examples
        --------
        >>> oget(sys.modules, '__main__')
        <module '__main__' (built-in)>
        >>> oget(sys.modules['__main__'], 'oget')
        <function oget at 0x000001A9A1920378>
        """
        if not isString(key):
            raise TypeError("oget(): attribute ('{}') name must be string".format(key))
        r = None
        try:
            r = obj[key] if key in obj else default
        except TypeError:
            # TypeError: 'module' object is not subscriptable
            r = getattr(obj, key, default)

        if call and callable(r):
            r = r()

        return r



    """
    Collection Functions
    """
    def items(self):
        """
        generator: iterates through each item of an dict or list, 
        using index for a key if not a dict. same as:
        enumerate(list) or dict.items()
        """
        if self.hasCallable('items'):
            for key, value in self._clean.obj.items():
                yield key, value
        else:
            for key, value in enumerate(self._clean.obj):
                yield key, value

    def each(self, func):
        """
        iterates through each item of an object
        :Param: func iterator function

        underscore.js:
        Iterates over a list of elements, yielding each in turn to an iteratee
        function. The iteratee is bound to the context object, if one is
        passed. Each invocation of iteratee is called with three arguments:
            (element, index, list). 
        If list is a JavaScript object, iteratee's arguments will be (value,
        key, list). Returns the list for chaining.
        """
        if callable(getattr(self._clean.obj, 'items', None)):
            for key, value in self.obj.items():
                r = func(value, key, self.obj)
                if r == "breaker":
                    break
        else:
            for index, value in enumerate(self.obj):
                r = func(value, index, self.obj)
                if r == "breaker":
                    break
        return self._wrap(self)
    forEach = each

    def mapObject(self, func):
        """ Return the results of applying the iterator to each element.
        """
        newlist = {}
        for k, v in self._clean.items():
            # if k not in values:  # use indexof to check identity
            k2, v2 = func(v, k, self.obj)
            newlist[k2] = v2

        return self._wrap(newlist)

    def map(self, func=None):
        """ Return the results of applying the iterator to each element.
        """
        if func is None:
            func = lambda x, *a: x

        ns = self.Namespace()
        ns.results = []

        def by(value, index, list, *args):
            ns.results.append(func(value, index, list))

        _(self.obj).each(by)
        return self._wrap(ns.results)
    collect = map

    def reduce(self, func, memo=None):
        """
        **Reduce** builds up a single result from a list of values,
        aka `inject`, or foldl
        """
        if memo is None:
            memo = []
        ns = self.Namespace()
        ns.initial = True  # arguments.length > 2
        ns.memo = memo
        obj = self.obj

        def by(value, index, *args):
            if not ns.initial:
                ns.memo = value
                ns.initial = True
            else:
                ns.memo = func(ns.memo, value, index)

        _(obj).each(by)
        return self._wrap(ns.memo)
    foldl = inject = reduce

    def reduceRight(self, func):
        """ The right-associative version of reduce, also known as `foldr`.
        """
        #foldr = lambda f, i: lambda s: reduce(f, s, i)
        x = self.obj[:]
        x.reverse()
        return self._wrap(functools.reduce(func, x))
    foldr = reduceRight

    def find(self, func):
        """
        Return the first value which passes a truth test.
        Aliased as `detect`.
        """
        self.ftmp = None

        def test(value, index, list):
            if func(value, index, list) is True:
                self.ftmp = value
                return True
        self._clean.any(test)
        return self._wrap(self.ftmp)
    detect = find

    def findKey(self, predicate):
        keys = self._clean.keys()
        for key in keys:
            if predicate(self.obj[key], key, self.obj):
                return self._wrap(key)

    def filterObject(self, func):
        """ Return all the items that pass a truth test
        """

        if self._clean.isDictlike():
            # https://stackoverflow.com/questions/2844516/how-to-filter-a-dictionary-according-to-an-arbitrary-condition-function
            # method a: {k: v for k, v in r.items() if not v['data'].startswith('False')}; 
            # method b: dict((k, v) for k, v in r.items() if not v['data'].startswith('False'))
            return self._wrap(type(self.obj)((k, v) for k, v in self.items() if func(v, k, self._clean.obj)))

        return self._wrap(type(self.obj)(v for k, v in self.items() if func(v, k, self._clean.obj)))


    def filter(self, func=lambda x, *a: not not x):
        """ Return all the elements that pass a truth test.
        """
        return self._wrap(list(filter(func, self.obj)))

    select = filter

    def remove(self, func):
        """ 
        Removes all elements from array that predicate returns truthy for
        and returns an array of the removed elements. The predicate is invoked
        with three arguments: (value, index, array).
        """
        ns = self.Namespace()
        ns.remove = []
        ns.result = []
        obj = self.obj

        def by(value, index, list):
            if func(value, index, list):
                ns.remove.append(index)
                ns.result.append(value)

        _(obj).each(by)
        ns.remove.reverse()

        for index in ns.remove:
            try:
                self.obj.pop(index)
            except ValueError:
                print("{} is not in {}".format(index, self.obj))

        return self._wrap(ns.result)


    def without(self, *values):
        """
        Return a version of the array that does not contain the specified
        value(s), or object that doesn't contain the specified key(s)
        """
        if self._clean.isDict():
            newlist = {}
            for i, k in enumerate(self.obj):
                # if k not in values:  # use indexof to check identity
                if _(values).indexOf(k) == -1:
                    newlist[k] = self.obj[k]
        else:
            newlist = []
            for i, v in enumerate(self.obj):
                # if v not in values:  # use indexof to check identity
                if _(values).indexOf(v) == -1:
                    newlist.append(v)

        return self._wrap(newlist)

    def only(self, *values):
        """
        Return a version of the array that only contains the specified
        value(s), or object that only contains the specified key(s)
        """
        if self._clean.isDictlike():
            newlist = {}
            for i, k in enumerate(self.obj):
                # if k not in values:  # use indexof to check identity
                if _(values).indexOf(k) != -1:
                    newlist[k] = self.obj[k]
        else:
            newlist = []
            for i, v in enumerate(self.obj):
                # if v not in values:  # use indexof to check identity
                if _(values).indexOf(v) != -1:
                    newlist.append(v)

        return self._wrap(newlist)



    def reject(self, func):
        """ Return all the elements for which a truth test fails.
        """
        return self._wrap(list(filter(lambda val: not func(val), self.obj)))

    def all(self, func=lambda x, *a: not not x):
        """ Determine whether all of the elements match a truth test.
        """
        self.altmp = True

        def testEach(value, index, *args):
            if func(value, index, *args) is False:
                self.altmp = False

        self._clean.each(testEach)
        return self._wrap(self.altmp)
    every = all

    def same(self):
        """ 
        Determine if all of the elements hold the same value. Returns False
        if there are no elements.
        """
        if not self._clean.obj or not len(self._clean.obj):
            return False
        _first = _.first(self._clean.obj)
        return self.all(lambda x, *a: x == _first)
        


    def any(self, func=lambda x, *a: not not x):
        """
        Determine if at least one element in the object
        matches a truth test.
        """
        self.antmp = False

        def testEach(value, index, *args):
            if func(value, index, *args):
                self.antmp = True
                return "breaker"

        self._clean.each(testEach)
        return self._wrap(self.antmp)
    some = any

    def include(self, target):
        """
        Determine if a given value(s) is included in the
        array or object using `is`.
        """
        target = _asList(target)

        if self._clean.isDict():
            return self._wrap(_.any(target, lambda x, *a: x in self.obj.values()))
        else:
            return self._wrap(_.any(target, lambda x, *a: x in self.obj))
    contains = include

    def invoke(self, method, *args):
        """ Invoke a method (with arguments) on every item in a collection.
        """
        def inv(value, *ar):
            if (
                _(method).isFunction() or
                _(method).isLambda() or
                _(method).isMethod()
            ):
                return method(value, *args)
            else:
                return getattr(value, method)(*args)
        return self._wrap(self._clean.map(inv))

    def pluck(self, key):
        """
        Convenience version of a common use case of
        `map`: fetching a property.
        """

        # allow pluck to operate on numeric indexes to quickly
        # grab items from tuples and lists
        if _.isInt(key):
            return list(list(zip(*self.obj))[key])

        if _.isList(key) or _.isTuple(key) and len(key) == 2:
            r1 = []
            for x in self.obj:
                r2 = []
                for _key in key:
                    r2.append(self._oget(x, _key, call=1))
                r1.append(tuple(r2))
            return(r1) 

        return self._wrap([self._oget(x, key, call=1) for x in self.obj])

    def re_findall(self, pattern, flags=0):
        """
        Return a list of all non-overlapping matches in the string.
        
        If one or more capturing groups are present in the pattern, return
        a list of groups; this will be a list of tuples if the pattern
        has more than one group.
        
        Empty matches are included in the result.
        """
        results = []
        for ob in Array(self.obj):
            results.extend(re.findall(pattern, ob))

        return self._wrap(results)


    # _([idc.get_screen_ea()]).chain().
    #    code_refs_to().
    #    func_start().
    #    code_refs_to().
    #    map(lambda x, *y: GetFunctionName(x)).filter(lambda x, *y: x.startswith('sub_')).
    #    invoke(lambda x, *y: LabelAddressPlus(LocByName( x ), 'allocsub_%s' % x[4:]))
    def ida_code_refs_to(self):
        return self._wrap(self._flatten(_(asList(self.obj)).map(lambda x, *y: asList(idautils.CodeRefsTo(x, 0))), shallow=True))

    def ida_func_start(self):
        return self._wrap(self._flatten(_(asList(self.obj)).map(lambda x, *y: GetFuncStart(x)), shallow=True))

    def ida_decompile(self):
        return self._wrap([str(idaapi.decompile(get_ea_by_any(e), hf=None, flags=idaapi.DECOMP_WARNINGS)) for e in self.obj])

    def ida_xrefs_to(self):
        return self._wrap([_us_xrefs_to(get_ea_by_any(e)) for e in self.obj])

    def ida_all_xrefs_from(self):
        def iter(x):
            if x[2] == 'fl_CN':
                return x[0]
            return None
        return self._wrap(_.uniq(_.filter(self._flatten(self.obj + [all_xrefs_from(get_ea_by_any(e), iteratee=iter) for e in self.obj]), lambda x, *a: x)))

    def where(self, attrs=None, first=False):
        """
        Convenience version of a common use case of `filter`:
        selecting only objects
        containing specific `key:value` pairs.
        """
        if attrs is None:
            return None if first is True else []

        method = _.find if first else _.filter

        def by(val, *args):
            for key, value in attrs.items():
                try:
                    if attrs[key] != val[key]:
                        return False
                except KeyError:
                    return False
                return True

        return self._wrap(method(self.obj, by))

    def findWhere(self, attrs=None):
        """
        Convenience version of a common use case of `find`:
        getting the first object
        containing specific `key:value` pairs.
        """
        return self._wrap(self._clean.where(attrs, True))

    def max(self):
        """ Return the maximum element or (element-based computation).
        """
        if(self._clean.isDict()):
            return self._wrap(list())
        return self._wrap(max(self.obj))

    def maxBy(self, key):
        """ Return the maximum element or (element-based computation).
        """
        if(self._clean.isDict()):
            return self._wrap(list())
        return self._wrap(max(self.obj, key=key))


    def min(self):
        """ Return the minimum element (or element-based computation).
        """
        if(self._clean.isDict()):
            return self._wrap(list())
        return self._wrap(min(self.obj))

    def minBy(self, key):
        """ Return the minimum element or (element-based computation).
        """
        if(self._clean.isDict()):
            return self._wrap(list())
        return self._wrap(min(self.obj, key=key))

    def shuffle(self):
        """ Shuffle an array.
        """
        if(self._clean.isDict()):
            return self._wrap(list())

        cloned = self.obj[:]

        random.shuffle(cloned)
        return self._wrap(cloned)

    def reverse(self):
        cloned = self.obj[:]
        cloned.reverse()
        return self._wrap(cloned)

    def sort(self, val=None):
        """ Sort the object's values by a criterion produced by an iterator.
        """
        if val is not None:
                return self._wrap(sorted(self.obj, cmp=val))
        else:
            return self._wrap(sorted(self.obj))

    def sortBy(self, val=None):
        """ 
        Sort the object's values by a criterion produced by an iterator or
        attribute name.
        """
        #  def get(obj, key):
            #  if callable(getattr(obj, 'get', None)):
                #  return obj.get(key)
            #  return getattr(obj, key)

        if val is not None:
            if _(val).isString():
                return self._wrap(sorted(self.obj, key=lambda x,
                                  *args: _.get(x, val)))
            else:
                return self._wrap(sorted(self.obj, key=val))
        else:
            return self._wrap(sorted(self.obj))

    def sortObjectBy(self, val=None, reverse=None):
        """ Sort the object's values by a criterion produced by an iterator.
        """
        keys = _.sortBy(self.obj, val)
        if reverse:
            keys.reverse()
        o = {}
        for k in keys:
            o[k] = self.obj[k]
        return self._wrap(o)

    def _lookupIterator(self, val):
        """ An internal function to generate lookup iterators.
        """
        if val is None:
            return lambda el, *args: el
        return val if _.isCallable(val) else lambda obj, *args: obj[val]

    def _group(self, obj, val, behavior):
        """ An internal function used for aggregate "group by" operations.
        """
        ns = self.Namespace()
        ns.result = {}
        iterator = self._lookupIterator(val)

        def e(value, index, *args):
            key = iterator(value, index)
            behavior(ns.result, key, value)

        _.each(obj, e)

        if False:
            if len(ns.result) == 1:
                try:
                    return ns.result[0]
                except KeyError:
                    return list(ns.result.values())[0]
        return ns.result

    def groupBy(self, val):
        """
        Groups the object's values by a criterion. Pass either a string
        attribute to group by, or a function that returns the criterion.
        """

        def by(result, key, value):
            if key not in result:
                result[key] = []
            result[key].append(value)

        res = self._group(self.obj, val, by)

        return self._wrap(res)

    def grouper(self, n, fillvalue=None):
        """
        https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks/312644#312644
        > grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')
        """
        # from itertools import zip_longest # for Python 3.x
        from six.moves import zip_longest # for both (uses the six compat library)
        return zip_longest(*[iter(self.obj)]*n, fillvalue=fillvalue)

    def indexBy(self, val=None):
        """
        Indexes the object's values by a criterion, similar to
        `groupBy`, but for when you know that your index values will be unique.
        """
        if val is None:
            val = lambda *args: args[0]

        def by(result, key, value):
            result[key] = value

        res = self._group(self.obj, val, by)

        return self._wrap(res)

    def countBy(self, val):
        """
        Counts instances of an object that group by a certain criterion. Pass
        either a string attribute to count by, or a function that returns the
        criterion.
        """

        def by(result, key, value):
            if key not in result:
                result[key] = 0
            result[key] += 1

        res = self._group(self.obj, val, by)

        return self._wrap(res)

    def sortedIndex(self, obj, iterator=lambda x: x):
        """
        Use a comparator function to figure out the smallest index at which
        an object should be inserted so as to maintain order.
        Uses binary search.
        """
        array = self.obj
        value = iterator(obj)
        low = 0
        high = len(array)
        while low < high:
            mid = (low + high) >> 1
            if iterator(array[mid]) < value:
                low = mid + 1
            else:
                high = mid
        return self._wrap(low)

    def toArray(self):
        """ Safely convert anything iterable into a real, live array.
        """
        return self._wrap(list(self.obj))

    def size(self):
        """ Return the number of elements in an object.
        """
        return self._wrap(len(self.obj))

    def first(self, n=1):
        """
        Get the first element of an array. Passing **n** will return the
        first N values in the array. Aliased as `head` and `take`.
        The **guard** check allows it to work with `_.map`.
        """
        keys = _.keys(self.obj)[0:n]
        res = [self.obj[x] for x in keys]
        if len(res) == 1:
            res = res[0]

        #  keys = getattr(self.obj, 'keys', None)
        #  res = []
        #  for i, v in enumerate(self.obj):
            #  if i >= n:
                #  break
            #  res.append(v)
        return self._wrap(res)
    head = take = first

    def initial(self, n=1):
        """
        Returns everything but the last entry of the array.
        Especially useful on the arguments object.
        Passing **n** will return all the values in the array, excluding the
        last N. The **guard** check allows it to work with `_.map`.
        """
        return self._wrap(self.obj[0:-n])

    def last(self, n=1):
        """
        Get the last element of an array. Passing **n** will return the last N
        values in the array.
        The **guard** check allows it to work with `_.map`.
        """
        res = self.obj[-n:]
        if len(res) == 1:
            res = res[0]
        return self._wrap(res)

    def rest(self, n=1):
        """
        Returns everything but the first entry of the array. Aliased as `tail`.
        Especially useful on the arguments object.
        Passing an **index** will return the rest of the values in the
        array from that index onward.
        The **guard** check allows it to work with `_.map`.
        """
        return self._wrap(self.obj[n:])
    tail = rest

    def compact(self):
        """ Trim out all falsy values from an array.
        """
        return self._wrap(self._clean.filter(lambda x: x))

    def _flatten(self, input, shallow=False, output=None):
        ns = self.Namespace()
        ns.output = output
        if ns.output is None:
            ns.output = []

        def by(value, *args):
            if _.isList(value) or _.isTuple(value):
                if shallow:
                    ns.output = ns.output + value
                else:
                    self._flatten(value, shallow, ns.output)
            else:
                ns.output.append(value)

        _.each(input, by)

        return ns.output

    def flatten(self, shallow=None):
        """ Return a completely flattened version of an array.
        """
        return self._wrap(self._flatten(self.obj, shallow))

    def partition(self, predicate=None):
        """
        Split an array into two arrays: one whose elements all satisfy the given
        predicate, and one whose elements all do not satisfy the predicate.
        """
        predicate = self._lookupIterator(predicate)
        pass_list = []
        fail_list = []

        def by(elem, index, *args):
            (pass_list if predicate(elem) else fail_list).append(elem)

        _.each(self.obj, by)

        return self._wrap([pass_list, fail_list])

    def uniq(self, isSorted=False, iterator=None):
        """
        Produce a duplicate-free version of the array. If the array has already
        been sorted, you have the option of using a faster algorithm.
        Aliased as `unique`.
        """
        ns = self.Namespace()
        ns.results = []
        ns.array = self.obj
        initial = self.obj
        if iterator is not None:
            initial = _(ns.array).map(iterator)

        def by(memo, value, index):
            if ((_.last(memo) != value or
                 not len(memo)) if isSorted else not _.include(memo, value)):
                memo.append(value)
                ns.results.append(ns.array[index])

            return memo

        ret = _.reduce(initial, by)
        return self._wrap(ret)
        # seen = set()
        # seen_add = seen.add
        # ret = [x for x in seq if x not in seen and not seen_add(x)]
        # return self._wrap(ret)
    unique = uniq

    def sum(self, iterator=None, initial=0):
        """
        Add shit up -- todo
        """

        def by(memo, value, index):
            # lambda memo, value, index: memo + len(value), 0)
            if callable(iterator):
                return memo + iterator(value)
            return memo + value

        ret = _.reduce(self.obj, by, initial)
        return self._wrap(ret)

    def union(self, *args):
        """
        Produce an array that contains the union: each distinct element
        from all of the passed-in arrays.
        """
        # setobj = set(self.obj)
        # for i, v in enumerate(args):
        #     setobj = setobj + set(args[i])
        # return self._wrap(self._clean._toOriginal(setobj))
        args = list(args)
        args.insert(0, self.obj)
        return self._wrap(_.uniq(self._flatten(args, True, [])))

    def intersection(self, *args):
        """
        Produce an array that contains every item shared between all the
        passed-in arrays.
        """
        if type(self.obj[0]) is int:
            a = self.obj
        else:
            a = tuple(self.obj[0])
        setobj = set(a)
        for i, v in enumerate(args):
            setobj = setobj & set(args[i])
        return self._wrap(list(setobj))

    def difference(self, *args):
        """
        Take the difference between one array and a number of other arrays.
        Only the elements present in just the first array will remain.
        """
        setobj = set(self.obj)
        for i, v in enumerate(args):
            setobj = setobj - set(args[i])
        return self._wrap(self._clean._toOriginal(setobj))

    def zip(self, *args):
        """
        Zip together multiple lists into a single array -- elements that share
        an index go together.
        """
        args = list(args)
        args.insert(0, self.obj)
        maxLen = _(args).chain().collect(lambda x, *args: len(x)).max().value()
        for i, v in enumerate(args):
            l = len(args[i])
            if l < maxLen:
                args[i]
            for x in range(maxLen - l):
                args[i].append(None)
        return self._wrap(zip(*args))

    def object(self, values=None, manyValues=None):
        """
        Zip together two arrays -- an array of keys and an array
        of values -- into a single object. Or pass a single array 
        of `[key, value]` (the reverse of `_.pairs`)

        Aliased as `fromPairs` (lodash) and `zipObject`

        @param manyValues bool: if True, input is `[key, value1, value2, ...]`
        and output will be `{key: [value1, value2, ...]}`
        """
        if _.isIntegral(values):
            values, manyValues = manyValues, values
        if manyValues:
            return self.mapObject(lambda v, k, *a: (v[0], v[1:]))

        result = {}
        keys = self.obj
        if values:
            i = 0
            l = len(keys)
            while i < l:
                result[keys[i]] = values[i]
                l = len(keys)
                i += 1
        else:
            for k, v in keys:
                result[k] = v;

        return self._wrap(result)

    fromPairs = zipObject = object

    def indexOf(self, item, isSorted=False):
        """
        Return the position of the first occurrence of an
        item in an array, or -1 if the item is not included in the array.
        """
        array = self.obj
        ret = -1

        if not (self._clean.isList() or self._clean.isTuple()):
            return self._wrap(-1)

        if isSorted:
            i = _.sortedIndex(array, item)
            ret = i if array[i] is item else -1
        else:
            i = 0
            l = len(array)
            while i < l:
                # array[i] is item -- fails under py3
                if array[i] == item:
                    return self._wrap(i)
                i += 1
        return self._wrap(ret)

    def lastIndexOf(self, item):
        """
        Return the position of the last occurrence of an
        item in an array, or -1 if the item is not included in the array.
        """
        array = self.obj
        i = len(array) - 1
        if not (self._clean.isList() or self._clean.isTuple()):
            return self._wrap(-1)

        while i > -1:
            if array[i] is item:
                return self._wrap(i)
            i -= 1
        return self._wrap(-1)

    def range(self, *args):
        """ Generate an integer Array containing an arithmetic progression.
        """
        args = list(args)
        args.insert(0, self.obj)
        return self._wrap(range(*args))

    """
    Function functions
    """

    def bind(self, context):
        """
        Create a function bound to a given object (assigning `this`,
        and arguments, optionally).
        Binding with arguments is also known as `curry`.
        """
        return self._wrap(self.obj)
    curry = bind

    def partialx(func, *args):
        def part(*args_rest):
            return func(*(args + args_rest)) 
        return part

    def partial(self, *args):
        """
        Partially apply a function by creating a version that has had some of
        its arguments pre-filled, without changing its dynamic `this` context.
        """
        def part(*args2):
            args3 = args + args2
            return self.obj(*args3)

        return self._wrap(part)

    def bindAll(self, *args):
        """
        Bind all of an object's methods to that object.
        Useful for ensuring that all callbacks defined on an
        object belong to it.
        """
        return self._wrap(self.obj)

    def memoize(self, hasher=None):
        """ Memoize an expensive function by storing its results.
        """
        ns = self.Namespace()
        ns.memo = {}
        if hasher is None:
            hasher = lambda x: x

        def memoized(*args, **kwargs):
            key = hasher(*args)
            if key not in ns.memo:
                ns.memo[key] = self.obj(*args, **kwargs)
            return ns.memo[key]

        return self._wrap(memoized)

    def delay(self, wait, *args):
        """
        Delays a function for the given number of milliseconds, and then calls
        it with the arguments supplied.
        """

        def call_it():
            self.obj(*args)

        t = Timer((float(wait) / float(1000)), call_it)
        t.start()
        return self._wrap(self.obj)

    def defer(self, *args):
        """
        Defers a function, scheduling it to run after
        the current call stack has cleared.
        """
        # I know! this isn't really a defer in python. I'm open to suggestions
        return self.delay(1, *args)

    def throttle(self, wait):
        """
        Returns a function, that, when invoked, will only be triggered
        at most once during a given window of time.
        """
        ns = self.Namespace()
        ns.timeout = None
        ns.throttling = None
        ns.more = None
        ns.result = None

        def done():
            ns.more = ns.throttling = False

        whenDone = _.debounce(done, wait)
        wait = (float(wait) / float(1000))

        def throttled(*args, **kwargs):
            def later():
                ns.timeout = None
                if ns.more:
                    self.obj(*args, **kwargs)
                whenDone()

            if not ns.timeout:
                ns.timeout = Timer(wait, later)
                ns.timeout.start()

            if ns.throttling:
                ns.more = True
            else:
                ns.throttling = True
                ns.result = self.obj(*args, **kwargs)
            whenDone()
            return ns.result
        return self._wrap(throttled)

    # https://gist.github.com/2871026
    def debounce(self, wait, immediate=None):
        """
        Returns a function, that, as long as it continues to be invoked,
        will not be triggered. The function will be called after it stops
        being called for N milliseconds. If `immediate` is passed, trigger
        the function on the leading edge, instead of the trailing.
        """
        wait = (float(wait) / float(1000))

        def debounced(*args, **kwargs):
            def call_it():
                self.obj(*args, **kwargs)
            try:
                debounced.t.cancel()
            except(AttributeError):
                pass
            debounced.t = Timer(wait, call_it)
            debounced.t.start()
        return self._wrap(debounced)

    def once(self):
        """
        Returns a function that will be executed at most one time,
        no matter how often you call it. Useful for lazy initialization.
        """
        ns = self.Namespace()
        ns.memo = None
        ns.run = False

        def work_once(*args, **kwargs):
            if ns.run is False:
                ns.memo = self.obj(*args, **kwargs)
            ns.run = True
            return ns.memo

        return self._wrap(work_once)

    def wrap(self, wrapper):
        """
        Returns the first function passed as an argument to the second,
        allowing you to adjust arguments, run code before and after, and
        conditionally execute the original function.
        """
        def wrapped(*args, **kwargs):

            if kwargs:
                kwargs["object"] = self.obj
            else:
                args = list(args)
                args.insert(0, self.obj)

            return wrapper(*args, **kwargs)

        return self._wrap(wrapped)

    def compose(self, *args):
        """
        Returns a function that is the composition of a list of functions, each
        consuming the return value of the function that follows.
        """
        args = list(args)

        def composed(*ar, **kwargs):
            lastRet = self.obj(*ar, **kwargs)
            for i in args:
                lastRet = i(lastRet)

            return lastRet

        return self._wrap(composed)

    def after(self, func):
        """
        Returns a function that will only be executed after being
        called N times.
        """
        ns = self.Namespace()
        ns.times = self.obj

        if ns.times <= 0:
            return func()

        def work_after(*args):
            if ns.times <= 1:
                return func(*args)
            ns.times -= 1

        return self._wrap(work_after)

    """
    Object Functions
    """

    def keys(self):
        """ 
        Retrieve the names of an object's properties.
        (extended) will attempt to obtain some index list for non-objects, such
        that they can be used in slicing

        """
        #  keys = self.obj.keys()
        #  if type(keys) == "<class 'dict_keys'>":
            #  keys = [x for x in keys]
        if self._clean.isList() or self._clean.isTuple():
            return self._wrap(_.map(_.range(len(self.obj))))
        
        try:
            return self._wrap(list(self.obj.keys()))
        except AttributeError:
            return self._wrap(list(dir(self.obj)))

    def values(self):
        """ Retrieve the values of an object's properties.
        """
        return self._wrap(list(self.obj.values()))

    def pairs(self):
        """ Convert an object into a list of `[key, value]` pairs.

        Aliased as `toPairs`.
        """
        keys = self._clean.keys()
        pairs = []
        for key in keys:
            pairs.append([key, self.obj[key]])

        return self._wrap(pairs)

    toPairs = pairs

    def invert(self):
        """
        Invert the keys and values of an object.
        The values must be serializable.
        """
        keys = self._clean.keys()
        inverted = {}
        for key in keys:
            inverted[self.obj[key]] = key

        return self._wrap(inverted)

    def functions(self):
        """ Return a sorted list of the function names available on the object.
        """
        names = []

        for i, k in enumerate(self.obj):
            if _(self.obj[k]).isCallable():
                names.append(k)

        return self._wrap(sorted(names))
    methods = functions

    def extend(self, *args):
        """
        Extend a given object with all the properties in
        passed-in object(s).
        """
        #  args = list(args)
        """
        update(...)
            D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
            If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
            If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
            In either case, this is followed by: for k in F:  D[k] = F[k]
        """

        if hasattr(self.obj, 'update'):
            for i in args:
                self.obj.update(i)
        else:
            for i in args:
                if callable(getattr(i, 'keys', None)):
                    for k in i:
                        #  self.obj[k] = i[k]
                        setattr(self.obj, k, i[k])
                else:
                    for k, v in i:
                        #  self.obj[k] = v
                        setattr(self.obj, k, v)

        return self._wrap(self.obj)

    def pick(self, *args):
        """
        Return a copy of the object only containing the
        whitelisted properties.
        """
        ns = self.Namespace()
        ns.result = {}

        #  def by(key, *args):
            #  if key in self.obj:
                #  ns.result[key] = self.obj[key]

        def by(key, *args):
            if _.get(self.obj, key, 'nop6690') != 'nop6690':
                ns.result[key] = _.get(self.obj, key)

        _.each(self._flatten(args, True, []), by)
        return self._wrap(ns.result)

    def omit(self, *args):
        copy = {}
        keys = _(args).flatten()
        for i, key in enumerate(self.obj):
            if not _.include(keys, key):
                copy[key] = self.obj[key]

        return self._wrap(copy)

    def defaults(self, *args):
        """ Fill in a given object with default properties.
        """
        ns = self.Namespace
        ns.obj = self.obj

        def by(source, *ar):
            for i, prop in enumerate(source):
                if prop not in ns.obj:
                    ns.obj[prop] = source[prop]

        _.each(args, by)

        return self._wrap(ns.obj)

    def clone(self):
        """ Create a (shallow-cloned) duplicate of an object.
        """
        import copy
        return self._wrap(copy.copy(self.obj))

    def tap(self, interceptor):
        """
        Invokes interceptor with the obj, and then returns obj.
        The primary purpose of this method is to "tap into" a method chain, in
        order to perform operations on intermediate results within the chain.
        """
        interceptor(self.obj)
        return self._wrap(self.obj)

    def isEqual(self, match):
        """ Perform a deep comparison to check if two objects are equal.
        """
        return self._wrap(self.obj == match)

    def isEmpty(self):
        """
        Is a given array, string, or object empty?
        An "empty" object has no enumerable own-properties.
        """
        if self.obj is None:
            return True
        if self._clean.isString():
            ret = self.obj.strip() == ""
        elif self._clean.isDict():
            ret = len(self.obj.keys()) == 0
        else:
            ret = len(self.obj) == 0
        return self._wrap(ret)

    def isElement(self):
        """ No use in python
        """
        return self._wrap(False)

    def isDict(self):
        """ Check if given object is a dictionary
        """
        return self._wrap(type(self.obj) is dict)

    def isTuple(self):
        """ Check if given object is a tuple
        """
        return self._wrap(type(self.obj) is tuple)

    def isList(self):
        """ Check if given object is a list
        """
        return self._wrap(type(self.obj) is list)

    def isNone(self):
        """ Check if the given object is None
        """
        return self._wrap(self.obj is None)

    def isType(self):
        """ Check if the given object is a type
        """
        return self._wrap(type(self.obj) is type)

    def isBoolean(self):
        """ Check if the given object is a boolean
        """
        return self._wrap(type(self.obj) is bool)
    isBool = isBoolean

    def isInt(self):
        """ Check if the given object is an int
        """
        return self._wrap(type(self.obj) is int)

    def isIntegral(self):
        """ Check if the given object is integral (from C++11)

        Checks whether T is an integral type. Provides the member constant
        value which is equal to true, if T is the type bool, char, char8_t
        (since C++20), char16_t, char32_t, wchar_t, short, int, long, long
        long, or any implementation-defined extended integer types, including
        any signed, unsigned, and cv-qualified variants. Otherwise, value is
        equal to false.
        """
        return self._wrap(isinstance(self.obj, (int,bool)))

    def isNumeric(self):
        """ Check if the given object is a number (float/int/bool)
        """
        return self._wrap(isinstance(self.obj, (int,bool,float)) or isinstance(self.obj, str) and re.match(r'^[0-9-+.eE]+$', self.obj))

    # :DEPRECATED: Python 2 only.
    # 3 removes this.
    def isLong(self):
        """ Check if the given object is a long
        """
        return self._wrap(type(self.obj) is long)

    def isFloat(self):
        """ Check if the given object is a float
        """
        return self._wrap(type(self.obj) is float)

    def isComplex(self):
        """ Check if the given object is a complex
        """
        return self._wrap(type(self.obj) is complex)

    def isString(self):
        """ Check if the given object is a string
        """
        return self._wrap(type(self.obj) is str)

    def isUnicode(self):
        """ Check if the given object is a unicode string
        """
        return self._wrap(type(self.obj) is unicode)

    def isCallable(self):
        """ Check if the given object is any of the function types
        """
        return self._wrap(callable(self.obj))

    def isFunction(self):
        """ Check if the given object is FunctionType
        """
        return self._wrap(type(self.obj) is FunctionType)

    def isLambda(self):
        """ Check if the given object is LambdaType
        """
        return self._wrap(type(self.obj) is LambdaType)

    def isGenerator(self):
        """ Check if the given object is GeneratorType
        """
        return self._wrap(type(self.obj) is GeneratorType)

    def isCode(self):
        """ Check if the given object is CodeType
        """
        return self._wrap(type(self.obj) is CodeType)

    def isClass(self):
        """ Check if the given object is ClassType
        """
        return self._wrap(inspect.isclass(self.obj))

    # :DEPRECATED: Python 2 only.
    # 3 removes this.
    def isInstance(self):
        """ Check if the given object is InstanceType
        """
        return self._wrap(type(self.obj) is InstanceType)

    def isMethod(self):
        """ Check if the given object is MethodType
        """
        return self._wrap(inspect.ismethod(self.obj))

    # :DEPRECATED: Python 2 only.
    # 3 removes this.
    def isUnboundMethod(self):
        """ Check if the given object is UnboundMethodType
        """
        return self._wrap(type(self.obj) is UnboundMethodType)

    def isBuiltinFunction(self):
        """ Check if the given object is BuiltinFunctionType
        """
        return self._wrap(type(self.obj) is BuiltinFunctionType)

    def isBuiltinMethod(self):
        """ Check if the given object is BuiltinMethodType
        """
        return self._wrap(type(self.obj) is BuiltinMethodType)

    def isModule(self):
        """ Check if the given object is ModuleType
        """
        return self._wrap(type(self.obj) is ModuleType)

    def isFile(self):
        """ Check if the given object is a file
        """
        try:
            filetype = file
        except NameError:
            filetype = io.IOBase

        return self._wrap(type(self.obj) is filetype)

    # :DEPRECATED: Python 2 only.
    # 3 removes this.
    def isXRange(self):
        """ Check if the given object is XRangeType
        """
        return self._wrap(type(self.obj) is XRangeType)

    def isSlice(self):
        """ Check if the given object is SliceType
        """
        return self._wrap(type(self.obj) is type(slice))

    def isEllipsis(self):
        """ Check if the given object is EllipsisType
        """
        return self._wrap(type(self.obj) is type(Ellipsis))

    def isTraceback(self):
        """ Check if the given object is TracebackType
        """
        return self._wrap(type(self.obj) is TracebackType)

    def isFrame(self):
        """ Check if the given object is FrameType
        """
        return self._wrap(type(self.obj) is FrameType)

    # :DEPRECATED: Python 2 only.
    # 3 uses memoryview.
    def isBuffer(self):
        """ Check if the given object is BufferType
        """
        return self._wrap(type(self.obj) is BufferType)

    # :DEPRECATED: Python 2 only.
    # 3 uses mappingproxy.
    def isDictProxy(self):
        """ Check if the given object is DictProxyType
        """
        return self._wrap(type(self.obj) is DictProxyType)

    def isNotImplemented(self):
        """ Check if the given object is NotImplementedType
        """
        return self._wrap(type(self.obj) is type(NotImplemented))

    def isGetSetDescriptor(self):
        """ Check if the given object is GetSetDescriptorType
        """
        return self._wrap(type(self.obj) is GetSetDescriptorType)

    def isMemberDescriptor(self):
        """ Check if the given object is MemberDescriptorType
        """
        return self._wrap(type(self.obj) is MemberDescriptorType)

    def has(self, key):
        """
        Shortcut function for checking if an object has a
        given property directly on itself (in other words, not on a prototype).
        """
        return self._wrap(hasattr(self.obj, key))

    def hasCallable(self, key):
        """
        Shortcut function for checking if an object has a
        given property that is callable
        """
        return self._wrap(callable(getattr(self.obj, key, None)))

    def get(self, key, _default=None):
        if callable(getattr(self.obj, 'get', None)):
            return self._wrap(self.obj.get(key, _default))
        return self._wrap(getattr(self.obj, key, _default))

    def getmanyattr(self, *args):
        """
        getmanyattr(object, name1[, name2 ,[name3 ,...]], default]) -> value
        
        Get many named attributes from an object; getmanyattr(x, 'y', 'z', None) is
        equivalent to [x.y, x.z].  The default argument (None) is returned when the
        attribute doesn't exist.
        """
        default = args[-1]
        return self._wrap([getattr(self.obj, key, default) for key in args[0:-1]])

    def isDictlike(self):
        return self._wrap(_.all(_.getmanyattr(self.obj, 'items', 'values', 'keys', 'get', None), lambda x, *a: callable(x)))

    @staticmethod
    def _isListlike(obj):
        return _.all(_.getmanyattr(obj, 'append', 'remove', '__len__', None), lambda x, *a: callable(x))

    def isListlike(self):
        return self._wrap(self._isListlike(self.obj))

    def join(self, glue=" "):
        """ Javascript's join implementation
        """
        j = glue.join([str(x) for x in self.obj])
        return self._wrap(j)

    def constant(self, *args):
        """ High order of identity
        """
        return self._wrap(lambda *args: self.obj)

    def identity(self, *args):
        """ Keep the identity function around for default iterators.
        """
        return self._wrap(self.obj)

    def property(self):
        """
        For easy creation of iterators that pull
        specific properties from objects.
        """
        return self._wrap(lambda obj, *args: obj[self.obj])

    def matches(self):
        """
        Returns a predicate for checking whether an object has a given
        set of `key:value` pairs.
        """
        def ret(obj, *args):
            if self.obj is obj:
                return True  # avoid comparing an object to itself.

            for key in self.obj:
                if self.obj[key] != obj[key]:
                    return False

            return True

        return self._wrap(ret)

    def times(self, func, *args):
        """ Run a function **n** times.
        """
        n = self.obj
        i = 0
        while n != 0:
            n -= 1
            func(i)
            i += 1

        return self._wrap(func)

    def now(self):
        return self._wrap(time.time())

    def random(self, max_number=None):
        """ Return a random integer between min and max (inclusive).
        """
        min_number = self.obj
        if max_number is None:
            min_number = 0
            max_number = self.obj
        return random.randrange(min_number, max_number)

    def result(self, property, *args):
        """
        If the value of the named property is a function then invoke it;
        otherwise, return it.
        """
        if self.obj is None:
            return self._wrap(self.obj)

        if(hasattr(self.obj, property)):
            value = getattr(self.obj, property)
        else:
            value = self.obj.get(property)
        if _.isCallable(value):
            return self._wrap(value(*args))
        return self._wrap(value)

    def mixin(self):
        """
        Add your own custom functions to the Underscore object, ensuring that
        they're correctly added to the OOP wrapper as well.
        """
        methods = self.obj
        for i, k in enumerate(methods):
            setattr(underscore, k, methods[k])

        self.makeStatic()
        return self._wrap(self.obj)

    def uniqueId(self, prefix=""):
        """
        Generate a unique integer id (unique within the entire client session).
        Useful for temporary DOM ids.
        """
        _IdCounter.count += 1
        id = _IdCounter.count
        if prefix:
            return self._wrap(prefix + str(id))
        else:
            return self._wrap(id)

    _html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }

    def escape(self):
        """ Escape a string for HTML interpolation.
        """
        # & must be handled first
        self.obj = self.obj.replace("&", self._html_escape_table["&"])

        for i, k in enumerate(self._html_escape_table):
            v = self._html_escape_table[k]
            if k != "&":
                self.obj = self.obj.replace(k, v)

        return self._wrap(self.obj)

    def unescape(self):
        """
        Within an interpolation, evaluation, or escaping, remove HTML escaping
        that had been previously added.
        """
        for i, k in enumerate(self._html_escape_table):
            v = self._html_escape_table[k]
            self.obj = self.obj.replace(v, k)

        return self._wrap(self.obj)

    """
    Template Code will be here
    """

    templateSettings = {
        "evaluate":     r"<%([\s\S]+?)%>",
        "interpolate":  r"<%=([\s\S]+?)%>",
        "escape":       r"<%-([\s\S]+?)%>"
    }

    escapes = {
        '\\':    '\\',
        "'":     r"'",
        "r":     r'\r',
        "n":     r'\n',
        "t":     r'\t',
        "u2028": r'\u2028',
        "u2029": r'\u2029',
        r'\\':   '\\',
        r"'":    "'",
        'br':    "r",
        'bn':    "n",
        'bt':    "t",
        'bu2028':  "u2028",
        'bu2029':  "u2029"
    }

    def template(self, data=None, settings=None):
        """
        Python micro-templating, similar to John Resig's implementation.
        Underscore templating handles arbitrary delimiters, preserves
        whitespace, and correctly escapes quotes within interpolated code.
        """
        if settings is None:
            settings = {}
        ts = _.templateSettings
        _.defaults(ts, self.templateSettings)
        _.extend(settings, ts)

        # settings = {
        #     "interpolate": self.templateSettings.get('interpolate'),
        #     "evaluate": self.templateSettings.get('evaluate'),
        #     "escape": self.templateSettings.get('escape')
        # }

        _.extend(settings, {
            "escaper": r"\\|'|\r|\n|\t|\u2028|\u2029",
            "unescaper": r"\\(\\|'|r|n|t|u2028|u2029)"
        })

        src = self.obj
        #src = re.sub('"', r'\"', src)
        #src = re.sub(r'\\', r"\\", src)
        ns = self.Namespace()
        ns.indent_level = 1

        def unescape(code):
            def unescapes(matchobj):
                a = re.sub("^[\'\"]|[\'\"]$", "", ("%r" % matchobj.group(1)))
                # Python doesn't accept \n as a key
                if a == '\n':
                    a = "bn"
                if a == '\r':
                    a = "br"
                if a == '\t':
                    a = "bt"
                if a == '\u2028':
                    a = 'bu2028'
                if a == '\u2029':
                    a = 'bu2029'
                return self.escapes[a]
            return re.sub(settings.get('unescaper'), unescapes, code)

        def escapes(matchobj):
            a = matchobj.group(0)
            # Python doesn't accept \n as a key
            if a == '\n':
                a = "bn"
            if a == '\r':
                a = "br"
            if a == '\t':
                a = "bt"
            if a == '\u2028':
                a = 'bu2028'
            if a == '\u2029':
                a = 'bu2029'
            return '\\' + self.escapes[a]

        def indent(n=None):
            if n is not None:
                ns.indent_level += n
            return "  " * ns.indent_level

        def interpolate(matchobj):
            if getattr(str, 'decode', False):
                key = (matchobj.group(1).decode('string-escape')).strip()
            else:
                key = (bytes(matchobj.group(1), "utf-8").decode()).strip()
            return "' + str(" + unescape(key) + " or '') + '"

        def evaluate(matchobj):
            if getattr(str, 'decode', False):
                code = (matchobj.group(1).decode('string-escape')).strip()
            else:
                code = (bytes(matchobj.group(1), "utf-8").decode()).strip()
            if code.startswith("end"):
                return "')\n" + indent(-1) + "ns.__p += ('"
            elif code.endswith(':'):
                return "')\n" + indent() + unescape(code) + \
                       "\n" + indent(+1) + "ns.__p += ('"
            else:
                return "')\n" + indent() + unescape(code) + \
                       "\n" + indent() + "ns.__p += ('"

        def escape(matchobj):
            if getattr(str, 'decode', False):
                key = (matchobj.group(1).decode('string-escape')).strip()
            else:
                key = (bytes(matchobj.group(1), "utf-8").decode()).strip()
            return "' + _.escape(str(" + unescape(key) + " or '')) + '"

        source = indent() + 'class closure(object):\n    pass' + \
                            ' # for full closure support\n'
        source += indent() + 'ns = closure()\n'
        source += indent() + "ns.__p = ''\n"
        #src = re.sub("^[\'\"]|[\'\"]$", "", ("%r" % src))
        src = re.sub(settings.get("escaper"), escapes, src)
        source += indent() + "ns.__p += ('" + \
            re.sub(settings.get('escape'), escape, src) + "')\n"
        source = re.sub(settings.get('interpolate'), interpolate, source)
        source = re.sub(settings.get('evaluate'), evaluate, source)

        if getattr(str, 'decode', False):
            source += indent() + 'return ns.__p.decode("string_escape")\n'
        else:
            source += indent() + 'return bytes(ns.__p, "utf-8").decode()\n'

        f = self.create_function(settings.get("variable")
                                 or "obj=None", source)

        if data is not None:
            return f(data)
        return f

    def create_function(self, args, source):
        source = "global func\ndef func(" + args + "):\n" + source + "\n"
        ns = self.Namespace()
        try:
            code = compile(source, '', 'exec')
            exec(code) in globals(), locals()
        except:
            print(source)
            raise Exception("template error")
        ns.func = func

        def _wrap(obj={"this": ""}):
            for i, k in enumerate(obj):
                if getattr(ns.func, 'func_globals', False):
                    ns.func.func_globals[k] = obj[k]
                else:
                    ns.func.__globals__[k] = obj[k]
            return ns.func(obj)

        _wrap.source = source
        return _wrap

    def chain(self):
        """ Add a "chain" function, which will delegate to the wrapper.
        """
        self.chained = True
        return self

    def value(self):
        """ returns the object instead of instance
        """
        if self._wrapped is not self.Null:
            return self._wrapped
        else:
            return self.obj

    @staticmethod
    def makeStatic():
        """ Provide static access to underscore class
        """
        p = lambda value: inspect.ismethod(value) or inspect.isfunction(value)
        for eachMethod in inspect.getmembers(underscore, predicate=p):
            m = eachMethod[0]
            m1 = eachMethod[1]
            d = eachMethod[1].__doc__
            if not hasattr(_, m):
                def caller(a):
                    def execute(*args):
                        r = None
                        if len(args) == 1:
                            r = getattr(underscore(args[0]), a)()
                        elif len(args) > 1:
                            rargs = args[1:]
                            r = getattr(underscore(args[0]), a)(*rargs)
                        else:
                            r = getattr(underscore([]), a)()
                        if r is None:
                            print("makeStatic: failed: {}".format(m))
                        return r
                    execute.__doc__ = "{}{}\n\n{}".format(
                            m,
                            inspect.signature(m1),
                            d
                            )
                    return execute
                    
               

                _.__setattr__(m, caller(m))
                getattr(_, m).__name__ = m

        # put the class itself as a parameter so that we can use it on outside
        _.__setattr__("underscore", underscore)
        _.templateSettings = {}

# Imediatelly create static object
underscore.makeStatic()

# The end
