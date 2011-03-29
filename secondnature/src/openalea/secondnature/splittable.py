# -*- python -*-
#
#       OpenAlea.SecondNature
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
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

__license__ = "CeCILL v2"
__revision__ = " $Id$ "

from PyQt4 import QtGui, QtCore
from openalea.visualea.splitterui import SplittableUI, DraggableWidget, RubberBandScrollArea


from openalea.secondnature.applets import AppletSpace
from openalea.secondnature.project import ProjectManager

class CustomSplittable(SplittableUI):

    paneMenuRequest = QtCore.pyqtSignal(object, int, QtCore.QPoint)

    def getPlaceHolder(self):
        proj = ProjectManager().get_active_project()
        return AppletSpace( proj )


    def _install_child(self, paneId, widget, **kwargs):
        w = SplittableUI._install_child(self, paneId, widget, **kwargs)
        self._raise_overlays(paneId)
        return w

