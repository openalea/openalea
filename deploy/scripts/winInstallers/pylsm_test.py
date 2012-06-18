import sys

try:
    from pylsm import lsmreader
    sys.exit(0)
except Exception, e:
    sys.exit(1)
