# -*- python -*-
#
# OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
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
from openalea.vpltk.qt import QtGui, QtCore
from openalea.vpltk.qt.compat import getexistingdirectory


from openalea.core.path import path as Path
from openalea.core.settings import get_default_home_dir
from openalea.core.service.project import (projects, add_project_directory,
                                           write_project_settings)

from openalea.oalab.manager.explorer import ManagerExplorer
from openalea.oalab.project.preview import Preview, DEFAULT_PROJECT_ICON


class ProjectExplorer(ManagerExplorer):

    criteria = [
        ('path', 'Paths'),
        ('authors', 'Authors')
    ]

    def __init__(self, parent=None):
        ManagerExplorer.__init__(self, parent)
        self._explorer.search_item_request.connect(self.add_path_to_search_item)
        self._explorer.set_default_item_icon(DEFAULT_PROJECT_ICON)
        self.set_items(projects())
        self.set_criteria(self.criteria)

        self.groupby(filter_name="path")

    def groupby(self, **kwds):
        filter_name = kwds.get("filter_name", None)
        if filter_name == 'path':
            root = Path(get_default_home_dir())

            def parent_path(project):
                return str(root.relpathto(project.path.parent))

            self.groupby(function=parent_path)
        elif filter_name == 'authors':
            def label(criterion):
                if isinstance(criterion, list):
                    return ', '.join(criterion)
                else:
                    return str(criterion)
            self.groupby(criteria=filter_name, label=label)
        elif filter_name:
            self.groupby(criteria=filter_name)
        else:
            self._explorer.groupby(**kwds)

    def add_path_to_search_item(self):
        itemdir = getexistingdirectory(self, 'Select Directory Containing Projects')
        if itemdir:
            add_project_directory(itemdir)
            write_project_settings()
            self.set_items(projects())

    def _on_item_changed(self, item):
        if item:
            self._switcher.set_widget(Preview, item)
        self._current = item


def main():
    import sys

    app = QtGui.QApplication(sys.argv)
    selector = ProjectExplorer()
    selector.show()
    app.exec_()


if __name__ == "__main__":
    main()
