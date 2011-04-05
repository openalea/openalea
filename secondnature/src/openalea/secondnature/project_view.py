
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
from openalea.secondnature.project import ProjectManager
from openalea.secondnature.qtutils import try_to_disconnect
from openalea.secondnature.api     import get_datafactory_menu


def muteItemChange(f):
    def muteWrapper(self, *args, **kwargs):
        self.itemChanged.disconnect(self._ProjectManagerTreeModel__on_item_changed)
        f(self, *args, **kwargs)
        self.itemChanged.connect(self._ProjectManagerTreeModel__on_item_changed)
    return muteWrapper



class ProjectManagerTreeModel(QtGui.QStandardItemModel):

    projectRole  = QtCore.Qt.UserRole + 1
    dataRole = QtCore.Qt.UserRole + 2

    def __init__(self, parent=None):
        QtGui.QStandardItemModel.__init__(self, parent)
        self.__projMan = ProjectManager()

        self.__docItemMap     = {}
        self.__activeProjItem = None

        self.itemChanged.connect(self.__on_item_changed)
        self.__projMan.active_project_changed.connect(self.set_active_project)

        self.__activeProj = None

        activePrj = self.__projMan.get_active_project()
        if activePrj:
            self.set_active_project(activePrj)


    def set_active_project(self, proj, old=None):
        # -- clear the view (maybe be less radical) --
        self.__clear(old)
        # -- now set active project and reconnect slots to this one --
        if proj:
            self.__activeProj = proj
            self.__activeProjItem = QtGui.QStandardItem(proj.name)
            self.__activeProjItem.setData(QtCore.QVariant(proj), self.projectRole)
            self.appendRow(self.__activeProjItem)
            self.connect_project(proj)
            for k, v in proj:
                self.__on_data_added(proj, v)


    #####################
    # utility functions #
    #####################
    def connect_project(self, proj):
        if proj:
            proj.data_added.connect(self.__on_data_added)
            proj.data_name_changed.connect(self.__on_data_name_changed)
            proj.project_name_changed.connect(self.__on_active_project_name_changed)
            proj.modified.connect(self.__on_active_project_modified)
            proj.saved.connect(self.__on_active_project_saved)
            proj.closed.connect(self.__on_active_project_saved)

    def disconnect_project(self, proj):
        if proj:
            try_to_disconnect(proj.data_added, self.__on_data_added)
            try_to_disconnect(proj.data_name_changed, self.__on_data_name_changed)
            try_to_disconnect(proj.project_name_changed, self.__on_active_project_name_changed)
            try_to_disconnect(proj.modified, self.__on_active_project_modified)
            try_to_disconnect(proj.saved, self.__on_active_project_saved)

    ###################
    # Protected slots #
    ###################
    def __clear(self, proj):
        self.clear()
        # -- disconnect previously connected slots --
        if proj:
            self.disconnect_project(proj)

    def __on_item_changed(self, item):
        proj = item.data(self.projectRole).toPyObject()
        doc  = item.data(self.dataRole).toPyObject()
        if proj:
            proj.name = str(item.text())
        else:
            doc = item.data(self.dataRole).toPyObject()
            proj = item.parent().data(self.projectRole).toPyObject()
            if proj and doc:
                proj.set_data_name(doc, str(item.text()))

    @muteItemChange
    def __on_active_project_modified(self, proj):
        if self.__activeProjItem is None:
            self.set_active_project(proj)
        self.__activeProjItem.setText(proj.name+" *")

    @muteItemChange
    def __on_active_project_name_changed(self, proj, name):
        if self.__activeProjItem is None:
            self.set_active_project(proj)
        self.__activeProjItem.setText(name+" *")

    @muteItemChange
    def __on_active_project_saved(self, proj):
        if self.__activeProjItem is None:
            self.set_active_project(proj)
        self.__activeProjItem.setText(proj.name)

    @muteItemChange
    def __on_data_name_changed(self, proj, doc, fixed):
        docItem = self.__docItemMap.get(doc)
        if docItem:
            docItem.setText(fixed)

    def __on_data_added(self, proj, doc):
        newItem  = QtGui.QStandardItem(doc.name)
        newItem.setData(QtCore.QVariant(doc), self.dataRole)
        icon = doc.icon
        newItem.setIcon(icon)
        newItem.setDragEnabled(True)
        parItem = self.__activeProjItem
        parItem.appendRow(newItem)
        self.__docItemMap[doc] = newItem

    ################################
    # QStandardItemModel extension #
    ################################
    def mimeTypes(self):
        return QtGui.QStandardItemModel.mimeTypes(self) + [ProjectManager.mimeformat]

    def mimeData(self, modelIndexes):
        if len(modelIndexes) != 1:
            return None

        data    = QtGui.QStandardItemModel.mimeData(self, modelIndexes)
        item = self.itemFromIndex(modelIndexes[0])

        encoded = QtCore.QByteArray()
        if item:
            doc = item.data(self.dataRole).toPyObject()
            if doc and self.__activeProj:
                docId = self.__activeProj.get_data_id(doc)
                encoded = QtCore.QByteArray.number(docId)
        data.setData(ProjectManager.mimeformat, encoded)
        return data

    def headerData(self, section, orientation, role):
        return QtCore.QVariant()



class ProjectView(QtGui.QTreeView):
    def __init__(self, model, parent=None):
        QtGui.QTreeView.__init__(self, parent)

        self.setModel(model)
        self.expandAll()
        self.setHeaderHidden(True)
        self.setDragEnabled(True)
        self.setIconSize(QtCore.QSize(16,16))
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenuRequest)

    def onContextMenuRequest(pos):
        menu = get_datafactory_menu()
        menu.popup(self.viewport().mapToGlobal(pos))


