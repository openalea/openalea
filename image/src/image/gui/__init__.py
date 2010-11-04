# -*- python -*-
#
#       image: image manipulation GUI
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
This module import functions to graphicaly interact with images
"""

__license__= "Cecill-C"
__revision__ = " $Id: $ "

from pixmap import to_img,to_pix,to_tex

#from scalable_view import *
from animator import FrameAnimator
from pixmap_view import *
from slide_viewer import *
from palette import *
from point_selection import *

#try :
#	from stack_view import StackView
#except ImportError :
#	print "pglviewer views not available"
