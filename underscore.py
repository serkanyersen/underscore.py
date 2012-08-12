#/usr/bin/python
import inspect
from types import *
#from itertools import imap


# underscore object
def _(obj):
    return _oo(obj)


class _oo():

    object = None

    VERSION = "0.1.1"

    chained = False
    Null = "__Null__"
    _wrapped = Null

    @property
    def obj(self):
        if self._wrapped != self.Null:
            return self._wrapped
        else:
            return self.object

    def __init__(self, obj):
        self.chained = False
        self.object = obj

    def _wrap(self, ret):
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
                func(value, index, self.obj)
        else:
            for index, key in enumerate(self.obj):
                func(self.obj[key], key, self.obj, index)
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
        foldr = lambda f, i: lambda s: reduce(f, s, i)
        return self._wrap(foldr(func, self.obj))
    foldr = reduceRight

    def find(self, func):
        """
        Return the first value which passes a truth test. Aliased as `detect`.
        """
        ret = None

        def test(value, index, list):
            if func(value, index, list) == True:
                global ret
                ret = value
                return True
        self.any(test)
        return self._wrap(ret)
    detect = find

    def filter(self, func):
        """
        Return all the elements that pass a truth test.
        """
        return self._wrap(self.obj)
    select = filter

    def reject(self, func):
        """
        Return all the elements for which a truth test fails.
        """
        return self._wrap(self.obj)

    def every(self, func):
        """
        Determine whether all of the elements match a truth test.
        """
        return self._wrap(self.obj)
    all = every

    def some(self, func=None):
        """
        Determine if at least one element in the object matches a truth test.
        """
        if func == None:
            func = self.identity
        ret = False

        def testEach(value, index, *args):
            global ret
            if func(value, index, *args) == True:
                ret = True
                return "breaker"

        self.each(testEach)
        return self._wrap(ret)
    any = some

    def include(self, target):
        """
        Determine if a given value is included in the array or object using `===`.
        """
        return True
    contains = include

    def invoke(self, method):
        """
        Invoke a method (with arguments) on every item in a collection.
        """
        return self._wrap(self.obj)

    def pluck(self, key):
        """
        Convenience version of a common use case of `map`: fetching a property.
        """
        return self._wrap(self.obj)

    def max(self):
        """
        Return the maximum element or (element-based computation).
        """
        return self._wrap(max(self.obj))

    def min(self):
        """
        Return the minimum element (or element-based computation).
        """
        return self._wrap(min(self.obj))

    def shuffle(self):
        """
        Shuffle an array.
        """
        return self._wrap(self.obj)

    def sortBy(self, val):
        """
        Sort the object's values by a criterion produced by an iterator.
        """
        return self._wrap(self.obj)

    def groupBy(self, val):
        """
        Groups the object's values by a criterion. Pass either a string attribute
        to group by, or a function that returns the criterion.
        """
        return self._wrap(self.obj)

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
        return self._wrap(self.obj)

    def size(self):
        """
        Return the number of elements in an object.
        """
        return self._wrap(1)

    def first(self, n, guard):
        """
        Get the first element of an array. Passing **n** will return the first N
        values in the array. Aliased as `head` and `take`. The **guard** check
        allows it to work with `_.map`.
        """
        return self._wrap(self.obj)
    head = take = first

    def initial(self, n, guard):
        """
        Returns everything but the last entry of the array. Especially useful on
        the arguments object. Passing **n** will return all the values in
        the array, excluding the last N. The **guard** check allows it to work with
        `_.map`.
        """
        return self._wrap(self.obj)

    def last(self, n, guard):
        """
        Get the last element of an array. Passing **n** will return the last N
        values in the array. The **guard** check allows it to work with `_.map`.
        """
        return self._wrap(self.obj)

    def rest(self, n, guard):
        """
        Returns everything but the first entry of the array. Aliased as `tail`.
        Especially useful on the arguments object. Passing an **index** will return
        the rest of the values in the array from that index onward. The **guard**
        check allows it to work with `_.map`.
        """
        return self._wrap(self.obj)
    tail = rest

    def compact(self):
        """
        Trim out all falsy values from an array.
        """
        return self._wrap(self.obj)

    def flatten(self, shallow):
        """
        Return a completely flattened version of an array.
        """
        return self._wrap(self.obj)

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
        return self._wrap(type(self.obj) == DictType)

    def isTuple(self):
        """
        Check if given object is a Tuple
        """
        return self._wrap(type(self.obj) == TupleType)

    def isList(self):
        """
        Check if given object is a list
        """
        return self._wrap(type(self.obj) == ListType)

    def isNone(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == NoneType)

    def isType(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == TypeType)

    def isBoolean(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == BooleanType)
    isBool = isBoolean

    def isInt(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == IntType)

    def isLong(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == LongType)

    def isFloat(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == FloatType)

    def isComplex(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == ComplexType)

    def isString(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == StringType)

    def isUnicode(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == UnicodeType)

    def isFunction(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == FunctionType)

    def isLambda(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == LambdaType)  # or type(self.obj) == FunctionType)

    def isGenerator(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == GeneratorType)

    def isCode(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == CodeType)

    def isClass(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == ClassType)

    def isInstance(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == InstanceType)

    def isMethod(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == MethodType)

    def isUnboundMethod(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == UnboundMethodType)

    def isBuiltinFunction(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == BuiltinFunctionType)

    def isBuiltinMethod(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == BuiltinMethodType)

    def isModule(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == ModuleType)

    def isFile(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == FileType)

    def isXRange(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == XRangeType)

    def isSlice(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == SliceType)

    def isEllipsis(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == EllipsisType)

    def isTraceback(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == TracebackType)

    def isFrame(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == FrameType)

    def isBuffer(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == BufferType)

    def isDictProxy(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == DictProxyType)

    def isNotImplemented(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == NotImplementedType)

    def isGetSetDescriptor(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == GetSetDescriptorType)

    def isMemberDescriptor(self):
        """
        Check if the given object is
        """
        return self._wrap(type(self.obj) == MemberDescriptorType)

    def has(self, key):
        """
        Shortcut function for checking if an object has a given property directly
        on itself (in other words, not on a prototype).
        """
        return self._wrap(hasattr(self.obj, key))

    def identity(self, value):
        """
        Keep the identity function around for default iterators.
        """
        return self._wrap(value)

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
        print self.chained, self._wrapped
        if self._wrapped != self.Null:
            return self._wrapped
        else:
            return self.obj

    @staticmethod
    def makeStatic():
        """
        Provide static access to _ object
        """
        for eachMethod in inspect.getmembers(_oo, predicate=inspect.ismethod):
            m = eachMethod[0]
            if not hasattr(_, m):
                def caller(a):
                    return lambda *args: getattr(_oo(args[0]), a)(*args[1:])
                _.__setattr__(m, caller(m))

# Imediatelly create static object
_oo.makeStatic()

# The end
