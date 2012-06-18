import sys

try:
    import rpy2.robjects as robjects
    sys.exit(0)
except RuntimeError, e:
    #this happens when impot succeeds but the 
    #R_USER variable doesn't exist
    sys.exit(0)
except ImportError, e:
    sys.exit(1)
