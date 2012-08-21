#!/usr/bin/env python
import inspect
from types import *
from itertools import ifilterfalse
from itertools import chain
import re
import functools
import cgi
from sets import Set


class _IdCounter:
    """
    A Global Dictionary for uniq IDs
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
    """
    Decorator to rename a function
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


class underscore():
    """
    Instead of creating a class named _ (underscore) I created underscore
    So I can use _ function both statically and dynamically just it
    is in the original underscore
    """

    object = None
    """
    Passed object
    """

    VERSION = "0.1.2"
    """
    Version of the library
    """

    chained = False
    """
    If the object is in a chained state or not
    """

    Null = "__Null__"
    """
    Since we are working with the native types of the library
    I cannot compare any type with None, so I use a Substitute type for cheching
    """

    _wrapped = Null
    """
    When object is in chained state, This property will contain the latest processed
    Value of passed object, I assign it no Null so I can check against None results
    """

    class Namespace:
        """
        For simulating full closure support
        """
        pass

    def __init__(self, obj):
        """
        Let there be light
        """
        self.chained = False
        self.object = obj

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
            return self.object

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
        """
        Pitty attempt to convert itertools result into a real object
        """
        if self._clean.isTuple():
            return tuple(val)
        elif self._clean.isList():
            return list(val)
        elif self._clean.isDict():
            return dict(val)
        else:
            return val

    """
    Collection Functions
    """

    def each(self, func):
        """
        iterates through each item of an object
        :Param: func iterator function
        """
        if self._clean.isTuple() or self._clean.isList():
            for index, value in enumerate(self.obj):
                r = func(value, index, self.obj)
                if r is "breaker":
                    break
        else:
            for index, key in enumerate(self.obj):
                r = func(self.obj[key], key, self.obj, index)
                if r is "breaker":
                    break
        return self._wrap(self)
    forEach = each

    def map(self, func):
        """
        Return the results of applying the iterator to each element.
        """
        ns = self.Namespace()
        ns.results = []

        def by(value, index, list, *args):
            ns.results.append(func(value, index, list))

        _(self.obj).each(by)
        return self._wrap(ns.results)
    collect = map

    def reduce(self, func, memo=None):
        """
        **Reduce** builds up a single result from a list of values, aka `inject`, or foldl
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
        """
        The right-associative version of reduce, also known as `foldr`.
        """
        #foldr = lambda f, i: lambda s: reduce(f, s, i)
        x = self.obj[:]
        x.reverse()
        return self._wrap(reduce(func, x))
    foldr = reduceRight

    def find(self, func):
        """
        Return the first value which passes a truth test. Aliased as `detect`.
        """
        self.ftmp = None

        def test(value, index, list):
            if func(value, index, list) is True:
                self.ftmp = value
                return True
        self._clean.any(test)
        return self._wrap(self.ftmp)
    detect = find

    def filter(self, func):
        """
        Return all the elements that pass a truth test.
        """
        return self._wrap(filter(func, self.obj))
    select = filter

    def reject(self, func):
        """
        Return all the elements for which a truth test fails.
        """
        r = ifilterfalse(func, self.obj)
        return self._wrap(self._toOriginal(r))

    def all(self, func=None):
        """
        Determine whether all of the elements match a truth test.
        """
        if func is None:
            func = lambda x, *args: x
        self.altmp = True

        def testEach(value, index, *args):
            if func(value, index, *args) is False:
                self.altmp = False

        self._clean.each(testEach)
        return self._wrap(self.altmp)
    every = all

    def any(self, func=None):
        """
        Determine if at least one element in the object matches a truth test.
        """
        if func is None:
            func = lambda x, *args: x
        self.antmp = False

        def testEach(value, index, *args):
            if func(value, index, *args) is True:
                self.antmp = True
                return "breaker"

        self._clean.each(testEach)
        return self._wrap(self.antmp)
    some = any

    def include(self, target):
        """
        Determine if a given value is included in the array or object using `is`.
        """
        if self._clean.isDict():
            return self._wrap(target in self.obj.values())
        else:
            return self._wrap(target in self.obj)
    contains = include

    def invoke(self, method, *args):
        """
        Invoke a method (with arguments) on every item in a collection.
        """
        def inv(value, *ar):
            if(_(method).isFunction() or _(method).isLambda() or _(method).isMethod()):
                return method(value, *args)
            else:
                return getattr(value, method)(*args)
        return self._wrap(self._clean.map(inv))

    def pluck(self, key):
        """
        Convenience version of a common use case of `map`: fetching a property.
        """
        return self._wrap([x.get(key) for x in self.obj])

    def max(self):
        """
        Return the maximum element or (element-based computation).
        """
        if(self._clean.isDict()):
            return self._wrap(list())
        return self._wrap(max(self.obj))

    def min(self):
        """
        Return the minimum element (or element-based computation).
        """
        if(self._clean.isDict()):
            return self._wrap(list())
        return self._wrap(min(self.obj))

    def shuffle(self):
        """
        Shuffle an array.
        """
        if(self._clean.isDict()):
            return self._wrap(list())

        cloned = self.obj[:]
        import random
        random.shuffle(cloned)
        return self._wrap(cloned)

    def sortBy(self, val=None):
        """
        Sort the object's values by a criterion produced by an iterator.
        """
        if val is not None:
            if _(val).isString():
                return self._wrap(sorted(self.obj, key=lambda x, *args: x.get(val)))
            else:
                return self._wrap(sorted(self.obj, val))
        else:
            return self._wrap(sorted(self.obj))

    def _lookupIterator(self, obj, val):
        """
        An internal function to generate lookup iterators.
        """
        return val if _.isCallable(val) else lambda obj, *args: obj[val]

    def _group(self, obj, val, behavior):
        """
        An internal function used for aggregate "group by" operations.
        """
        ns = self.Namespace()
        ns.result = {}
        iterator = self._lookupIterator(obj, val)

        def e(value, index, *args):
            key = iterator(value, index)
            behavior(ns.result, key, value)

        _.each(obj, e)

        return ns.result

    def groupBy(self, val):
        """
        Groups the object's values by a criterion. Pass either a string attribute
        to group by, or a function that returns the criterion.
        """

        def by(result, key, value):
            if key not in result:
                result[key] = []
            result[key].append(value)

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
        an object should be inserted so as to maintain order. Uses binary search.
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
        """
        Safely convert anything iterable into a real, live array.
        """
        return self._wrap(list(self.obj))

    def size(self):
        """
        Return the number of elements in an object.
        """
        return self._wrap(len(self.obj))

    def first(self, n=1):
        """
        Get the first element of an array. Passing **n** will return the first N
        values in the array. Aliased as `head` and `take`. The **guard** check
        allows it to work with `_.map`.
        """
        res = self.obj[0:n]
        if len(res) is 1:
            res = res[0]
        return self._wrap(res)
    head = take = first

    def initial(self, n=1):
        """
        Returns everything but the last entry of the array. Especially useful on
        the arguments object. Passing **n** will return all the values in
        the array, excluding the last N. The **guard** check allows it to work with
        `_.map`.
        """
        return self._wrap(self.obj[0:-n])

    def last(self, n=1):
        """
        Get the last element of an array. Passing **n** will return the last N
        values in the array. The **guard** check allows it to work with `_.map`.
        """
        res = self.obj[-n:]
        if len(res) is 1:
            res = res[0]
        return self._wrap(res)

    def rest(self, n=1):
        """
        Returns everything but the first entry of the array. Aliased as `tail`.
        Especially useful on the arguments object. Passing an **index** will return
        the rest of the values in the array from that index onward. The **guard**
        check allows it to work with `_.map`.
        """
        return self._wrap(self.obj[n:])
    tail = rest

    def compact(self):
        """
        Trim out all falsy values from an array.
        """
        return self._wrap(self._clean.filter(lambda x: x))

    def flatten(self, shallow=None):
        """
        Return a completely flattened version of an array.
        """
        if(shallow is True):
            return self._wrap(list(chain.from_iterable(self.obj)))
        else:
            return self._wrap(list(chain.from_iterable(self.obj)))  # Must do this recursively

    def without(self, *values):
        """
        Return a version of the array that does not contain the specified value(s).
        """
        if self._clean.isDict():
            newlist = {}
            for i, k in enumerate(self.obj):
                if k not in values:
                    newlist.set(k, self.obj[k])
        else:
            newlist = []
            for i, v in enumerate(self.obj):
                if v not in values:
                    newlist.append(v)

        return self._wrap(newlist)

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
            if (_.last(memo) != value or not len(memo)) if isSorted else not _.include(memo, value):
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

    def union(self, *args):
        """
        Produce an array that contains the union: each distinct element from all of
        the passed-in arrays.
        """
        setobj = Set(self.obj)
        for i, v in enumerate(args):
            setobj = setobj.union(args[i])
        return self._wrap(self._clean._toOriginal(setobj))

    def intersection(self, *args):
        """
        Produce an array that contains every item shared between all the
        passed-in arrays.
        """
        a = tuple(self.obj[0])
        setobj = Set(a)
        for i, v in enumerate(args):
            setobj = setobj.intersection(args[i])
        return self._wrap(list(setobj))

    def difference(self, *args):
        """
        Take the difference between one array and a number of other arrays.
        Only the elements present in just the first array will remain.
        """
        setobj = Set(self.obj)
        for i, v in enumerate(args):
            setobj = setobj.difference(args[i])
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

    def zipObject(self, values):
        """
        Zip together two arrays -- an array of keys and an array of values -- into
        a single object.
        """
        result = {}
        keys = self.obj
        i = 0
        l = len(keys)
        while i < l:
            result[keys[i]] = values[i]
            l = len(keys)
            i += 1

        return self._wrap(result)

    def indexOf(self, str):
        """
        Return the position of the first occurrence of an
        item in an array, or -1 if the item is not included in the array.
        """
        return self._wrap(1)

    def lastIndexOf(self, str):
        """
        Return the position of the last occurrence of an
        item in an array, or -1 if the item is not included in the array.
        """
        return self._wrap(2)

    def range(self, start, stop, step):
        """
        Generate an integer Array containing an arithmetic progression.
        """
        return self._wrap(range(start, stop, step))

    """
    Function functions
    """

    def bind(self, context):
        """
        Create a function bound to a given object (assigning `this`, and arguments,
        optionally). Binding with arguments is also known as `curry`.
        """
        return self._wrap(self.obj)
    curry = bind

    def bindAll(self, *args):
        """
        Bind all of an object's methods to that object. Useful for ensuring that
        all callbacks defined on an object belong to it.
        """
        return self._wrap(self.obj)

    def memoize(self, hasher):
        """
        Memoize an expensive function by storing its results.
        """
        return self._wrap(self.obj)

    def delay(self, wait):
        """
        Delays a function for the given number of milliseconds, and then calls
        it with the arguments supplied.
        """
        return self._wrap(self.obj)

    def defer(self):
        """
        Defers a function, scheduling it to run after the current call stack has
        cleared.
        """
        return self._wrap(self.obj)

    def throttle(self, wait):
        """
        Returns a function, that, when invoked, will only be triggered at most once
        during a given window of time.
        """
        return self._wrap(self.obj)

    # https://gist.github.com/2871026
    def debounce(self, wait, immediate):
        """
        Returns a function, that, as long as it continues to be invoked, will not
        be triggered. The function will be called after it stops being called for
        N milliseconds. If `immediate` is passed, trigger the function on the
        leading edge, instead of the trailing.
        """
        return self._wrap(self.obj)

    def once(self):
        """
        Returns a function that will be executed at most one time, no matter how
        often you call it. Useful for lazy initialization.
        """
        return self._wrap(self.obj)

    def wrap(self, wrapper):
        """
        Returns the first function passed as an argument to the second,
        allowing you to adjust arguments, run code before and after, and
        conditionally execute the original function.
        """
        return self._wrap(self.obj)

    def compose(self, *args):
        """
        Returns a function that is the composition of a list of functions, each
        consuming the return value of the function that follows.
        """
        return self._wrap(self.obj)

    def after(self, times):
        """
        Returns a function that will only be executed after being called N times.
        """
        return self._wrap(self.obj)

    """
    Object Functions
    """

    def keys(self):
        """
        Retrieve the names of an object's properties.
        """
        return self._wrap(self.obj.keys())

    def values(self):
        """
        Retrieve the values of an object's properties.
        """
        return self._wrap(self.obj.values())

    def functions(self):
        """
        Return a sorted list of the function names available on the object.
        """
        return self._wrap(self._clean.filter(lambda k, v, *args: type(v) is MethodType \
                                                              or type(v) is FunctionType \
                                                              or type(v) is LambdaType \
                                                              or type(v) is BuiltinMethodType \
                                                              or type(v) is BuiltinFunctionType\
                                                              or type(v) is UnboundMethodType))
    methods = functions

    def extend(self, *args):
        """
        Extend a given object with all the properties in passed-in object(s).
        """
        for i in args:
            self.obj.update(args[i])

        return self._wrap(self.obj)

    def pick(self, *args):
        """
        Return a copy of the object only containing the whitelisted properties.
        """
        return self._wrap(self.obj)

    def defaults(self, *args):
        """
        Fill in a given object with default properties.
        """
        return self._wrap(self.obj)

    def clone(self):
        """
        Create a (shallow-cloned) duplicate of an object.
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
        """
        Perform a deep comparison to check if two objects are equal.
        """
        return self._wrap(self.obj is match)

    def isEmpty(self):
        """
        Is a given array, string, or object empty?
        An "empty" object has no enumerable own-properties.
        """
        if self._clean.isString():
            ret = self.obj.strip() is ""
        elif self._clean.isDict():
            ret = len(self.obj.keys()) > 0
        else:
            ret = len(self.obj) > 0
        return self._wrap(ret)

    def isElement(self):
        """
        No use in python
        """
        return self._wrap(False)

    def isDict(self):
        """
        Check if given object is a dictionary
        """
        return self._wrap(type(self.obj) is DictType)

    def isTuple(self):
        """
        Check if given object is a Tuple
        """
        return self._wrap(type(self.obj) is TupleType)

    def isList(self):
        """
        Check if given object is a list
        """
        return self._wrap(type(self.obj) is ListType)

    def isNone(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is NoneType)

    def isType(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is TypeType)

    def isBoolean(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is BooleanType)
    isBool = isBoolean

    def isInt(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is IntType)

    def isLong(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is LongType)

    def isFloat(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is FloatType)

    def isComplex(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is ComplexType)

    def isString(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is StringType)

    def isUnicode(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is UnicodeType)

    def isCallable(self):
        """
        Check if the given object is any of the function types
        """
        return self._wrap(type(self.obj) is MethodType \
                       or type(self.obj) is FunctionType \
                       or type(self.obj) is LambdaType \
                       or type(self.obj) is BuiltinMethodType \
                       or type(self.obj) is BuiltinFunctionType\
                       or type(self.obj) is UnboundMethodType)

    def isFunction(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is FunctionType)

    def isLambda(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is LambdaType)  # or type(self.obj) is FunctionType)

    def isGenerator(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is GeneratorType)

    def isCode(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is CodeType)

    def isClass(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is ClassType)

    def isInstance(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is InstanceType)

    def isMethod(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is MethodType)

    def isUnboundMethod(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is UnboundMethodType)

    def isBuiltinFunction(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is BuiltinFunctionType)

    def isBuiltinMethod(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is BuiltinMethodType)

    def isModule(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is ModuleType)

    def isFile(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is FileType)

    def isXRange(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is XRangeType)

    def isSlice(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is SliceType)

    def isEllipsis(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is EllipsisType)

    def isTraceback(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is TracebackType)

    def isFrame(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is FrameType)

    def isBuffer(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is BufferType)

    def isDictProxy(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is DictProxyType)

    def isNotImplemented(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is NotImplementedType)

    def isGetSetDescriptor(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is GetSetDescriptorType)

    def isMemberDescriptor(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) is MemberDescriptorType)

    def has(self, key):
        """
        Shortcut function for checking if an object has a given property directly
        on itself (in other words, not on a prototype).
        """
        return self._wrap(hasattr(self.obj, key))

    def join(self, glue=" "):
        """
        Javascript's join implementation
        """
        j = glue.join([str(x) for x in self.obj])
        return self._wrap(j)

    def identity(self, *args):
        """
        Keep the identity function around for default iterators.
        """
        return self._wrap(self.obj)

    def times(self, func, *args):
        """
        Run a function **n** times.
        """
        n = self.obj
        i = 0
        while n is not 0:
            n -= 1
            func(i)
            i += 1

        return self._wrap(func)

    def escape(self):
        """
        Escape a string for HTML interpolation.
        """
        return self._wrap(cgi.escape(self.obj))

    def result(self, property):
        """
        If the value of the named property is a function then invoke it;
        otherwise, return it.
        """
        return self._wrap(self.obj)

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

    def unescape(self):
        """
        Within an interpolation, evaluation, or escaping, remove HTML escaping
        that had been previously added.
        """
        return self._wrap(self.obj)

    """
    Template Code will be here
    """

    templateSettings = {
        "evaluate":     r"<%([\s\S]+?)%>",
        "interpolate":  r"<%=([\s\S]+?)%>",
        "escape":       r"<%-([\s\S]+?)%>"
    }

    def template(self, settings={}):
        """
        Python micro-templating, similar to John Resig's implementation.
        Underscore templating handles arbitrary delimiters, preserves whitespace,
        and correctly escapes quotes within interpolated code.
        """
        # settings = _.defaults(settings, self.templateSettings)
        settings = {
            "interpolate": self.templateSettings.get('interpolate'),
            "evaluate": self.templateSettings.get('evaluate')
        }
        src = self.obj
        ns = self.Namespace()
        ns.indent_level = 1

        def indent(n=None):
            if n is not None:
                ns.indent_level += n
            return "  " * ns.indent_level

        def interpolate(matchobj):
            key = (matchobj.group(1).decode('string-escape')).strip()
            return '" + str(' + key + ') + "'

        def evaluate(matchobj):
            code = (matchobj.group(1).decode('string-escape')).strip()
            if code.startswith("end"):
                return '")\n' + indent(-1) + '__p += ("'
            elif code.endswith(':'):
                return '")\n' + indent() + code + "\n" + indent(+1) + '__p += ("'
            else:
                return '")\n' + indent() + code + "\n" + indent() + '__p += ("'

        source = indent() + '__p = ""\n'
        source += indent() + '__p += ("' + re.sub(settings.get('interpolate'), interpolate, ("%r" % src)) + '")\n'
        source = re.sub(settings.get('evaluate'), evaluate, source)
        source += indent() + 'return __p\n'
        return self.create_function("obj={}", source)

    def create_function(self, args, source):
        source = "def func(" + args + "):\n" + source + "\n"
        ns = self.Namespace()
        try:
            code = compile(source, '', 'exec')
            exec code in globals(), locals()
        except:
            print "Error Evaluating Code"
            print source
        ns.func = func

        def _wrap(obj):
            for i, k in enumerate(obj):
                ns.func.func_globals[k] = obj[k]
            return ns.func(obj)

        _wrap.source = source
        return _wrap

    def chain(self):
        """
        Add a "chain" function, which will delegate to the wrapper.
        """
        self.chained = True
        return self

    def value(self):
        """
        returns the object instead of instance
        """
        if self._wrapped is not self.Null:
            return self._wrapped
        else:
            return self.obj

    @staticmethod
    def makeStatic():
        """
        Provide static access to underscore class
        """
        for eachMethod in inspect.getmembers(underscore, predicate=inspect.ismethod):
            m = eachMethod[0]
            if not hasattr(_, m):
                def caller(a):
                    def execute(*args):
                        if len(args) == 1:
                            r = getattr(underscore(args[0]), a)()
                        elif len(args) > 1:
                            rargs = args[1:]
                            r = getattr(underscore(args[0]), a)(*rargs)
                        else:
                            r = getattr(underscore([]), a)()
                        return r
                    return execute
                _.__setattr__(m, caller(m))
        # put the class itself as a parameter so that we can use it on outside
        _.__setattr__("underscore", underscore)

# Imediatelly create static object
underscore.makeStatic()

# The end
