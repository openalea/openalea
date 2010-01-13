# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

""" openalea.multiprocessing operator """
__revision__=" $Id$ "


from openalea.core import *

__name__ = "openalea.multiprocessing"

__alias__ = []

__version__ = '0.0.2'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Functional Node library.'
__url__ = 'http://openalea.gforge.inria.fr'

__all__ = ['pmap_',]    


pmap_ = Factory( name="pmap",
               description="Apply a function on a sequence",
               category="Functional",
               inputs=(dict(name='func', interface=IFunction), 
                       dict(name='seq', interface=ISequence), 
                       dict(name='N', interface=IInt(min=1))),
               nodemodule="parallel",
               nodeclass="pymap",
               )


