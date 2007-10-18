
from openalea.core import *

def register_packages(pkgmanager):
    
    metainfo = {} 
    pkg = Package("Catalog.Color", metainfo)

    nf = Factory(name='ColorMap', 
                 description='defines a color map from a range of values [I,J] to RGB', 
                 category='Visualisation.Color', 
                 nodemodule='py_color',
                 nodeclass='color_map',
                 inputs=[{'interface': IFloat, 'name': 'val'}, {'interface': IFloat, 'name': 'minval', 'value': 0}, {'interface': IFloat, 'name': 'maxval', 'value': 1}, {'interface': IFloat, 'name': 'color1HSV', 'value': 20}, {'interface': IFloat, 'name': 'color2HSV', 'value': 80}],
                 outputs=[{'interface': IRGBColor, 'name': 'color'}],
                 widgetmodule=None,
                 widgetclass=None,
                 )

    pkg.add_factory( nf )

    pkgmanager.add_package(pkg)


