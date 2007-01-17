# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
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
__revision__=" $Id$ "



from openalea.core.core import Package
import arithmetics_factory
import dummy_model_fact

def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """


    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'SDK, CP',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'Arithmetic nodes.',
               }


    package = Package("arithmetics", metainfo)
    
    arithmetics_factory.define_factory(package)
    dummy_model_fact.define_factory(package)

    pkgmanager.add_package(package)


        




        



    
