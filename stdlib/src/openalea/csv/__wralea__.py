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


__doc__ = """ Catalog.CSV """
__revision__=" $Id$ "


from openalea.core import *

__name__ = "openalea.csv"
__alias__ = ["catalog.csv"]

__version__ = '0.0.1',
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Csv Node library.'
__url__ = 'http://openalea.gforge.inria.fr'



__all__ = ['csv2objs', 'obj2csv']

csv2objs = Factory(name="csv2objs", 
                   description="Csv converter", 
                   category="Csv", 
                   nodemodule="csv",
                   nodeclass="parseText",
                   lazy = False,
                   outputs=(dict(name='objects', interface=None),
                            dict(name='header', interface=None),)
                   )


obj2csv = Factory(name="obj2csv", 
                  description="Csv exporter", 
                  category="Csv", 
                  nodemodule="csv",
                  nodeclass="writeObjs",
                  lazy = False,
                  outputs=(dict(name='string', interface=IStr),)
                  )


