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

from openalea.vpltk.qt import QtCore, QtGui

class EscEventSwallower(QtCore.QObject):
    def eventFilter(self, watched, event):
        if event.type() in [QtCore.QEvent.KeyPress, QtCore.QEvent.KeyRelease]:
            if event.key() == QtCore.Qt.Key_Escape:
                return True
        return False


class ComboBox(QtGui.QComboBox):
    def setCurrentIndex(self, index):
        QtGui.QComboBox.setCurrentIndex(self, index)
        self.activated[int].emit(self.currentIndex())




def try_to_disconnect(signal, slot=None):
    try:
        if slot:
            signal.disconnect(slot)
        else:
            signal.disconnect()
    except TypeError:
        pass
