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

import unittest
from openalea.vpltk.qt import QtGui, QtCore
from PyQt4 import QtTest


class QtTestCase(unittest.TestCase):
    PAUSE_FACTOR = 1000
    SAVE_AS_REFERENCE = False

    def init(self):
        self._pause = False
        self._duration = 0
        self.instance = QtGui.QApplication.instance()
        if self.instance is None:
            self.app = QtGui.QApplication([])
        else:
            self.app = self.instance

        self.widget = None

    def finalize(self):
        if self.widget:
            self.widget.show()
            self.widget.raise_()

        if self._pause:
            QtTest.QTest.qWait(self._duration)

        if self.widget:
            self.widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self.widget.close()
            del self.widget

        self.app.quit()
        del self.app
        del self.instance

    def exec_(self):
        if self.instance is None:
            self.app.exec_()

    def pause(self, duration=1):
        self._duration = duration * self.PAUSE_FACTOR
        self._pause = True

    def setUp(self):
        self.init()

    def tearDown(self):
        self.finalize()
