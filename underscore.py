#/usr/bin/python
import inspect
#from itertools import imap


# underscore object
def _(obj):
    return _oo(obj)


class _oo():

    obj = None

    VERSION = "0.1.1"

    def __init__(self, obj):
        self.obj = obj

    def each(self, func):
        """
        iterates through each item of an object
        :Param: func iterator function
        """
        if self.isTuple() or self.isList():
            for index, value in enumerate(self.obj):
                func(value, index, self.obj)
        else:
            for index, key in enumerate(self.obj):
                func(self.obj[key], key, self.obj, index)
        return self
    forEach = each

    def map(self, func):
        """
        Return the results of applying the iterator to each element.
        """
        if self.isDict():
            return map(lambda k: func(self.obj[k], k), self.obj)
        else:
            return map(lambda v: func(v), self.obj)
    collect = map

    def reduce(self, func):
        """
        **Reduce** builds up a single result from a list of values, aka `inject`, or foldl
        """
        return self.obj
    foldl = inject = reduce

    def reduceRight(self, func):
        """
        The right-associative version of reduce, also known as `foldr`.
        """
        return self.obj
    foldr = reduceRight

    def find(self, func):
        """
        Return the first value which passes a truth test. Aliased as `detect`.
        """
        return self.obj
    detect = find

    def filter(self, func):
        """
        Return all the elements that pass a truth test.
        """
        return self.obj
    select = filter

    def reject(self, func):
        """
        Return all the elements for which a truth test fails.
        """
        return self.obj

    def every(self, func):
        """
        Determine whether all of the elements match a truth test.
        """
        return self.obj
    all = every

    def some(self, func):
        """
        Determine if at least one element in the object matches a truth test.
        """
        return self.obj
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
        return self.obj

    def pluck(self, key):
        """
        Convenience version of a common use case of `map`: fetching a property.
        """
        return self.obj

    def max(self):
        """
        Return the maximum element or (element-based computation).
        """
        return max(self.obj)

    def min(self):
        """
        Return the minimum element (or element-based computation).
        """
        return min(self.obj)

    def shuffle(self):
        """
        Shuffle an array.
        """
        return self.obj

    def sortBy(self, val):
        """
        Sort the object's values by a criterion produced by an iterator.
        """
        return self.obj

    def groupBy(self, val):
        """
        Groups the object's values by a criterion. Pass either a string attribute
        to group by, or a function that returns the criterion.
        """
        return self.obj

    def countBy(self, val):
        """
        Counts instances of an object that group by a certain criterion. Pass
        either a string attribute to count by, or a function that returns the
        criterion.
        """
        return self.obj

    def sortedIndex(self, func):
        """
        Use a comparator function to figure out the smallest index at which
        an object should be inserted so as to maintain order. Uses binary search.
        """
        return self.obj

    def toArray(self):
        """
        Safely convert anything iterable into a real, live array.
        """
        return self.obj

    def size(self):
        """
        Return the number of elements in an object.
        """
        return 1

    def first(self, n, guard):
        """
        Get the first element of an array. Passing **n** will return the first N
        values in the array. Aliased as `head` and `take`. The **guard** check
        allows it to work with `_.map`.
        """
        return self.obj
    head = take = first

    def initial(self, n, guard):
        """
        Returns everything but the last entry of the array. Especially useful on
        the arguments object. Passing **n** will return all the values in
        the array, excluding the last N. The **guard** check allows it to work with
        `_.map`.
        """
        return self.obj

    def last(self, n, guard):
        """
        Get the last element of an array. Passing **n** will return the last N
        values in the array. The **guard** check allows it to work with `_.map`.
        """
        return self.obj

    def rest(self, n, guard):
        """
        Returns everything but the first entry of the array. Aliased as `tail`.
        Especially useful on the arguments object. Passing an **index** will return
        the rest of the values in the array from that index onward. The **guard**
        check allows it to work with `_.map`.
        """
        return self.obj
    tail = rest

    def compact(self):
        """
        Trim out all falsy values from an array.
        """
        return self.obj

    def flatten(self, shallow):
        """
        Return a completely flattened version of an array.
        """
        return self.obj

    def without(self, values):
        """
        Return a version of the array that does not contain the specified value(s).
        """
        return self.obj

    def uniq(self, isSorted, iterator):
        """
        Produce a duplicate-free version of the array. If the array has already
        been sorted, you have the option of using a faster algorithm.
        Aliased as `unique`.
        """
        return self.obj
    unique = uniq

    def union(self, *args):
        """
        Produce an array that contains the union: each distinct element from all of
        the passed-in arrays.
        """
        return self.obj

    def intersection(self, *args):
        """
        Produce an array that contains every item shared between all the
        passed-in arrays.
        """
        return self.obj

    def difference(self, *args):
        """
        Take the difference between one array and a number of other arrays.
        Only the elements present in just the first array will remain.
        """
        return self.obj

    def zip(self, *args):
        """
        Zip together multiple lists into a single array -- elements that share
        an index go together.
        """
        return self.obj

    def zipObject(self, *args):
        """
        Zip together two arrays -- an array of keys and an array of values -- into
        a single object.
        """
        return self.obj

    def indexOf(self, str):
        """
        Return the position of the first occurrence of an
        item in an array, or -1 if the item is not included in the array.
        """
        return 1

    def lastIndexOf(self, str):
        """
        Return the position of the last occurrence of an
        item in an array, or -1 if the item is not included in the array.
        """
        return 2

    def range(self, start, stop, step):
        """
        Generate an integer Array containing an arithmetic progression.
        """
        return range(start, stop, step)

    """
    Function functions
    """

    def bind(self, context):
        """
        Create a function bound to a given object (assigning `this`, and arguments,
        optionally). Binding with arguments is also known as `curry`.
        """
        return self.obj
    curry = bind

    def bindAll(self, *args):
        """
        Bind all of an object's methods to that object. Useful for ensuring that
        all callbacks defined on an object belong to it.
        """
        return self.obj

    def memoize(self, hasher):
        """
        Memoize an expensive function by storing its results.
        """
        return self.obj

    def delay(self, wait):
        """
        Delays a function for the given number of milliseconds, and then calls
        it with the arguments supplied.
        """
        return self.obj

    def defer(self):
        """
        Defers a function, scheduling it to run after the current call stack has
        cleared.
        """
        return self.obj

    def throttle(self, wait):
        """
        Returns a function, that, when invoked, will only be triggered at most once
        during a given window of time.
        """
        return self.obj

    def debounce(self, wait, immediate):
        """
        Returns a function, that, as long as it continues to be invoked, will not
        be triggered. The function will be called after it stops being called for
        N milliseconds. If `immediate` is passed, trigger the function on the
        leading edge, instead of the trailing.
        """
        return self.obj

    def once(self):
        """
        Returns a function that will be executed at most one time, no matter how
        often you call it. Useful for lazy initialization.
        """
        return self.obj

    def wrap(self, wrapper):
        """
        Returns the first function passed as an argument to the second,
        allowing you to adjust arguments, run code before and after, and
        conditionally execute the original function.
        """
        return self.obj

    def compose(self, *args):
        """
        Returns a function that is the composition of a list of functions, each
        consuming the return value of the function that follows.
        """
        return self.obj

    def after(self, times):
        """
        Returns a function that will only be executed after being called N times.
        """
        return self.obj

    """
    Object Functions
    """

    def keys(self):
        """
        Retrieve the names of an object's properties.
        """
        return self.obj

    def values(self):
        """
        Retrieve the values of an object's properties.
        """
        return self.obj

    def functions(self):
        """
        Return a sorted list of the function names available on the object.
        """
        return self.obj
    methods = functions

    def extend(self, *args):
        """
        Extend a given object with all the properties in passed-in object(s).
        """
        return self.obj

    def pick(self, *args):
        """
        Return a copy of the object only containing the whitelisted properties.
        """
        return self.obj

    def defaults(self, *args):
        """
        Fill in a given object with default properties.
        """
        return self.obj

    def clone(self):
        """
        Create a (shallow-cloned) duplicate of an object.
        """
        return self.obj

    def tap(self, interceptor):
        """
        Invokes interceptor with the obj, and then returns obj.
        The primary purpose of this method is to "tap into" a method chain, in
        order to perform operations on intermediate results within the chain.
        """
        return self.obj

    def isEqual(self, match):
        """
        Perform a deep comparison to check if two objects are equal.
        """
        return True

    def isEmpty(self):
        """
        Is a given array, string, or object empty?
        An "empty" object has no enumerable own-properties.
        """
        return True

    def isElement(self):
        """
        No use in python
        """
        return False

    def isDict(self):
        """
        Check if given object is a dictionary
        """
        return type(self.obj) == type({})

    def isTuple(self):
        """
        Check if given object is a Tuple
        """
        return type(self.obj) == type(())

    def isList(self):
        """
        Check if given object is a list
        """
        return type(self.obj) == type([])

    def isNone(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isType(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isBoolean(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isInt(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isLong(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isFloat(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isComplex(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isString(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isUnicode(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isFunction(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isLambda(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isGenerator(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isCode(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isClass(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isInstance(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isMethod(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isUnboundMethod(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isBuiltinFunction(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isBuiltinMethod(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isModule(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isFile(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isXRange(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isSlice(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isEllipsis(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isTraceback(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isFrame(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isBuffer(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isDictProxy(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isNotImplemented(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isGetSetDescriptor(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

    def isMemberDescriptor(self):
        """
        Check if the given object is
        """
        return type(self.obj) == "<type ''>"

        def isStringT(self):
            """
            Check if the given object is
            """
            return type(self.obj) == "<type ''>"

    def has(self, key):
        """
        Shortcut function for checking if an object has a given property directly
        on itself (in other words, not on a prototype).
        """
        return hasattr(self.obj, key)

    def identity(self, value):
        """
        Keep the identity function around for default iterators.
        """
        return value

    def times(self, n, func):
        """
        Run a function **n** times.
        """
        return self

    def escape(self):
        """
        Escape a string for HTML interpolation.
        """
        return self.obj

    def result(self, property):
        """
        If the value of the named property is a function then invoke it;
        otherwise, return it.
        """
        return self.obj

    def mixin(self, object):
        """
        Add your own custom functions to the Underscore object, ensuring that
        they're correctly added to the OOP wrapper as well.
        """
        return self.obj

    idCounter = 0

    def uniqueId(self, prefix):
        """
        Generate a unique integer id (unique within the entire client session).
        Useful for temporary DOM ids.
        """
        self.idCounter = self.idCounter + 1
        id = self.idCounter
        if prefix:
            return prefix + id
        else:
            return id

    def unescape(self):
        """
        Within an interpolation, evaluation, or escaping, remove HTML escaping
        that had been previously added.
        """
        return self.obj

    """
    Template Code will be here
    """
    def chain(self):
        """
        Add a "chain" function, which will delegate to the wrapper.
        """
        return self

    def value(self):
        """
        returns the object instead of instance
        """
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
