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

from itertools import groupby

from openalea.vpltk.qt import QtGui, QtCore
from openalea.vpltk.qt.compat import getexistingdirectory

from openalea.oalab.utils import obj_icon, qicon
from openalea.oalab.widget.switcher import WidgetSwitcher
from openalea.oalab.widget import resources_rc

from openalea.core.path import path as Path
from openalea.core.settings import get_default_home_dir


class ManagerExplorerModel(QtGui.QStandardItemModel):

    def __init__(self):
        QtGui.QStandardItemModel.__init__(self)

        self._headers = [u'Manager']
        self.setHorizontalHeaderLabels(self._headers)
        self._items = None
        self._group = {}
        self._groupby = {}
        self.default_item_icon = "icons/Crystal_Clear_app_kservices.png"
        self.default_group_icon = "icons/Crystal_Clear_filesystem_folder_grey_open.png"
        self.undefined_group_label = "Default / Undefined"

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._headers[col]
        return None

    def set_items(self, items):
        self._items = items
        self.refresh()

    def items(self):
        return self._items

    def groupby(self, **kwds):
        self._groupby = kwds
        self.refresh()

    def refresh(self):

        self.clear()
        self._group = {}
        items = self._items
        if items is None:
            return

        # Manage groupby info
        gby_func = self._groupby.get('function', None)
        gby_criteria = self._groupby.get('criteria', None)
        gby_label = self._groupby.get('label', None)

        if gby_func:
            f_gby_key = gby_func
        elif gby_criteria:
            def f_gby_key(item):
                if hasattr(item, gby_criteria):
                    return getattr(item, gby_criteria)
                else:
                    return self.undefined_group_label
        else:
            f_gby_key = lambda item: self.undefined_group_label

        if gby_label:
            f_gby_label = gby_label
        else:
            f_gby_label = lambda criterion: str(criterion)

        _items = []
        for item in items:
            key = f_gby_key(item)
            if not key:
                key = self.undefined_group_label
            _items.append((key, item))
        _items.sort()

        parent_item = self.invisibleRootItem()

        groups = groupby(_items, lambda item: item[0])

        for key, items in groups:
            try:
                label = f_gby_label(key)
            except:
                label = str(key)
            repository_item = QtGui.QStandardItem(label)
            repository_item.setIcon(qicon(self.default_group_icon))
            parent_item.appendRow(repository_item)
            self._group[repository_item] = []

            for _, item in sorted(items, key=lambda args: args[1].label):
                qitem = QtGui.QStandardItem(item.label)
                qitem.item = item
                if hasattr(item, 'path'):
                    paths = [item.path, item.path.parent]
                else:
                    paths = []
                qitem.setIcon(obj_icon(item, default=self.default_item_icon, paths=paths))
                repository_item.appendRow(qitem)
                self._group[repository_item].append(qitem)

        self.more_item = QtGui.QStandardItem("Add more items")
        self.more_item.setIcon(qicon("icons/Crystal_Clear_action_edit_add.png"))
        parent_item.appendRow(self.more_item)

    def search_item_selected(self, idx):
        item = self.itemFromIndex(idx)
        return item is self.more_item

    def item(self, idx):
        try:
            return self.itemFromIndex(idx).item
        except AttributeError:
            return self._group[self.itemFromIndex(idx)][0].item


class ManagerExplorerView(QtGui.QTreeView):
    item_changed = QtCore.Signal(object)
    search_item_request = QtCore.Signal()

    def __init__(self, parent=None):
        QtGui.QTreeView.__init__(self, parent=parent)
        self.setContentsMargins(0, 0, 0, 0)
        self._model = ManagerExplorerModel()
        self.setModel(self._model)

        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setIconSize(QtCore.QSize(24, 24))

        self.setHeaderHidden(True)

    def set_items(self, items):
        self._model.set_items(items)
        if len(items):
            first = self._model._group.values()[0][0]
            self.setCurrentIndex(self._model.indexFromItem(first))
        self.expandAll()

    def selectionChanged(self, selected, deselected):
        for idx in selected.indexes():
            if self._model.search_item_selected(idx):
                self.search_item_request.emit()
            else:
                self.item_changed.emit(self._model.item(idx))
        return QtGui.QTreeView.selectionChanged(self, selected, deselected)

    def groupby(self, **kwds):
        self._model.groupby(**kwds)
        self.expandAll()

    def set_default_group_icon(self, icon_path):
        self._model.default_group_icon = icon_path

    def set_default_item_icon(self, icon_path):
        self._model.default_item_icon = icon_path


class FilterBox(QtGui.QWidget):
    filter_changed = QtCore.Signal(str)

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self._layout = QtGui.QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._cb_groupby = QtGui.QComboBox()
        self._cb_groupby.currentIndexChanged.connect(self._on_current_index_changed)

        self._layout.addWidget(self._cb_groupby)

    def _on_current_index_changed(self, idx):
        self.filter_changed.emit(self._criteria[idx][0])

    def set_criteria(self, criteria):
        self._criteria = criteria
        for criterion in self._criteria:
            self._cb_groupby.addItem(criterion[1])


class ManagerExplorer(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)

        self._current = None

        self._layout = QtGui.QGridLayout(self)

        p = QtGui.QSizePolicy

        self._explorer = ManagerExplorerView()
        self._explorer.item_changed.connect(self._on_item_changed)
        self._explorer.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))

        self._filter_box = FilterBox()
        self._filter_box.filter_changed.connect(self._on_filter_changed)

        self._switcher = WidgetSwitcher(parent=self)
        self._switcher.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))

        self._layout.addWidget(QtGui.QLabel("Group by ..."), 0, 0)
        self._layout.addWidget(self._filter_box, 0, 1)
        self._layout.addWidget(self._explorer, 1, 0, 1, 2)
        self._layout.addWidget(self._switcher, 1, 2)

        self.resize(800, 600)

    def _on_filter_changed(self, text):
        self.groupby(filter_name=text)

    def set_items(self, items):
        self._explorer.set_items(items)

    def set_criteria(self, criteria):
        self._filter_box.set_criteria(criteria)

    def item(self):
        return self._current

    def groupby(self, **kwds):
        self._explorer.groupby(**kwds)

    def _on_item_changed(self, item):
        pass
