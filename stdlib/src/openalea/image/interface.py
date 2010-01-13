# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""declaration of pix interface and its widget """

__license__ = "Cecill-C"
__revision__ = " $Id$"

from openalea.core.interface import IEnumStr, IInterface, IInterfaceMetaClass

class IImageMode(IEnumStr) :
    """
    interface for different modes of an image
    """
    def __init__ (self) :
        IEnumStr.__init__(self, ["RGB", "RGBA"])



class IPix(IInterface):
    """ Image interface """
    __metaclass__ = IInterfaceMetaClass
 
    # interface methods



