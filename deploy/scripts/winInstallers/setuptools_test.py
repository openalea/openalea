import sys

try:
    import setuptools
    print "yeah"
    sys.exit(0)
except Exception, e:
    print "oh"
    sys.exit(1)
