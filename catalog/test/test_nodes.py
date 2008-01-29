# Test Nodes


from openalea.core.pkgmanager import PackageManager

def test_init():
    """ Test the node intialisation """

    pm = PackageManager()
    pm.add_wraleapath('../src/catalog')
    pm.find_and_register_packages()

    for p in pm.keys():
        print p
        if('catalog' in p): 
            pkg = pm[p]
            for factory in pkg.values():
                print factory.name
                factory.instantiate()


test_init()
