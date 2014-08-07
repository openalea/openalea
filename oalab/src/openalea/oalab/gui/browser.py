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
###############################################################################
from openalea.vpltk.qt import QtGui, QtCore
from openalea.core import settings
import sys


class GenericFileBrowser(QtGui.QWidget):
    def __init__(self):
        super(GenericFileBrowser, self).__init__()
        layout = QtGui.QGridLayout()
        self.model = QtGui.QFileSystemModel()
        self.tree = QtGui.QTreeView()
        self.tree.setModel(self.model)
        home_dir = settings.get_default_home_dir()
        root_dir = "."
        self.model.setRootPath(root_dir)
        self.tree.setRootIndex(self.model.index(home_dir))
        layout.addWidget(self.tree)
        self.setLayout(layout)

        QtCore.QObject.connect(self.tree, QtCore.SIGNAL('doubleClicked(const QModelIndex&)'), self.open_file)

    def open_file(self, index):
        filename = self.model.filePath(index)
        if filename:
            print filename


class FileBrowser(GenericFileBrowser):
    def __init__(self, controller):
        super(FileBrowser, self).__init__()
        self.controller = controller

    def open_file(self, index):
        filename = self.model.filePath(index)
        if filename:
            self.controller.paradigm_container.open_file(filename=filename)


def main():
    app = QtGui.QApplication(sys.argv)

    wid = FileBrowser()
    wid.show()
    app.exec_()


if __name__ == "__main__":
    main()