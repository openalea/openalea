# -*- python -*-

from openalea.core import *


def register_packages(pkgmanager):

    metainfo = dict(version='0.0.1',
                    license='CECILL-C',
                    authors='C. Pradal, C. Fournier',
                    institutes='INRA/CIRAD',
                    description='Tools to explore and display Canestra files.',
                    url='http://openalea.gforge.inria.fr'
                    )


    package = Package("Caribu.Visualisation", metainfo)

    nf = Factory( name = "Import Can File",
                  description="ld a detailled description of a can file",
                  category="Visualisation.Caribu",
                  nodemodule="py_canview",
                  nodeclass="read_can",
                  inputs=[dict(name="can file", interface=IFileStr('*.can')),],
                  outputs=[dict(name="Canestra Scene",),],
                )

    package.add_factory(nf)
    nf = Factory( name = "Read Vec File",
                  description="Returns radiation values intercepted by the plant.",
                  category="Visualisation.Caribu",
                  nodemodule="py_canview",
                  nodeclass="read_vec",
                  inputs=[dict(name="vec file", interface=IFileStr('*.vec')),],
                  outputs=[dict(name="VecSequence",interface=ISequence),],
                )

    package.add_factory(nf)

    nf = Factory( name = "Plot Can File",
                  description="Simple Plot of a can file",
                  category="Visualisation.Caribu",
                  nodemodule="py_canview",
                  nodeclass="plot_can",
                  inputs=[dict(name="can file", interface=IFileStr('*.can')),
                          dict(name="colors", interface=ISequence, value = None),],
                  outputs=(),
                )

    package.add_factory(nf)

    pkgmanager.add_package(package)


