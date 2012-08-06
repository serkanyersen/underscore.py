#/usr/bin/python
import inspect
#from itertools import imap


# underscore object
def _(obj):
    return _oo(obj)


class _oo():

    obj = None

    def __init__(self, obj):
        self.obj = obj

    def isDict(self):
        return type(self.obj) == type({})

    def isTuple(self):
        return type(self.obj) == type(())

    def isList(self):
        return type(self.obj) == type([])

    def value(self):
        return self.obj

    def min(self):
        return min(self.obj)

    def max(self):
        return max(self.obj)

    def each(self, func):
        if self.isTuple() or self.isList():
            for index, value in enumerate(self.obj):
                func(value, index, self.obj)
        else:
            for index, key in enumerate(self.obj):
                func(self.obj[key], key, self.obj, index)
        return self
    # @alias self::each
    forEach = each

    def map(self, func):
        # if self.isDict():
        #     new = {}

        #     def iterate1(k, v, l, i):
        #         if(func(k, v, l, i) == True):
        #             new[k] = v

        #     self.each(iterate1)
        # else:
        #     new = self.obj[:]

        #     def iterate2(v, i, l):
        #         if(func(v, i, l) == True):
        #             new.append(v)

        #     self.each(iterate2)
        if self.isDict():
            return map(lambda k: func(self.obj[k], k), self.obj)
        else:
            return map(lambda v: func(v), self.obj)
    # @alias
    collect = map

    @staticmethod
    def makeStatic():
        # Provide static access to _ object
        for eachMethod in inspect.getmembers(_oo, predicate=inspect.ismethod):
            m = eachMethod[0]
            #print m
            if not hasattr(_, m):
                def caller(a):
                    return lambda *args: getattr(_oo(args[0]), a)(*args[1:])
                _.__setattr__(m, caller(m))

_oo.makeStatic()

# The end

# Tests and Usage
if __name__ == '__main__':

    # Test each for lists
    def it(v, i, l):
        print "index: ", i, " Value: ", v

    c = _.each(("a", "b", "c"), it)     # Tuple
    c = _.forEach(["d", "e", "f"], it)  # List also alias test

    # Test each for Dicts
    def that(v, k, l, i):
        print k, ":", v, "- [", i, "]"

    d = _({"aa": "aaVal", "bb": "bbVal", "cc": "ccVal"}).each(that)  # OO Way

    # Some single handed methods (easy ones)
    print "min:", _([2, 3, 4, 5]).min()
    print "max:", _.max([2, 1, 4, 5])

    # try map on Dicts
    def isTrue(val, key):
        return val == True

    print _({"a": True, "b": False, "c": True, "d": 1}).map(isTrue)

    # Try map on lists
    def biggerThan4(v):
        return v > 4

    print _((4, 5, 2, 1, 6, 8)).map(biggerThan4)  # Tuple
    print _([4, 5, 2, 1, 6, 8]).collect(biggerThan4)  # List also alias test
