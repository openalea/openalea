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
from openalea.core.path import path as Path
from openalea.core.service.plugin import plugin_instance_exists, plugin_instance
from openalea.core.service.data import DataFactory
from openalea.oalab.utils import qicon
import sys


class GenericFileBrowser(QtGui.QWidget):
    pathSelected = QtCore.Signal(object)

    def __init__(self):
        super(GenericFileBrowser, self).__init__()
        self.model = QtGui.QFileSystemModel()
        self.tree = QtGui.QTreeView()
        self.tree.setModel(self.model)
        self.tree.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self._home_dir = settings.get_default_home_dir()
        self._cwd = Path(".").abspath()
        self.model.setRootPath(self._home_dir)
        self.tree.setRootIndex(self.model.index(self._home_dir))

        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.tree)

        self._create_actions()
        self._create_connections()

    def _create_connections(self):
        self.tree.doubleClicked.connect(self._on_index_clicked)

    def _create_actions(self):
        self._action_go_to_parent = QtGui.QAction(qicon('oxygen_go-up.png'), 'Parent dir', self)
        self._action_go_to_parent.triggered.connect(self.go_to_parent)

    def toolbar_actions(self):
        return [
            self._action_go_to_parent
        ]

    def go_to(self, path):
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(path))

    def go_to_parent(self):
        path = Path(self.model.filePath(self.tree.rootIndex()))
        self.go_to(path.parent)

    def _on_index_clicked(self, index):
        filename = self.model.filePath(index)
        self.pathSelected.emit(Path(filename))

    def set_properties(self, properties):
        columns = properties.get('columns', [0])
        for icol in range(self.model.columnCount()):
            self.tree.setColumnHidden(icol, icol not in columns)

    def properties(self):
        columns = [i for i in range(self.model.columnCount()) if not self.tree.isColumnHidden(i)]
        return dict(columns=columns)


class FileBrowser(GenericFileBrowser):

    def __init__(self):
        super(FileBrowser, self).__init__()
        self.pathSelected.connect(self.open_path)

    def open_path(self, path):
        if path.isfile():
            self.open_file(path)
        elif path.isdir():
            self.go_to(path)
        else:
            pass

    def _get_paradigm_container(self):
        if plugin_instance_exists('oalab.applet', 'EditorManager'):
            return plugin_instance('oalab.applet', 'EditorManager')
    paradigm_container = property(fget=_get_paradigm_container)

    def open_file(self, path):
        # This applet use "call applet" approach
        paradigm_container = self.paradigm_container
        if paradigm_container:
            paradigm_container.open_data(DataFactory(path))

        # A second possible approach would be to ask lab to connect this applet to an applet with a slot accepting
        # a factory parameter. In this case, you do not need to create this method but you need to add a connection in
        # lab.


def main():
    app = QtGui.QApplication(sys.argv)

    wid = FileBrowser()
    wid.show()
    app.exec_()


if __name__ == "__main__":
    main()
