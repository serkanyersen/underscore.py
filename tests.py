from underscore import _


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
    if val == True:
        return val
    return None

print _({"a": True, "b": False, "c": True, "d": 1}).map(isTrue)


# Try map on lists
def biggerThan4(v):
    if v > 4:
        return v
    return None

print _((4, 5, 2, 1, 6, 8)).map(biggerThan4)  # Tuple
print _([4, 5, 2, 1, 6, 8]).collect(biggerThan4)  # List also alias test
