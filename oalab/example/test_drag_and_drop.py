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

from openalea.vpltk.qt import QtGui, QtCore

from openalea.core.plugin.manager import PluginManager
from openalea.oalab.mimedata import QMimeCodec, QMimeCodecPlugin


class CustomData(object):

    def __init__(self, num, letter):
        self.num = num
        self.letter = letter

    def __repr__(self, ):
        return '%s(num=%r, letter=%r)' % (self.__class__.__name__, self.num, self.letter)


class Codec(QMimeCodec):

    def decode(self, raw_data, mimetype_in, mimetype_out):
        num, letter = raw_data.split(';')
        num = int(num)
        if mimetype_out == 'custom/data':
            data = CustomData(num, letter)
        elif mimetype_out == 'openalealab/control':
            from openalea.core.control import Control
            data = Control(letter, 'IInt', num)
        elif mimetype_out == 'text/plain':
            data = 'customdata: %s, %s' % (letter, num)
        elif mimetype_out == 'text/plain.verbose':
            data = 'Custom data define these values:\n  - letter: %s\n  - num: %s' % (letter, num)
        return data, {}

    def encode(self, data, mimetype_in, mimetype_out):
        return mimetype_out, '%s;%s' % (data.num, data.letter)


class SampleCodecPlugin(QMimeCodecPlugin):
    qtencode = [
        ("custom/data", "custom/data"),
    ]
    qtdecode = [
        ("custom/data", "custom/data"),
        ("custom/data", "openalealab/control"),
        ("custom/data", "text/plain"),
        ("custom/data", "text/plain.verbose"),
    ]

    mimetype_desc = {
        'text/plain': dict(title='Short Text'),
        'text/plain.verbose': dict(title='Long Text'),
        'custom/data': dict(title='Custom data'),
        'openalealab/control': dict(title='Control'),
    }

    def __call__(self):
        return Codec

pm = PluginManager()
pm.add_plugin('openalea.codec.mimetype', SampleCodecPlugin)

instance = QtGui.QApplication.instance()
if instance is None:
    app = QtGui.QApplication([])
else:
    app = instance

from openalea.oalab.service.drag_and_drop import add_drop_callback, add_drag_format, encode


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
        data = CustomData(row, self._lst[row])
        return encode(self, data, 'custom/data')


class DragWidget(QtGui.QTreeView):

    def __init__(self):
        QtGui.QTreeView.__init__(self)

        self.setDragEnabled(True)
        self.setDragDropMode(self.DragOnly)
        self._model = DragModel()
        self.setModel(self._model)


class DropWidget(QtGui.QLabel):

    def __init__(self):
        QtGui.QLabel.__init__(self, "Drop here .................................................")
        add_drop_callback(self, 'openalea/interface.IImage', self.drop)
        add_drop_callback(self, 'openalea/interface.IPath', self.drop)
        add_drop_callback(self, 'openalealab/control', self.drop)
        add_drop_callback(self, 'custom/data', self.drop)
        add_drop_callback(self, 'text/plain', self.drop)

    def drop(self, data, **kwds):
        self.setText(repr(data))

drag = DragWidget()
drag.show()

drop = DropWidget()
drop.show()

if instance is None:
    app.exec_()
