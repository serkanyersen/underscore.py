from underscore import _


 # Test each for lists
def it(v, i, l):
    print "index: ", i, " Value: ", v


# Test each for Dicts
def that(v, k, l, i):
    print k, ":", v, "- [", i, "]"


# try map on Dicts
def isTrue(val, key):
    if val == True:
        return val
    return None


# Try map on lists
def biggerThan4(v):
    if v > 4:
        return v
    return 100


print "Test Each"
c = _.each(("a", "b", "c"), it)     # Tuple
print "Test forEach"
c = _.forEach(["d", "e", "f"], it)  # List also alias test
print "Test Each on dictionaries"
_({"aa": "aaVal", "bb": "bbVal", "cc": "ccVal"}).each(that)  # OO Way
print "Test Map"
print _({"a": True, "b": False, "c": True, "d": 1}).map(isTrue)
print "Test Map and Collect"
print _([4, 5, 2, 1, 6, 8]).collect(biggerThan4)  # List also alias test
print "Test Chaining With Map"
print _((4, 5, 2, 1, 6, 8)).chain().map(biggerThan4).min().value()  # Tuple
print "Test Reduce"
print _([1, 2, 3, 4, 5, 6]).reduce(lambda sum, num: sum + num)
print "Test ReduceRight"
print _(["foo", "bar", "baz"]).reduceRight(lambda sum, num: sum + num)
print "Test find"
print _((4, 5, 2, 1, 6, 8)).find(lambda x, *args: x > 5)
print "Test min:", _([2, 3, 4, 5]).min()
print "Test max:", _.max([2, 1, 4, 5])
