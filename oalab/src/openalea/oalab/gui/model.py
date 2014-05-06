# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
from openalea.vpltk.qt import QtGui, QtCore
import sys


class InputsModel(QtGui.QWidget):
    def __init__(self, world={}, parent=None):
        super(InputsModel, self).__init__(parent=parent)
        self.world = world

        layout = QtGui.QGridLayout(self)

        self.label = QtGui.QLabel("Inputs: ")

        self.combo_input = QtGui.QComboBox(self)
        self.combo_input.addItems(world.keys())

        self.add_button = QtGui.QPushButton("Add Input")
        self.add_button.clicked.connect(self.add_input)
        self.rm_button = QtGui.QPushButton("Remove Input")
        self.rm_button.clicked.connect(self.rm_input)

        self.ok_button = QtGui.QPushButton("Ok")
        self.ok_button.clicked.connect(self.print_current)

        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.combo_input, 0, 1)
        # layout.addWidget(self.add_button, 0, 2)
        # layout.addWidget(self.rm_button, 0, 3)
        # layout.addWidget(self.ok_button, 10, 0)

        self.setLayout(layout)

    def add_input(self):
        print "add"

    def rm_input(self):
        print "rm"

    def get_current(self):
        text = self.combo_input.currentText()
        return text, self.world[text]

    def print_current(self):
        print self.get_current()


class OutputsModel(QtGui.QWidget):
    def __init__(self, parent=None):
        super(OutputsModel, self).__init__(parent=parent)

        layout = QtGui.QGridLayout(self)

        self.label = QtGui.QLabel("Outputs: ")

        self.line_output = QtGui.QLineEdit(self)

        self.add_button = QtGui.QPushButton("Add Output")
        self.add_button.clicked.connect(self.add_input)
        self.rm_button = QtGui.QPushButton("Remove Output")
        self.rm_button.clicked.connect(self.rm_input)

        self.ok_button = QtGui.QPushButton("Ok")
        self.ok_button.clicked.connect(self.print_current)

        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.line_output, 0, 1)
        # layout.addWidget(self.add_button, 0, 2)
        # layout.addWidget(self.rm_button, 0, 3)
        # layout.addWidget(self.ok_button, 10, 0)

        self.setLayout(layout)

    def add_input(self):
        print "add"

    def rm_input(self):
        print "rm"

    def get_current(self):
        text = self.line_output.text()
        return text

    def print_current(self):
        print self.get_current()


class InAndOutModel(QtGui.QWidget):
    def __init__(self, world={}, parent=None):
        super(InAndOutModel, self).__init__(parent=parent)
        self.world = world

        layout = QtGui.QGridLayout(self)
        self.inp = InputsModel(self.world)
        self.outp = OutputsModel()
        layout.addWidget(self.inp)
        layout.addWidget(self.outp)

        self.ok_button = QtGui.QPushButton("Ok")
        self.ok_button.clicked.connect(self.print_current)

        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def get_current(self):
        inp = self.inp.get_current()
        outp = self.outp.get_current()
        return inp, outp

    def print_current(self):
        inp, outp = self.get_current()
        print "inputs: ", inp
        print "outputs: ", outp


def main():
    app = QtGui.QApplication(sys.argv)

    a = dict()
    a[""] = None
    a["plop"] = 1
    a["yep"] = 2
    a["test"] = 3
    a["g"] = 4

    wid = InAndOutModel(a)
    wid.show()
    app.exec_()


if __name__ == "__main__":
    main()
