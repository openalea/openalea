# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "Cecill-C"
__revision__ = " $Id: color.py 2757 2010-08-12 14:43:58Z dbarbeau $ "

from openalea.vpltk.qt import qt
from openalea.visualea.graph_operator.base import Base

class AnnotationOperators(Base):
    STYLE_SIMPLE=0
    STYLE_BOX=1

    def annotation_set_style(self, style):
        master = self.master
        annotationItem = master.get_annotation_item()
        annotationItem.store_view_data(visualStyle=style)

    def annotation_change_style_simple(self):
        self.annotation_set_style(AnnotationOperators.STYLE_SIMPLE)

    def annotation_change_style_box(self):
        self.annotation_set_style(AnnotationOperators.STYLE_BOX)
