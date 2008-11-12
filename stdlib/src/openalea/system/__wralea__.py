# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__doc__="""
Wralea for System nodes
"""

__revision__=" $Id: __wralea__.py 1317 2008-07-10 16:06:28Z dufourko $ "


from openalea.core.external import *
from openalea.core.pkgdict import protected


__name__ = "openalea.system"

__version__ = '0.0.2'
__license__= "Cecill-C"
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'System Node library.'
__url__ = 'http://openalea.gforge.inria.fr'



__all__ = []


cmd = Factory(name=protected("command"), 
             description="Call a system command", 
             category="System", 
             nodemodule="systemnodes",
             nodeclass="system_cmd",
             inputs = (dict(name="commands", interface=ISequence, value=[], 
                            desc='List of command strings'),  
                       ),
             outputs = ( dict(name="stdout", interface=None, desc='result'), 
                         dict(name="stderr", interface=None, desc='result'), ),
                     )



__all__.append('cmd')




