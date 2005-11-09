"""
Test the Package Mngr
"""

import sys
sys.path.append("..\src")

from package import NodeFactory, WidgetFactory, Package

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
    p= Package('os','os','0.0.1',node_factories=[node_factory1()])
    return p

def pkg_node_widget():
    p= Package('os','os','0.0.1',node_factories=[node_factory1()],
               widget_factories=[widget_factory1()])
    return p


def test_package_ctor1():
    assert(pkg_os())

def test_package_ctor2():
    assert(pkg_node())

def test_package_ctor3():
    assert(pkg_node_widget())

def test_package_node():
    pkg= pkg_node_widget()
    nodes= pkg.nodes
    print nodes
    assert nodes

    deps=pkg.dependencies
    print deps
    assert deps

    assert pkg.load()
