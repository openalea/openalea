# -*- coding: utf-8 -*-
# -*- python -*-
#
#       TissueLab
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Cerutti <guillaume.cerutti@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       TissueLab Website : http://virtualplants.github.io/
#
###############################################################################

from openalea.deploy.shared_data import shared_data
import openalea.image
from openalea.oalab.colormap.colormap_utils import Colormap, colormap_from_file
from openalea.oalab.control.widget import AbstractQtControlWidget
from openalea.oalab.widget.basic import QFloatSlider, QSpanSlider, QColormapBar
from openalea.vpltk.qt import QtCore, QtGui


class ColormapRectangle(QtGui.QColormapBar, AbstractQtControlWidget):
    valueChanged = QtCore.Signal(dict)

    def __init__(self):
        QColormapBar.__init__(self)

        self.setAutoFillBackground(True)

        AbstractQtControlWidget.__init__(self)
        self.setMinimumHeight(40)

        self.value_changed_signal = self.valueChanged

    def reset(self, value=dict(name='grey', color_points=dict(
            [(0.0, (0.0, 0.0, 0.0)), (1.0, (1.0, 1.0, 1.0))])), **kwargs):
        self.setValue(value)

    def read(self, control):
        self.reset(control.value)

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)


class ColormapSwitcher(QtGui.QWidget, AbstractQtControlWidget):
    valueChanged = QtCore.Signal(dict)

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.colormap_bar = QColormapBar()
        self.colormap_bar.setMinimumHeight(20)
        self.colormap_bar.setMinimumWidth(120)

        self.colormap_name = "grey"

        # self.label = QtGui.QLabel(self)
        # self.label.setText("Colormap")

        self.combobox = QtGui.QComboBox(self)

        # self.setMinimumHeight(50)

        colormap_names = []
        # colormaps_path = Path(shared_data(tissuelab, 'colormaps/grey.lut')).parent
        colormaps_path = shared_data(openalea.image) / 'colormaps'
        for colormap_file in colormaps_path.walkfiles('*.lut'):
            colormap_name = str(colormap_file.name[:-4])
            colormap_names.append(colormap_name)
        colormap_names.sort()

        # map between string and combobox index
        self.map_index = {}
        for s in colormap_names:
            self.combobox.addItem(s)
            self.map_index[s] = self.combobox.count() - 1
        self.combobox.setCurrentIndex(self.map_index[self.colormap_name])

        # Fill background to avoid to see text or widget behind
        self.setAutoFillBackground(True)

        AbstractQtControlWidget.__init__(self)

        self.combobox.currentIndexChanged.connect(self.updateColormap)
        self.colormap_bar.valueChanged.connect(self.valueChanged)

        layout = QtGui.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # line = QtGui.QHBoxLayout(self)
        # line.setContentsMargins(0, 0, 0, 0)

        # line.addWidget(self.label)
        # line.addWidget(self.combobox)
        # layout.addLayout(line)
        layout.addWidget(self.combobox)
        layout.addWidget(self.colormap_bar)

        self.value_changed_signal = self.valueChanged

    def reset(self, value=dict(name='grey', color_points=dict(
            [(0.0, (0.0, 0.0, 0.0)), (1.0, (1.0, 1.0, 1.0))])), **kwargs):
        self.setValue(value)

    def read(self, control):
        self.reset(control.value)

    def apply(self, control):
        AbstractQtControlWidget.apply(self, control)

    def value(self, interface=None):
        return self.colormap_bar.value()

    def setValue(self, value):
        self.colormap_bar.setValue(value)
        self.colormap_name = value['name']
        self.combobox.setCurrentIndex(self.map_index[self.colormap_name])

    def updateColormap(self, colormap_index):
        self.colormap_name = self.combobox.itemText(colormap_index)

        colormap_path = shared_data(openalea.oalab, 'colormaps/' + self.colormap_name + '.lut')

        colormap = colormap_from_file(colormap_path, name=self.colormap_name)
        self.setValue(dict(name=self.colormap_name, color_points=colormap._color_points))
