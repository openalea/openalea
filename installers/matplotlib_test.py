import sys

try:
    from pylab import *
    sys.exit(0)
except Exception, e:
    sys.exit(1)
