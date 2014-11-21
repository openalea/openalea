# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

from openalea.core.node import NodeFactory
from openalea.core.compositenode import CompositeNodeFactory, CompositeNode
from openalea.core.interface import IInt
from openalea.core.package import Package
from openalea.core.pkgmanager import PackageManager
from openalea.oalab.model.visualea import VisualeaModel

pm = PackageManager()
# pm.init()


def package():

    plus = NodeFactory('plus', nodemodule='operator', nodeclass='add',
                       inputs=(dict(name='a', interface=None, value=0.),
                               dict(name='b', interface=None, value=0.),
                               ),
                       outputs=(dict(name='out'),
                                )
                       )
    my_int = NodeFactory('int', nodemodule='', nodeclass='int',
                         inputs=(dict(name='in', interface=None, value=0),
                                 ),
                         outputs=(dict(name='out'),
                                  )
                         )

    pkg = Package('test', metainfo={})
    pkg.add_factory(plus)
    pkg.add_factory(my_int)

    pm.add_package(pkg)

    return pkg


def composite_node(a=1, b=2):
    pkg = package()

    plus_node = pkg['plus'].instantiate()
    int_node = pkg['int'].instantiate()

    if a is None:
        input_a = {'interface': IInt, 'name': 'a', 'desc': ''}
    else:
        input_a = {'interface': IInt, 'name': 'a', 'value': a, 'desc': ''}

    if b is None:
        input_b = {'interface': IInt, 'name': 'b', 'desc': ''}
    else:
        input_b = {'interface': IInt, 'name': 'b', 'value': b, 'desc': ''}

    sg = CompositeNode(
        inputs=[input_a, input_b],
        outputs=[{'interface': IInt, 'name': 'a', 'desc': 'result'}],
    )

    # build the compositenode factory
    addid = sg.add_node(plus_node)

    sg.connect(sg.id_in, 0, addid, 0)
    sg.connect(sg.id_in, 1, addid, 1)
    sg.connect(addid, 0, sg.id_out, 0)

    sgfactory = CompositeNodeFactory("addition")
    sg.to_factory(sgfactory)

    return sgfactory


def test_io():

    sgfactory = composite_node()

    model = VisualeaModel()
    model.set_code(sgfactory)

    assert model() == 3
    assert model(10, 20) == 30
    assert model.run() == 3


def test_io_no_default():
    from openalea.core.service.control import new_control, clear_controls
    clear_controls()
    sgfactory = composite_node(None, None)

    model = VisualeaModel()
    model.set_code(sgfactory)

    a = 100
    b = 200
    assert model(namespace=locals()) == 300
    assert model(**locals()) == 300

    new_control('a', 'IInt', 5)
    assert model(a=1, b=20, namespace=locals()) == 21
    assert model(b=20, namespace=locals()) == 25
