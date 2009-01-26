"""
Test the Package Mngr
"""

import os
pj=os.path.join
import sys
sys.path.append(pj("..","src"))

import package
from package import NodeFactory, WidgetFactory, Package,\
                    pid, alea_package

class MyNode(object):
    def __call__(self):
        s="Node called\n"
        print s
        return s

class MyWidget(object):
    def __init__(self, node):
        s= "widget called\n"
        n= node()
        print s+n

def node_factory1():
    return NodeFactory( "MyNode", "This is my node",
                    "Category",["gnuplot","amlPy"],MyNode)

def widget_factory1():
    return WidgetFactory( "MyWidget","image.jpg",MyWidget,MyNode)

def test_NodeFactory_ctor():
    n= NodeFactory( "MyNode", "This is my node",
                    "Category",["gnuplot","amlPy"],MyNode)
    assert(n)

def test_NodeFactory_call():
    n= NodeFactory( "MyNode", "This is my node",
                    "Category",["gnuplot","amlPy"],MyNode)
    node= n()
    assert(node)

def test_WidgetFactory_ctor():
    wf= WidgetFactory( "MyWidget","image.jpg",MyWidget,MyNode)
    assert(wf)

def test_WidgetFactory_call():
    wf= WidgetFactory( "MyWidget","image.jpg",MyWidget,MyNode)
    node= MyNode()
    widget= wf(node)
    assert(widget)

def pkg_os():
    p= Package('os','os','0.0.1')
    return p

def pkg_node():
    p= Package('node','node','0.0.1',node_factories=[node_factory1()])
    return p

def pkg_widget():
    p= Package('widget','widget','0.0.1',node_factories=[node_factory1()],
               widget_factories=[widget_factory1()])
    return p


def test_package_ctor1():
    assert(pkg_os())

def test_package_ctor2():
    assert(pkg_node())

def test_package_ctor3():
    assert(pkg_widget())

def test_package_node():
    pkg= pkg_widget()
    nodes= pkg.nodes
    print nodes
    assert nodes

    deps=pkg.dependencies
    print deps
    assert deps

    assert pkg.load()

    assert pid(pkg) == "widget"

    alea_pkg= alea_package()
    assert alea_pkg

    #pkg.install(alea_pkg)
    #assert pkg.installed

    #pkg.uninstall(alea_pkg)
    #assert not pkg.installed

###############################################################################

def test_pm1():

    p1= pkg_os()
    p2= pkg_node()
    p3= pkg_widget()

    pm= package.PackageManager()
    assert pm

    pm.register(p1)
    assert len(pm.packages()) == 1
    pm.register(p2)
    assert len(pm.packages()) == 2
    pm.register(p3)
    assert len(pm.packages()) == 3

    assert pm.unregister(p2)
    assert len(pm.packages()) == 2

    # TODO: error "tata" is name, not a package
    # assert not pm.unregister("tata")

    assert not pm.loaded_packages()
    assert not pm.installed_packages()

    assert 'widget' in pm.packages()
    widget_pkg=pm['widget']
    assert widget_pkg
    
    nf=widget_pkg.node_factories[-1]
    assert nf
    
    node_instance= nf()
    assert node_instance

    widget_result= pm.widget(node_instance)
    print widget_result
    assert widget_result

    pm.unregister(p1)
    print pm.widget(node_instance)
    
    pm.unregister(p3)
    assert not pm.widget(node_instance)

def test_pm_factories():
    p1= pkg_os()
    p2= pkg_node()
    p3= pkg_widget()

    package.register(p1)

    pm= package.load_pkg_manager()
    assert len(pm.packages()) == 1

    package.register(p2)
    pm= package.load_pkg_manager()
    assert len(pm.packages()) == 2

    package.register(p3)
    pm= package.load_pkg_manager()
    assert len(pm.packages()) == 3

    package.unregister(p1)
    package.unregister(p2)
    package.unregister(p3)

    pm= package.load_pkg_manager()
    assert len(pm.packages()) == 0
    
    pm= package.PackageManager()
    package.save_pkg_manager(pm)

######################################################

def test_pkg_install():
    '''
    test of the pakage installation process
    '''
    from path import path 
    import config 

    src_dir= path(__file__).dirname().abspath()
    package_tree = [ 'lib/toto.dll', 'bin/toto.exe', 'include/toto.h', 'examples/toto.exp', 'packages/toto.py', 'documentation/toto.doc', 'resources/toto.rsc', 'tests/toto.tst' ]
    package_tree= [ src_dir / f for f in package_tree ]
    toto_pkg = pkg_os()
    toto_pkg.name = 'toto'
    toto_pkg.directories = {} 

    tempdir = src_dir
    destdir = config.prefix
    print "source dir is " + tempdir 
    print 'destination dir is ' + destdir
    
    for k in package_tree:      
        toto_pkg.directories[path(k).dirname()] = k
        f= k
        print f
        dir= f.dirname()
        if not dir.exists():
            dir.mkdir()
        if not f.exists():
            f.touch()

    toto_pkg.install()

    result = True
    files_to_remove =[]
    dirs_to_remove =[]
    for k in package_tree:
        # make sure the file was copied
        src,f = k.splitall()[-2:]

        if src =='bin' or src ==  'lib':
            fn= destdir / src / f
        else:
            d= destdir / src / 'toto'
            fn= d / f
            dirs_to_remove.append(d)

        assert fn.exists()
        files_to_remove.append(fn)
            
    for fn in files_to_remove:
        fn.remove()

    # remove created deirectories
    for d in dirs_to_remove:
        d.rmdir()

    for d in toto_pkg.directories.keys():
        d.rmtree()
    
