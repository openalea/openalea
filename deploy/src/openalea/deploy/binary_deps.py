
import pkg_resources

def binary_deps(pkg,verbose = True):
    """ add to the pkg the version number for binary dependancy """
    dists = pkg_resources.require(pkg)
    deps = pkg+'=='+dists[0].version
    if verbose:
        print ("Binary dependency : '"+deps+"'")
    return deps
