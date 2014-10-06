"""Export Tests"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core import export_app
from openalea.core.pkgmanager import PackageManager
from openalea.core import *
import os

def test_export():
    """test export"""
    d= {}
    execfile('catalog.py', globals(), d)
    pkg = d['pkg']
    plus_node= pkg['plus'].instantiate()
    float_node= pkg['float'].instantiate()
    int_node= pkg['int'].instantiate()
    string_node= pkg['string'].instantiate()
    pm = PackageManager()
    pm.add_package(pkg)

    sg = CompositeNode()

    # build the compositenode factory
    addid = sg.add_node(plus_node)
    val1id = sg.add_node(float_node)
    val2id = sg.add_node(float_node)
    val3id = sg.add_node(float_node)

    sg.connect(val1id, 0, addid, 0)
    sg.connect(val2id, 0, addid, 1)
    sg.connect(addid, 0, val3id, 0)

    sgfactory = CompositeNodeFactory("addition")
    sg.to_factory(sgfactory)

    export_app.export_app("ADD", "app.py", sgfactory)

    f = open("app.py")
    assert f

    import app
    # requires X server 
    # app.main(sys.argv)
    f.close()
    os.remove("app.py")
    try:
        os.remove("app.pyc")
    except:
        pass

