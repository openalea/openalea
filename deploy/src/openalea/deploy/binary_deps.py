
import pkg_resources
import warnings

def binary_deps(pkg,verbose = True):
    """ add to the pkg the version number for binary dependancy """
    try:
        dists = pkg_resources.require(pkg)
    except:
       warnings.warn("package '"+pkg+"' not found.")
       return pkg
    deps = pkg+'=='+dists[0].version
    if verbose:
        print ("Binary dependency : '"+deps+"'")
    return deps
