# -*- python -*-
#
#       OpenAlea.Catalog.Library: OpenAlea Catalog Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): BOUDON Frederic <frederic.boudon@cirad.fr>
#                       Da SILVA David <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
Wralea for Core.Library 
"""

__license__= "Cecill-C"
__revision__=" $Id: python_wralea.py 799 2007-10-01 06:41:20Z dufourko $ "


from openalea.core import *



def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """

    # Base Library

    metainfo = dict(version='0.0.1',
                    license='CECILL-C',
                    authors='OpenAlea Consortium',
                    institutes='INRIA/CIRAD',
                    description='Csv Node library.',
                    url='http://openalea.gforge.inria.fr'
                    )


    package = Package("Catalog.Csv", metainfo)


    # Factories
    nf = Factory(name="csv2objs", 
                 description="Csv converter", 
                 category="Csv", 
                 nodemodule="csv",
                 nodeclass="parseText",
                 outputs=(dict(name='objects', interface=None),
                          dict(name='header', interface=None),)
                 )

    package.add_factory(nf)

    nf = Factory(name="obj2cvs", 
                 description="Csv exporter", 
                 category="Csv", 
                 nodemodule="csv",
                 nodeclass="writeObjs",
                 outputs=(dict(name='string', interface=IStr),)
                 )

    package.add_factory(nf)

    pkgmanager.add_package(package)

