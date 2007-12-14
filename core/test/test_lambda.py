

# Test for lambda functions

from openalea.core.pkgmanager import PackageManager

def test_lambda():
    pm = PackageManager ()
    pm.init()

    import testnodes
    testnodes.register_packages(pm)
    
    for t in ('LambdaFactoriel',
              'testlambdaFor',
              'testorder',
              'testlambda2',
              'testlambda3', ):

        print "run", t
        n = pm.get_node("TestLambda", t)
        n()

test_lambda()
