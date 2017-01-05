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

import pkg_resources
import openalea.core
import openalea.oalab

from Qt import QtWidgets, QtGui, QtCore

from openalea.core.path import path as Path
from openalea.core.path import tempdir

from openalea.core.formatting.html import html_section
from openalea.core.formatting.util import icon_path

from openalea.core.plugin import iter_groups

from openalea.core.plugin.formatting.html import html_header, html_footer, html_summary
from openalea.core.plugin.formatting.util import DEFAULT_ICON
from openalea.core.plugin.formatting.text import format_str, format_author
from openalea.core.service.plugin import plugins

from openalea.oalab.manager.explorer import ManagerExplorer
from openalea.oalab.manager.explorer import ManagerExplorer
from openalea.oalab.utils import qicon_path

QI = QtGui.QIcon

class Preview(QtWidgets.QTextEdit):

    """
    This widget displays meta-information about project.
    """

    def __init__(self, item, parent=None):
        super(Preview, self).__init__(parent)

        self._tmp = tempdir()
        self.setContentsMargins(0, 0, 0, 0)

        html = html_header
        html += html_summary(item, icon_path=qicon_path(item, self._tmp))
        html += html_footer

        self.setText(html)
        self.setReadOnly(True)

    def closeEvent(self, event):
        self._tmp.rmtree()
        return event.accept()


def filter_authors(item):
    author = item.criteria.get('authors', None)
    if author is None:
        return
    elif isinstance(author, dict):
        return author.get('name', None)
    else:
        return author


def filter_team(item):
    author = item.criteria.get('authors', None)
    if author is None:
        return
    elif isinstance(author, dict):
        return author.get('team', None)
    else:
        teams = set([])
        for a in author:
            for team in a.get('team', []):
                teams.add(team)
        return list(teams)


def format_label_author(author):
    return format_author(author, email=False)


def format_label_team(author):
    return author


class PluginExplorer(ManagerExplorer):

    criteria = [
        ('implement', 'Implementation'),
        ('authors', 'Authors'),
        ('team', 'Team'),
        ('tags', 'Tags'),
        ('plugin_ep', 'Entry Point'),
        ('plugin_modulename', 'Plugin Module'),
        ('plugin_dist', 'Python Distribution'),
    ]

    def __init__(self, parent=None):
        ManagerExplorer.__init__(self, parent)

        self._explorer.set_default_item_icon(DEFAULT_ICON)
        self.set_criteria(self.criteria)

        self._cb_group = QtWidgets.QComboBox()
        prefixes = ['openalea', 'oalab']
        for group in sorted(iter_groups()):
            match = False
            for prefix in prefixes:
                if group.startswith(prefix):
                    match = True
                    break
            if match:
                self._cb_group.addItem(group)
        self._cb_group.currentIndexChanged.connect(self._on_group_changed)
        self._layout.addWidget(self._cb_group, 0, 2)

        self._on_group_changed(0)

    def _on_group_changed(self, idx):
        group = self._cb_group.itemText(idx)
        self.set_items(plugins(group))

    def groupby(self, **kwds):
        filter_name = kwds.get("filter_name", None)
        if filter_name:
            if filter_name == 'authors':
                self.groupby(function=filter_authors, label=format_label_author)
            elif filter_name == 'team':
                self.groupby(function=filter_team, label=format_label_team)
            else:
                self.groupby(criteria=filter_name)
            self._filter_box.set_filter(filter_name)
        else:
            self._explorer.groupby(**kwds)

    def set_items(self, items):
        ## Add all criteria
        #criteria = set()
        #criteria.add(('implement', 'Implementation'))
        #for item in items:
        #    criteria = criteria.union([(k, k) for k in item.criteria])
        #self.set_criteria(list(criteria))
        ManagerExplorer.set_items(self, items)

    def _on_item_changed(self, item):
        if item:
            self._switcher.set_widget(Preview, item)
        self._current = item

def show_plugins(group="oalab.applet"):
    import sys

    app = QtWidgets.QApplication(sys.argv)

    plugin_selector = PluginExplorer()
    plugin_selector.show()

    app.exec_()

if __name__ == "__main__":
    show_plugins()
