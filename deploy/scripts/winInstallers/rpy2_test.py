import sys

try:
    import rpy2.robjects as robjects
    sys.exit(0)
except Exception, e:
    sys.exit(1)
