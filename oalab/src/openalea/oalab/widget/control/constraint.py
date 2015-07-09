# -*- coding: utf-8 -*-

from openalea.vpltk.qt import QtGui    

class IntConstraintWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        layout = QtGui.QFormLayout(self)

        self.e_min = QtGui.QLineEdit('0')
        self.e_max = QtGui.QLineEdit('100')
        text = 'Can be an int (for instance -5) or empty (no limits)'
        self.e_min.setToolTip(text)
        self.e_min.setWhatsThis(text)
        self.e_max.setToolTip(text)
        self.e_max.setWhatsThis(text)

        layout.addRow(QtGui.QLabel('Minimum'), self.e_min)
        layout.addRow(QtGui.QLabel('Maximum'), self.e_max)

    def constraints(self):
        dic = {}
        try:
            dic['min'] = int(self.e_min.text())
        except ValueError:
            pass

        try:
            dic['max'] = int(self.e_max.text())
        except ValueError:
            pass

        return dic


class FloatConstraintWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        layout = QtGui.QFormLayout(self)

        self.e_min = QtGui.QLineEdit('0.0')
        self.e_max = QtGui.QLineEdit('1.0')
        self.e_step = QtGui.QLineEdit('0.01')
        text = 'Can be a float (for instance -0.5) or empty (no limits)'
        self.e_min.setToolTip(text)
        self.e_min.setWhatsThis(text)
        self.e_max.setToolTip(text)
        self.e_max.setWhatsThis(text)
        text = 'Must be a positive float (for instance 0.1)'
        self.e_step.setToolTip(text)
        self.e_step.setWhatsThis(text)

        layout.addRow(QtGui.QLabel('Minimum'), self.e_min)
        layout.addRow(QtGui.QLabel('Maximum'), self.e_max)
        layout.addRow(QtGui.QLabel('Step'), self.e_step)

    def constraints(self):
        dic = {}
        try:
            dic['min'] = float(self.e_min.text())
        except ValueError:
            pass
        try:
            dic['max'] = float(self.e_max.text())
        except ValueError:
            pass
        try: 
            dic['max'] = float(self.e_step.text())
            if dic['max']<0:
                dic['max'] = 0.01
        except ValueError:
            pass
        return dic