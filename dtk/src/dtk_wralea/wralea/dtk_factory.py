# -*- python -*-
#
#       dtk function definition
#
#       2010 INRIA - CIRAD - INRA  
#
#       File author(s): Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

from openalea.core.external import *

def define_factory(package):
    """ Define factories for dtk nodes """

    nf = Factory( name= "dtkDataReader", 
                  description= "", 
                  category = "dtk.plugins", 
                  nodemodule = "py_dtk",
                  nodeclass = "dtk_DataReader",
                  )

    package.add_factory( nf )


    nf = Factory( name= "dtkDataViewer", 
                  description= "", 
                  category = "dtk.plugins", 
                  nodemodule = "py_dtk",
                  nodeclass = "dtk_DataViewer",
                  )

    package.add_factory( nf )


