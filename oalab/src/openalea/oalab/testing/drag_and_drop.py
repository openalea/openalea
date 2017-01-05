###############################################################################
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

from Qt import QtGui, QtWidgets

from openalea.oalab.testing.mimedata import SampleCustomData
from openalea.oalab.service.drag_and_drop import add_drop_callback, add_drag_format, encode_to_qmimedata

class DragModel(QtGui.QStandardItemModel):

    def __init__(self):
        QtGui.QStandardItemModel.__init__(self)
        self._lst = list('abc')
        for l in self._lst:
            self.appendRow(QtGui.QStandardItem(l))

        # Define all type of data managed by this model
        add_drag_format(self, "custom/data", icon=":/images/resources/openalealogo.png")

    def mimeData(self, indices):
        for index in indices:
            row = index.row()
        data = SampleCustomData(row, self._lst[row])
        return encode_to_qmimedata(data, 'custom/data')

class DragWidget(QtWidgets.QTreeView):

    def __init__(self):
        QtWidgets.QTreeView.__init__(self)

        self.setDragEnabled(True)
        self.setDragDropMode(self.DragOnly)
        self.model = DragModel()
        self.setModel(self.model)

class DropWidget(QtWidgets.QLabel):

    def __init__(self):
        QtWidgets.QLabel.__init__(self, "Drop here .................................................")
        add_drop_callback(self, 'openalea/interface.IImage', self.drop)
        add_drop_callback(self, 'openalea/interface.IPath', self.drop)
        add_drop_callback(self, 'openalealab/control', self.drop)
        add_drop_callback(self, 'custom/data', self.drop)
        add_drop_callback(self, 'text/plain', self.drop)

    def drop(self, data, **kwds):
        self.setText(repr(data))

class DragAndDropWidget(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QHBoxLayout(self)

        self.drag = DragWidget()
        self.drop = DropWidget()

        layout.addWidget(self.drag)
        layout.addWidget(self.drop)
