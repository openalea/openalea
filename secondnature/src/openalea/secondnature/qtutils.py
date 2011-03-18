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

from PyQt4 import QtCore, QtGui

class EscEventSwallower(QtCore.QObject):
    def eventFilter(self, watched, event):
        if event.type() in [QtCore.QEvent.KeyPress, QtCore.QEvent.KeyRelease]:
            if event.key() == QtCore.Qt.Key_Escape:
                return True
        return False


class ComboBox(QtGui.QComboBox):

    aboutToShow = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        QtGui.QComboBox.__init__(self, *args, **kwargs)
        self.installEventFilter(self)

    def eventFilter(self, watched, event):
        if watched==self and event.type() == QtCore.QEvent.MouseButtonPress:
            self.aboutToShow.emit(self)
        return False


def try_to_disconnect(signal, slot=None):
    print "disconnect", signal, "from", slot
    try:
        if slot:
            signal.disconnect(slot)
        else:
            signal.disconnect()
    except TypeError:
        pass
