# -*- python -*-
#
# OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013-2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#                       Julien Coste <julien.coste@inria.fr>
#
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

from itertools import groupby

from openalea.vpltk.qt import QtGui, QtCore
from openalea.vpltk.qt.compat import getexistingdirectory

from openalea.core.service.project import (projects, add_project_directory,
                                           write_project_settings)

from openalea.oalab.utils import obj_icon
from openalea.oalab.widget.switcher import WidgetSwitcher
from openalea.oalab.widget import resources_rc
from openalea.oalab.project.preview import Preview
from openalea.core.path import path as Path
from openalea.core.settings import get_default_home_dir


class ProjectExplorerModel(QtGui.QStandardItemModel):

    def __init__(self):
        QtGui.QStandardItemModel.__init__(self)
        self._headers = [u'Project']
        self.setHorizontalHeaderLabels(self._headers)
        self._group = {}

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._headers[col]
        return None

    def set_projects(self, projects):
        self._projects = projects
        self.refresh()

    def projects(self):
        return self._projects

    def refresh(self):
        default_icon = ':/images/resources/openalea_icon2.png'

        self.clear()
        self._group = {}
        projects = self._projects
        if projects is None:
            return

        _projects = []
        for project in projects:
            p = project.path.parent
            _projects.append((p, project))
        _projects.sort()

        parent_item = self.invisibleRootItem()
        root = Path(get_default_home_dir())
        for path, projects in groupby(_projects, lambda item: item[0]):
            name = str(root.relpathto(path))
            repository_item = QtGui.QStandardItem(name)
            #item.project = project
            #item.setIcon(obj_icon(project, default=default_icon, paths=[project.path]))
            parent_item.appendRow(repository_item)
            self._group[repository_item] = []

            for _, project in projects:
                item = QtGui.QStandardItem(project.name)
                item.project = project
                item.setIcon(obj_icon(project, default=default_icon, paths=[project.path]))
                repository_item.appendRow(item)
                self._group[repository_item].append(item)

    def project(self, idx):
        try:
            return self.itemFromIndex(idx).project
        except AttributeError:
            return self._group[self.itemFromIndex(idx)][0].project


class ProjectExplorerView(QtGui.QTreeView):
    project_changed = QtCore.Signal(object)

    def __init__(self, parent=None):
        QtGui.QTreeView.__init__(self, parent=parent)
        self._model = ProjectExplorerModel()
        self.setModel(self._model)

        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

    def set_projects(self, projects):
        self._model.set_projects(projects)
        self.expandAll()
        if len(projects):
            first = self._model._group.values()[0][0]
            self.setCurrentIndex(self._model.indexFromItem(first))

    def selectionChanged(self, selected, deselected):
        for idx in selected.indexes():
            self.project_changed.emit(self._model.project(idx))
        return QtGui.QTreeView.selectionChanged(self, selected, deselected)


class ProjectSelector(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)

        self._current = None

        self._layout = QtGui.QGridLayout(self)

        p = QtGui.QSizePolicy

        self._explorer = ProjectExplorerView()
        self._explorer.project_changed.connect(self._on_project_changed)
        self._explorer.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))

        self._switcher = WidgetSwitcher(parent=self)
        self._switcher.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))

        self._pb_search = QtGui.QPushButton("Search Projects")
        self._pb_search.clicked.connect(self.add_path_to_search_project)

        self._layout.addWidget(self._explorer, 0, 0)
        self._layout.addWidget(self._switcher, 0, 1)
        self._layout.addWidget(self._pb_search, 1, 0)

        self.set_projects(projects())

    def set_projects(self, projects):
        self._explorer.set_projects(projects)

    def project(self):
        return self._current

    def _on_project_changed(self, project):
        if project:
            self._switcher.set_widget(Preview, project)
        self._current = project

    def add_path_to_search_project(self):
        projectdir = getexistingdirectory(self, 'Select Directory to search Projects')
        if projectdir:
            add_project_directory(projectdir)
            write_project_settings()
            self.set_projects(projects())


def main():
    from openalea.core.service.project import projects
    import sys

    app = QtGui.QApplication(sys.argv)
    selector = ProjectSelector()
    selector.show()
    app.exec_()


if __name__ == "__main__":
    main()
