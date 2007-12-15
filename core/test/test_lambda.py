

# Test for lambda functions

from openalea.core.pkgmanager import PackageManager

def test_lambda():
    pm = PackageManager ()
    pm.init()

    import testnodes
    testnodes.register_packages(pm)
    
    for t, id, res in (
        ('LambdaFactoriel', 2, 362880),
        ('testlambdaFor', 3, 12),
        ('testlambdaFor', 9, [3628800, 11]),
        ('testorder', 4, [1.,2.]),
        ('TestLambda', 3, map( lambda x: (x+5)*5, range(10))),
        ('testlambda2', 10, filter( lambda x: x>=2 and x <= 7, range(10))),
        ('testlambda3', 3, map( lambda y : filter( lambda x: x>=7, y), [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]) ),         ):

        print "run", t
        n = pm.get_node("TestLambda", t)
        n()
        assert n.node(id).get_output(0) == res

#test_lambda()
