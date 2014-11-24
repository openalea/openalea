# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2010 INRIA - CIRAD - INRA
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
"""
The logger view widget.
"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.vpltk.qt import qt

class LoggerView(qt.QtGui.QTableView):
    """A QTableView that has more compact lines
    and customized header actions to manipulate logs"""

    def __init__(self, parent, model, *args, **kwargs):
        qt.QtGui.QTableView.__init__(self, *args, **kwargs)
        rowHeight = self.fontMetrics().height() + 2;
        self.verticalHeader().setDefaultSectionSize(rowHeight);
        self.verticalHeader().setStyleSheet(
            "QHeaderView::section {" + \
            "padding-bottom: 0px;" + \
            "padding-top: 0px;" + \
            "padding-left: 0px;" + \
            "padding-right: 1px;" + \
            "margin: 1px;" + \
            "}")

        self.__proxyModel = qt.QtGui.QSortFilterProxyModel(self)
        self.__proxyModel.setSourceModel(model)
        self.__proxyModel.setDynamicSortFilter(True)

        self.verticalHeader().hide()
        self.setAlternatingRowColors(True)
        self.setModel(self.__proxyModel)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.horizontalHeader().sectionPressed.connect(self.on_section_pressed)


    def on_section_pressed(self, section):
        if section == 0:
            menu = qt.QtGui.QMenu(self)
            filterMenu = menu.addMenu("Filter...")
            #sortMenu   = menu.addMenu("Sort...")

            # --filtering--
            showAll = filterMenu.addAction("Show All")
            showDebug = filterMenu.addAction("Show Debug")
            showInfo = filterMenu.addAction("Show Info")
            showWarning = filterMenu.addAction("Show Warning")
            showError = filterMenu.addAction("Show Error")
            showCritical = filterMenu.addAction("Show Critical")

            showAll.triggered.connect(self.show_all)
            showDebug.triggered.connect(self.show_debug)
            showInfo.triggered.connect(self.show_info)
            showWarning.triggered.connect(self.show_warning)
            showError.triggered.connect(self.show_error)
            showCritical.triggered.connect(self.show_critical)

            menu.popup(menu.mapFromGlobal(qt.QtGui.QCursor.pos()))

    def show_all(self):
        self.__proxyModel.setFilterWildcard("*")
        self.__proxyModel.setFilterKeyColumn(0)

    def show_debug(self):
        self.__proxyModel.setFilterFixedString("DEBUG")
        self.__proxyModel.setFilterKeyColumn(0)

    def show_info(self):
        self.__proxyModel.setFilterFixedString("INFO")
        self.__proxyModel.setFilterKeyColumn(0)

    def show_warning(self):
        self.__proxyModel.setFilterFixedString("WARNING")
        self.__proxyModel.setFilterKeyColumn(0)

    def show_error(self):
        self.__proxyModel.setFilterFixedString("ERROR")
        self.__proxyModel.setFilterKeyColumn(0)

    def show_critical(self):
        self.__proxyModel.setFilterFixedString("CRITICAL")
        self.__proxyModel.setFilterKeyColumn(0)
