# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): David Da SILVA <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Wralea for Catalog.PlotTools 
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


from openalea.core import *
 

def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """

    # Base Library

    metainfo = { 'version' : '0.0.1',
                 'license' : 'CECILL-C',
                 'authors' : 'OpenAlea Consortium',
                 'institutes' : 'INRIA/CIRAD',
                 'description' : 'Catalog library.',
                 'url' : 'http://openalea.gforge.inria.fr'
                 }


    package = Package("Catalog.PlotTools", metainfo)

    nf = Factory( name= "Plot2D", 
                  description="Plot a list of 2D plotable objects", 
                  category="Vizualisation", 
                  nodemodule="plotools",
                  nodeclass="Plot2D",
                  inputs=(dict(name='plotObjList', interface=ISequence, showwidget=False),
                          dict(name='title', interface=IStr, value='MyPlot'),
                            dict(name='xlabel', interface=IStr, value='x-axis-label'),
                            dict(name='ylabel', interface=IStr, value='y-axis-label'),  ),
                  outputs=()

                )

    package.add_factory(nf)


    nf = Factory( name= "Plotable", 
                  description="Allows us to edit plotable object", 
                  category="Vizualisation", 
                  nodemodule="plotools",
                  nodeclass="IPlotable",
                  inputs=(dict(name='plotable', interface=None, showwidget=False),
                            dict(name='legend', interface=IStr, value='Default'),
                            dict(name='linestyle', interface=IStr, value='Default'),
                            dict(name='marker', interface=IStr, value='Default'),
                            dict(name='color', interface=IStr, value='Default'), ),
                  outputs=( dict(name='Plotable', interface=None), )
                )
    package.add_factory(nf)

    pkgmanager.add_package(package)



