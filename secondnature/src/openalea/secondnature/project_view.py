
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


def muteItemChange(f):
    def muteWrapper(self, *args, **kwargs):
        self.itemChanged.disconnect(self._ProjectManagerTreeModel__on_item_changed)
        f(self, *args, **kwargs)
        self.itemChanged.connect(self._ProjectManagerTreeModel__on_item_changed)
    return muteWrapper



class ProjectManagerTreeModel(QtGui.QStandardItemModel):

    projectRole  = QtCore.Qt.UserRole + 1
    documentRole = QtCore.Qt.UserRole + 2

    def __init__(self, parent=None):
        QtGui.QStandardItemModel.__init__(self, parent)
        self.__projMan = ProjectManager()

        self.__docItemMap     = {}
        self.__activeProjItem = None

        self.itemChanged.connect(self.__on_item_changed)
        self.__projMan.activeProjectChanged.connect(self.set_active_project)
        #self.__projMan.activeProjectClosed.connect()

        self.__activePrj = None

        activePrj = self.__projMan.get_active_project()
        if activePrj:
            self.set_active_project(activePrj)

    def set_active_project(self, proj):
        # -- first disconnect previously connected slots --
        if self.__activePrj:
            self.__activePrj.document_added.disconnect(self.__on_document_added)
            self.__activePrj.document_name_changed.disconnect(self.set_active_project)
            self.__activePrj.project_name_changed.disconnect(self.__on_active_project_name_changed)
            self.__activePrj.modified.disconnect(self.__on_active_project_modified)
            self.__activePrj.saved.disconnect(self.__on_active_project_saved)
        # -- then clear the view (maybe be less radical) --
        self.clear()
        # -- now set active project and reconnect slots to this one --
        if proj:
            self.__activePrj = proj
            self.__activeProjItem = QtGui.QStandardItem(proj.name)
            self.__activeProjItem.setData(QtCore.QVariant(proj), self.projectRole)
            self.appendRow(self.__activeProjItem)
            self.__activePrj.document_added.connect(self.__on_document_added)
            self.__activePrj.document_name_changed.connect(self.__on_document_name_changed)
            self.__activePrj.project_name_changed.connect(self.__on_active_project_name_changed)
            self.__activePrj.modified.connect(self.__on_active_project_modified)
            self.__activePrj.saved.connect(self.__on_active_project_saved)

    ###################
    # Protected slots #
    ###################
    def __on_item_changed(self, item):
        proj = item.data(self.projectRole).toPyObject()
        print "__on_item_changed::proj", proj
        if proj:
            proj.name = str(item.text())
        else:
            doc = item.data(self.documentRole).toPyObject()
            proj = item.parent().data(self.projectRole).toPyObject()
            if proj and doc:
                proj.set_document_name(doc, str(item.text()))

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
    def __on_document_name_changed(self, proj, doc, fixed):
        docItem = self.__docItemMap.get(doc)
        if docItem:
            docItem.setText(fixed)

    def __on_document_added(self, proj, doc):
        newItem  = QtGui.QStandardItem(doc.name)
        newItem.setData(QtCore.QVariant(doc), self.documentRole)
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
        encoded = QtCore.QByteArray()

        item = self.itemFromIndex(modelIndexes[0])
        if item:
            doc = item.data(self.documentRole).toPyObject()
            if doc and self.__activePrj:
                docId = self.__activePrj.get_document_id(doc)
                encoded = QtCore.QByteArray.number(docId)
        data.setData(ProjectManager.mimeformat, encoded)
        return data
