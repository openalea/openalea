# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

from Qt import QtWidgets

from openalea.oalab.testing.drag_and_drop import DragAndDropWidget
from openalea.oalab.service.drag_and_drop import (add_drop_callback, add_drag_format, encode_to_qmimedata)

instance = QtWidgets.QApplication.instance()
if instance is None:
    app = QtWidgets.QApplication([])
else:
    app = instance

dnd = DragAndDropWidget()
dnd.show()

if instance is None:
    app.exec_()
