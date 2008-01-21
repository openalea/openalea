# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2008 INRIA - CIRAD - INRA  
#
#       File author(s): Szymon Stoma <szymon.stoma@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################


__doc__="""
View for organizing the compontent lookout.
"""

__license__= "Cecill-C"
__revision__=" $Id: node.py 1016 2008-01-10 10:44:12Z dufourko $ "


class View( object ):
    """Describes the layaout of widget.
    
    <Long description of the class functionality.>
    """
    def __init__( self, *values, **kargs ):
        """Basic constructor.
        """
        self.content = values
        print values
    
class Item( object ):
    """Describes the atom of View.
    
    <Long description of the class functionality.>
    """
    def __init__( self, name, show_label=True, **keys ):
        """Basic constructor.
        """
        self.name = name
        self.show_label = show_label

class Group( object ):
    """Describes the group for  View.
    
    <Long description of the class functionality.>
    """
    def __init__( self, label, *values, **keys ):
        """Basic constructor.
        """
        self.content = values
        self.label = label
        #self.content = values
