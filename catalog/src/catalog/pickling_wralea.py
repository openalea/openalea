# -*- python -*-
#
#       OpenAlea.Catalog
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

__doc__ = """ Catalog.Python """

__license__ = "Cecill-C"
__revision__ = " $Id$ "


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
                    description='Python Node library.',
                    url='http://openalea.gforge.inria.fr'
                    )


    package = Package("Catalog.Pickle", metainfo)

################# node description ###################

    nf = Factory(name = "pickle load", 
                 description = "load pickled data", 
                 category = "Python", 
                 nodemodule ="pickling",
                 nodeclass = "py_load",
                 inputs = (dict(name="file_path", interface=IFileStr),
                          ),
                 outputs = (dict(name="data", interface=None,),
                           ),
                 lazy=False,
                 )

    package.add_factory(nf)

    nf = Factory(name = "pickle dump", 
                 description = "pickled data writer", 
                 category = "Python", 
                 nodemodule ="pickling",
                 nodeclass = "py_dump",
                 inputs = (dict(name="data", interface=None,),
                           dict(name="file_path", interface=IFileStr),
                           dict(name="append", interface=IBool, value=False,),
                          ),
                 outputs = (),
                 lazy=False,
                 )

    package.add_factory(nf)




############### end node description #################

    pkgmanager.add_package(package)

