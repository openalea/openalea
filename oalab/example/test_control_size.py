
from openalea.vpltk.qt import QtGui, QtCore
from control_sizes import Ui_Form

import openalea.oalab.service.control as scontrol
from openalea.oalab.control.control import Control

class CheckSizes(Ui_Form, QtGui.QWidget):
    def __init__(self, iname='IInt', widget=None, edit_mode='edit'):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

        self.l_title.setText('%s, %s, %s' % (iname, widget, edit_mode))

        control = Control('a', iname, widget=widget)

#        m = getattr(scontrol, '%s_qt' % edit_mode)
        m = getattr(scontrol, 'qt_editor')

        for shape in ['hline', 'vline', 'small', 'large', 'responsive']:
            layout = getattr(self, 'l_%s' % shape)
            try:
                widget = m(control, shape=shape)
            except IOError, e:
                print shape
            else:
                if widget:
                    layout.addWidget(widget)
                else:
                    layout.addWidget(QtGui.QLabel("X"))


if __name__ == '__main__':

    import sys

    instance = QtGui.QApplication.instance()
    if instance is None :
        app = QtGui.QApplication([])
    else :
        app = instance

    w = CheckSizes(*sys.argv[1:])
    w.show()
    w.raise_()

    if instance is None :
        app.exec_()
