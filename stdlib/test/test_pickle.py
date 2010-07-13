import pickle

from  openalea.core import alea

pm = alea.load_package_manager()

def subdataflow():
    factory = pm['openalea.tutorial.multiprocess']['x+1']
    f = alea.function(factory)
    return f()[0]

def test0():
    l  = pm.search_node('int')
    n = l[0]
    pickle.dumps(n.instantiate())

def test1():
    pickle.dumps(subdataflow())

def test2():
    sdf = subdataflow()
    pickle.dumps(sdf.dataflow)

def test3():
    sdf = subdataflow()
    pickle.dumps(sdf.algo)

def check(node):
    d = node.__getstate__()
    for k, v in d.iteritems():
        try:
            pickle.dumps(v)
        except:
            print 'Pickle Error ', k


