# Test Nodes


from openalea.core.pkgmanager import PackageManager

def test_init():
    """ Test the node intialisation """

    pm = PackageManager()
    pm.add_wraleapath('../src/catalog')
    pm.find_and_register_packages()


    pkg = pm['Library']
    for factory in pkg.values():
        factory.instantiate()

