#!/usr/bin/env python
import inspect
from types import *
from itertools import ifilterfalse
from itertools import groupby
from itertools import chain
import re
import functools


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
        if self._clean.isDict():
            return self._wrap(map(lambda k: func(self.obj[k], k), self.obj))
        else:
            return self._wrap(map(lambda v: func(v), self.obj))
    collect = map

    def reduce(self, func):
        """
        **Reduce** builds up a single result from a list of values, aka `inject`, or foldl
        """
        return self._wrap(reduce(func, self.obj))
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
            func = self.identity
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
            func = self.identity
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
                return self._wrap(sorted(self.obj, key=lambda x: x.get(val)))
            else:
                return self._wrap(sorted(self.obj, val))
        else:
            return self._wrap(sorted(self.obj))

    def groupBy(self, val):
        """
        Groups the object's values by a criterion. Pass either a string attribute
        to group by, or a function that returns the criterion.
        """
        return self._wrap(self._toOriginal(groupby(self.obj, val)))

    def countBy(self, val):
        """
        Counts instances of an object that group by a certain criterion. Pass
        either a string attribute to count by, or a function that returns the
        criterion.
        """
        return self._wrap(self.obj)

    def sortedIndex(self, func):
        """
        Use a comparator function to figure out the smallest index at which
        an object should be inserted so as to maintain order. Uses binary search.
        """
        return self._wrap(self.obj)

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

    def without(self, values):
        """
        Return a version of the array that does not contain the specified value(s).
        """
        return self._wrap(self.obj)

    def uniq(self, isSorted, iterator):
        """
        Produce a duplicate-free version of the array. If the array has already
        been sorted, you have the option of using a faster algorithm.
        Aliased as `unique`.
        """
        return self._wrap(self.obj)
    unique = uniq

    def union(self, *args):
        """
        Produce an array that contains the union: each distinct element from all of
        the passed-in arrays.
        """
        return self._wrap(self.obj)

    def intersection(self, *args):
        """
        Produce an array that contains every item shared between all the
        passed-in arrays.
        """
        return self._wrap(self.obj)

    def difference(self, *args):
        """
        Take the difference between one array and a number of other arrays.
        Only the elements present in just the first array will remain.
        """
        return self._wrap(self.obj)

    def zip(self, *args):
        """
        Zip together multiple lists into a single array -- elements that share
        an index go together.
        """
        return self._wrap(self.obj)

    def zipObject(self, *args):
        """
        Zip together two arrays -- an array of keys and an array of values -- into
        a single object.
        """
        return self._wrap(self.obj)

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
        return self._wrap(self.obj)

    def values(self):
        """
        Retrieve the values of an object's properties.
        """
        return self._wrap(self.obj)

    def functions(self):
        """
        Return a sorted list of the function names available on the object.
        """
        return self._wrap(self.obj)
    methods = functions

    def extend(self, *args):
        """
        Extend a given object with all the properties in passed-in object(s).
        """
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
        return self._wrap(self.obj)

    def tap(self, interceptor):
        """
        Invokes interceptor with the obj, and then returns obj.
        The primary purpose of this method is to "tap into" a method chain, in
        order to perform operations on intermediate results within the chain.
        """
        return self._wrap(self.obj)

    def isEqual(self, match):
        """
        Perform a deep comparison to check if two objects are equal.
        """
        return self._wrap(True)

    def isEmpty(self):
        """
        Is a given array, string, or object empty?
        An "empty" object has no enumerable own-properties.
        """
        return self._wrap(True)

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

    def identity(self, *args):
        """
        Keep the identity function around for default iterators.
        """
        return self._wrap(args[0])

    def times(self, n, func):
        """
        Run a function **n** times.
        """
        return self._wrap(self.obj)

    def escape(self):
        """
        Escape a string for HTML interpolation.
        """
        return self._wrap(self.obj)

    def result(self, property):
        """
        If the value of the named property is a function then invoke it;
        otherwise, return it.
        """
        return self._wrap(self.obj)

    def mixin(self, object):
        """
        Add your own custom functions to the Underscore object, ensuring that
        they're correctly added to the OOP wrapper as well.
        """
        return self._wrap(self.obj)

    idCounter = 0

    def uniqueId(self, prefix):
        """
        Generate a unique integer id (unique within the entire client session).
        Useful for temporary DOM ids.
        """
        self.idCounter = self.idCounter + 1
        id = self.idCounter
        if prefix:
            return self._wrap(prefix + id)
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

    class Namespace:
        pass

    def template(self, src):
        i = self.templateSettings.get('interpolate')
        e = self.templateSettings.get('evaluate')
        ns = self.Namespace()
        ns.il = 1
        source = ("  " * ns.il) + '__p = ""\n'

        def interpolate(matchobj):
            key = (matchobj.group(1).decode('string-escape')).strip()
            return '" + (obj.get("' + key + '") or "") + "'

        source += ("  " * ns.il) + '__p += ("' + re.sub(i, interpolate, ("%r" % src)) + '")\n'

        def evaluate(matchobj):
            code = (matchobj.group(1).decode('string-escape')).strip()
            if code.startswith("end"):
                ns.il -= 1
                return '")\n' + ("  " * ns.il) + '__p += ("'
            elif code.endswith(':'):
                rep = '")\n' + ("  " * ns.il)
                ns.il += 1
                rep += code + "\n" + ("  " * ns.il) + '__p += ("'
                return rep
            else:
                print "Errored code: " + code

        source = re.sub(e, evaluate, source)
        source += ("  " * ns.il) + 'return __p\n'
        return self.create_function("obj={}", source)

    def create_function(self, args, source):
        source = "def func(" + args + "):\n" + source + "\n"
        try:
            code = compile(source, '', 'exec')
            exec code
        except:
            print "Error Evaluating Code"
            print source

        return func

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
                    return lambda *args: getattr(underscore(args[0]), a)(*args[1:])
                _.__setattr__(m, caller(m))
        # put the class itself as a parameter so that we can use it on outside
        _.__setattr__("underscore", underscore)

# Imediatelly create static object
underscore.makeStatic()

# The end
