import sys

try:
    import scipy
    sys.exit(0)
except Exception, e:
    sys.exit(1)
