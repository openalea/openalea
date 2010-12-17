# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2010 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

__doc__ = """ A GUI for stdlid.python.wrap_method.SelectCallable """
__revision__ = " $Id$ "

import types
from inspect import getmembers, ismethod, isfunction, isbuiltin
from openalea.visualea.node_widget import NodeWidget, DefaultNodeWidget
from openalea.core.observer import lock_notify
from PyQt4 import QtGui, QtCore

class SelectCallable(QtGui.QWidget, NodeWidget):
    def __init__(self, node, parent):
        """
        @param node
        @param parent
        """
        QtGui.QWidget.__init__(self, parent)
        NodeWidget.__init__(self, node)

        # -- imitate DefaultNodeWidget : refactor DefaultNodeWidget??? --
        # this is because we reuse the same code from DefaultNodeWidget
        # to build the UI.
        self.widgets = []
        self.empty   = True
        # -- end of imitate DefaultNodeWidget --

        # -- own custom layout
        self.setMinimumSize(100, 20)
        # self.setSizePolicy(QtGui.QSizePolicy.Preferred,
        #                    QtGui.QSizePolicy.Preferred)
        self._mainLayout = QtGui.QVBoxLayout(self)
        self._mainLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self._mainLayout.setMargin(3)
        self._mainLayout.setSpacing(2)

        # -- the method name selection group box -- #
        self.__methodGBox = QtGui.QGroupBox("Method to wrap")
        # self.__methodGBox.setSizePolicy(QtGui.QSizePolicy.Preferred,
        #                                 QtGui.QSizePolicy.Preferred)
        self._mainLayout.addWidget(self.__methodGBox, 0, QtCore.Qt.AlignTop)

        methNameLayout = QtGui.QHBoxLayout()
        methNameLayout.setMargin(3)
        methNameLayout.setSpacing(2)

        methNameLabel  = QtGui.QLabel("Method name:")
        self.__methodComboBox = QtGui.QComboBox()
        self.__lockChoice     = QtGui.QPushButton()
        style = QtGui.QApplication.style()
        self.__lockChoice.setCheckable(True)
        self.__lockChoice.setIcon(style.standardIcon(QtGui.QStyle.SP_DialogApplyButton))
        self.__lockChoice.toggled.connect(self._methodChosen)
        methNameLayout.addWidget(methNameLabel, 0, QtCore.Qt.AlignLeft)
        methNameLayout.addWidget(self.__methodComboBox)
        methNameLayout.addWidget(self.__lockChoice, 0, QtCore.Qt.AlignLeft)

        self.__methodGBox.setLayout(methNameLayout)

        # -- The method's inputs widget --
        self.__vboxlayout = QtGui.QVBoxLayout()
        self._mainLayout.addLayout(self.__vboxlayout, 0)

        # -- map between string and combobox index --
        self.map_index = {}

        # -- initialisation --
        self.notify(node, ("input_modified", 0))
        self.__isInit =True
        toggled = bool(self.node.internal_data["methodName"] and
                       self.node.internal_data["methodSig"])
        self.__lockChoice.setChecked(toggled)
        self.__isInit =False

    def notify(self, sender, event):
        """ Notification sent by node """
        eventName = event[0]
        if eventName == "input_modified":
            inputIndex = event[1]
            if inputIndex == 0: # instance has changed
                # Read Inputs
                instance = self.node.get_input(inputIndex)
                # Update Combo Box
                seq = getmembers(instance,
                                 lambda x : ismethod(x) or isfunction(x) or isbuiltin(x))
                self.update_list(seq)

                currentMethodName = self.node.get_method_name()
                index = self.map_index.get(currentMethodName, -1)
                self.__methodComboBox.setCurrentIndex(index)

    def update_list(self, seq):
        """ Rebuild the list """
        self.map_index.clear()
        self.__methodComboBox.clear()
        for s in seq:
            name = s[0]
            if name.startswith("_"):
                continue
            self.__methodComboBox.addItem(name)
            self.map_index[name] = self.__methodComboBox.count() - 1
        self.refresh_layout()

    def refresh_layout(self):
        # refresh the layout (without these three lines, the widget won't shrink!)
        self.__methodGBox.layout().activate()
        self._mainLayout.activate()
        parent = self.parentWidget()
        if parent is not None:
            parent.layout().activate()
            parent.setGeometry(QtCore.QRect())


    def _methodChosen(self, toggled):
        style = QtGui.QApplication.style()
        if toggled:
            methodName = str(self.__methodComboBox.currentText())
            instance = self.node.get_input(0)
            # if instance is not None and not hasattr(instance, methodName):
            #     QtGui.QMessageBox.warning(self, "Type error", "Object of type " + str(type(instance)) + " does not have \n" + \
            #     "such attribute " + methodName)
            #     return
            self.__methodComboBox.setEnabled(False)
            self.__lockChoice.setIcon(style.standardIcon(QtGui.QStyle.SP_DialogCancelButton))
            if not self.__isInit:
                self.node.set_method_name(methodName)
            DefaultNodeWidget.do_layout(self, self.node, self.__vboxlayout)
        else:
            self.__methodComboBox.setEnabled(True)
            self.__lockChoice.setIcon(style.standardIcon(QtGui.QStyle.SP_DialogApplyButton))

            if not self.__isInit:
                self.node.discard_method_name()

            for i in range(self.__vboxlayout.count()):
                it = self.__vboxlayout.itemAt(0)
                if it:
                    self.__vboxlayout.removeItem(it)
                    it.widget().setAttribute(QtCore.Qt.WA_DeleteOnClose)
                    it.widget().close()
            self.widgets = []

            self.refresh_layout()



