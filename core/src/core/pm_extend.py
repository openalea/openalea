from fnmatch import fnmatch

from openalea.core.alea import *
from openalea.core.data import DataFactory
from openalea.core.compositenode import CompositeNodeFactory
from openalea.core.node import NodeFactory

def get_pm():
    return load_package_manager()

def is_data(factory):
    return isinstance(factory, DataFactory)
def is_cn(factory):
    return isinstance(factory, CompositeNodeFactory)
def is_node(factory):
    return isinstance(factory, NodeFactory)

def get_packages(pm, pkg_name=None):
    if pkg_name and pkg_name in pm:
        pkgs = [pkg_name]
    else:
        pkgs = set(pk.name for pk in pm.itervalues() if not pk.name.startswith('#'))
    return pkgs

def data(pm, pattern = '*.*', pkg_name=None):
    pkgs = get_packages(pm, pkg_name)
    
    datafiles = [f for p in pkgs for f in pm[p].values() if is_data(f) and fnmatch(f.name,pattern)]
    return datafiles
    

def composites(pm, pkg_name=None):
    pkgs = get_packages(pm, pkg_name)
    cn = [f for p in pkgs for f in pm[p].values() if is_cn(f) ]
    return cn

def nodes(pm, pkg_name=None):
    pkgs = get_packages(pm, pkg_name)
    nf = [f for p in pkgs for f in pm[p].values() if is_node(f) ]
    return nf

def cn_deps(pm, cn_factory):
    """ return all the factory dependencies of a composite node. """
    f = cn_factory
    if not is_cn(f):
        return 
    for p,n in f.elt_factory.values():
        try:
            fact = pm[p][n]
        except:
            continue
        yield fact
        for df in cn_deps(pm, fact):
            yield df

def composite_dependencies(pm, cn_factory):
    factories = set((f.package.name, f.name) for f in cn_deps(pm, cn_factory))
    return factories

def cn_pkgs_deps(pm, cn_factory):
    fs = composite_dependencies(pm, cn_factory)
    pkgs = set(f[0] for f in fs)
    l = list(pkgs)
    return sorted(l)

def package_dependencies(pm, package):
    cns = [f for f in package.itervalues() if is_cn(f)]
    factories = set((f.package.name, f.name) for cn_factory in cns for f in cn_deps(pm, cn_factory))
    pkgs = set(f for f in factories if f[0] != package.name)
    l = list(pkgs)
    return sorted(l)

def uid(factory):
    return '.'.join([factory.package.name, factory.name])

def pm_dependencies(pm):
    return dict((pkg, package_dependencies(pm, pm[pkg])) for pkg in get_packages(pm))

def score_packages(pm):
    d = pm_dependencies(pm)

    score = {}
    for k, l in d.iteritems():
        for p in l:
            score.setdefault(p,0)
            score[p]+=1

    new_score = {}
    for k, v in score.iteritems():
        new_score.setdefault(v,[]).append(k)
    return new_score

def print_score(score):
     for i in sorted(score.keys()):
         print
         print i, score[i]

