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
from openalea.core.service.plugin import plugin_instance_exists, plugin_instance
from openalea.core.service.data import DataFactory
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

    def __init__(self):
        super(FileBrowser, self).__init__()

    def _get_paradigm_container(self):
        if plugin_instance_exists('oalab.applet', 'EditorManager'):
            return plugin_instance('oalab.applet', 'EditorManager')
    paradigm_container = property(fget=_get_paradigm_container)

    def open_file(self, index):
        # TODO: Use signal
        filename = self.model.filePath(index)
        if filename:
            paradigm_container = self.paradigm_container
            if paradigm_container:
                paradigm_container.open_data(DataFactory(filename))


def main():
    app = QtGui.QApplication(sys.argv)

    wid = FileBrowser()
    wid.show()
    app.exec_()


if __name__ == "__main__":
    main()
