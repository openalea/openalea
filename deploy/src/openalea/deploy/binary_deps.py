"""binary dependencies"""

__license__ = "Cecill-C"
__revision__ = " $Id$"

import pkg_resources
import warnings


def binary_deps(pkg, verbose=True):
    """ add to the pkg the version number for binary dependency 
    
    :param pkg: package
    :param verbose: default is True
    
    """
    
    try:
        dists = pkg_resources.require(pkg)
    except:
        warnings.warn("package '" + pkg + "' not found.")
        return pkg
   
    deps = pkg + '==' + dists[0].version
    
    if verbose:
        print ("Binary dependency : '" + deps + "'")
    return deps
