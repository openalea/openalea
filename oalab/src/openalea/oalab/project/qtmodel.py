# -*- python -*-
#
# OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013-2015 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#                       Guillaume Baty <guillaume.baty@inria.fr>
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

from openalea.oalab.service.drag_and_drop import add_drag_format, encode_to_qmimedata
from openalea.vpltk.qt import QtGui
from openalea.oalab.utils import obj_icon


class ProjectModel(QtGui.QStandardItemModel):

    def __init__(self):
        QtGui.QStandardItemModel.__init__(self)
        self._data = {}
        self._root_item = None
        self._project = None

        add_drag_format(self, 'openalealab/data')
        add_drag_format(self, 'openalealab/model')

    def set_project(self, project):
        self._project = project
        self.refresh()

    def project(self):
        return self._project

    def refresh(self):
        self.clear()
        project = self._project
        if project is None:
            return

        icons = dict(
            project=QtGui.QIcon(":/images/resources/openalea_icon2.png"),
            src=QtGui.QIcon(":/images/resources/filenew.png"),
            control=QtGui.QIcon(":/images/resources/node.png"),
            world=QtGui.QIcon(":/images/resources/plant.png"),
            startup=QtGui.QIcon(":/images/resources/editredo.png"),
            data=QtGui.QIcon(":/images/resources/fileopen.png"),
            doc=QtGui.QIcon(":/images/resources/book.png"),
            cache=QtGui.QIcon(":/images/resources/editcopy.png"),
            model=QtGui.QIcon(":/images/resources/new.png"),
            lib=QtGui.QIcon(":/images/resources/codefile-red.png"),
        )

        name = project.name
        parentItem = self.invisibleRootItem()
        item = QtGui.QStandardItem(name)
        self._root_item = name

        item.setIcon(obj_icon(project, default=icons['project'], paths=[project.path]))
        parentItem.appendRow(item)

        for category in project.categories:
            item2 = QtGui.QStandardItem(category)
            item.appendRow(item2)

            if category in icons:
                item2.setIcon(icons[category])

            if not hasattr(project, category):
                continue

            data_dict = getattr(project, category)

            names = data_dict.keys()
            for name in sorted(names):
                data = data_dict[name]
                item3 = QtGui.QStandardItem(name)
                if hasattr(data, 'icon'):
                    data_icon_path = data.icon
                else:
                    data_icon_path = ''
                item3.setIcon(QtGui.QIcon(data_icon_path))
                item3.setData((category, data))
                item2.appendRow(item3)

    def projectdata(self, index):
        if index is None:
            return None
        if self._project is None:
            return

        if index.parent().data() in self._project.categories:
            category = index.parent().data()
            name = index.data()
            return category, name
        elif index.data() in self._project.categories:
            return ('category', index.data())
        elif index.data() == self._root_item:
            return ('project', index.data())
        else:
            return None

    def mimeData(self, indices):
        for index in indices:
            pass

        category, name = self.projectdata(index)
        if category in ('model', 'data'):
            data = self._project.get_item(category, name)
            return encode_to_qmimedata(data, 'openalealab/%s' % category)
        else:
            return QtGui.QStandardItemModel.mimeData(self, indices)
