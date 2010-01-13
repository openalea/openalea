""" todo """

__license__ = "Cecill-C"
__revision__ =" $Id$"

import pkg_resources

def dependencies(name, full_deps = None ):
    if full_deps is None:
        full_deps = set()
    dist = pkg_resources.get_distribution(name)
    full_deps.add(name)
    for dep in dist.requires():
        dependencies(dep.project_name, full_deps)
    return full_deps
    
def test():
    pass
