# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
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
System Nodes
"""

__license__= "Cecill-C"
__revision__=" $Id: python.py 604 2007-06-21 17:30:12Z dufourko $ "

from openalea.core.node import AbstractNode

class AnnotationNode(AbstractNode):
    """ A DummyNode is a fake node."""

    __graphitem__ = "annotation.Annotation"

    def get_nb_input(self):
        """ Return the nb of input ports """
        return 0

    
    def get_nb_output(self):
        """ Return the nb of output ports """
        return 0

    def eval(self):
        return False
