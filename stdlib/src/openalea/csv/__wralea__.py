# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__doc__ = """ OpenAlea.file.CSV """
__revision__=" $Id$ "


from openalea.core import *
from openalea.core.pkgdict import protected

__name__ = "openalea.file.csv"
__alias__ = ["catalog.csv", "openalea.csv"]

__version__ = '0.0.2',
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Csv Node library.'
__url__ = 'http://openalea.gforge.inria.fr'



__all__ = [ 'read_csv', 'write_csv']
read_csv = Factory(name='read csv', 
                   description='Csv converter', 
                   category='io', 
                   nodemodule='csv',
                   nodeclass='parseText',
                   lazy = False,
                   outputs=(dict(name='objects', interface=None),
                            dict(name='header', interface=None),)
                   )

Alias(read_csv, 'csv2objs')

write_csv = Factory(name='write csv', 
                  description='Csv exporter', 
                  category='io', 
                  nodemodule='csv',
                  nodeclass='writeObjs',
                  lazy = False,
                  outputs=(dict(name='string', interface=IStr),)
                  )
Alias(write_csv, 'obj2csv')

