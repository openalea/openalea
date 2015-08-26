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

from openalea.vpltk.qt import QtGui, QtCore

from openalea.core.project.html import icon_path, html_section
from openalea.core.plugin import iter_groups
from openalea.core.service.plugin import plugins
from openalea.oalab.manager.explorer import ManagerExplorer


from openalea.core.path import path as Path

QI = QtGui.QIcon

import openalea.core
import openalea.oalab
from openalea.deploy.shared_data import shared_data
stylesheet_path = shared_data(openalea.core, 'stylesheet.css')

html_header = '<html>\n  <head>\n    <link rel="stylesheet" type="text/css" href="%s">\n  </head>' % stylesheet_path
html_footer = '</html>'

DEFAULT_ICON = "icons/Crystal_Clear_app_kservices.png"


def html_summary(item):
    if hasattr(item, 'icon'):
        p = icon_path(item.icon, default=DEFAULT_ICON, packages=[openalea.core, openalea.oalab])
        image = '<img style="vertical-align:middle;" src="%s" width="128" />' % p
    else:
        image = ''
    args = dict(image=image, title=item.label, name=item.name)
    html = '<div class="summary"><p class="title"> %(image)s' % args
    html += '%(title)s</p>' % args
    html += '\n<hr>'

    items = []
    for label, value in item.criteria.items():
        if label in ('icon', ) or not value:
            continue
        items.append(
            '<span class="key">%s</span>: <span class="value">%s</span>\n' %
            (label.capitalize(), value))
    html += html_section('criteria', 'Criteria', items)

    items = []
    for tag in item.tags:
        items.append('<span class="key">%s</span>\n' % label)
    html += html_section('tags', 'Tags', items)

    html += '</div>'
    return html


class Preview(QtGui.QTextEdit):

    """
    This widget displays meta-information about project.
    """

    def __init__(self, item, parent=None):
        super(Preview, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        html = html_header
        html += '<div class="title">' + item.label + "</div>"
        html += html_footer

        html = html_header
        html += html_summary(item)
        html += html_footer

        self.setText(html)
        self.setReadOnly(True)


class PluginExplorer(ManagerExplorer):

    criteria = [
        ('implement', 'Implementation'),
        ('entry_point', 'Entry Point'),
        ('modulename', 'Plugin Module'),
        ('dist', 'Python Distribution'),
    ]

    def __init__(self, parent=None):
        ManagerExplorer.__init__(self, parent)

        self._explorer.set_default_item_icon(DEFAULT_ICON)
        self.set_criteria(self.criteria)
        self.groupby(filer_name='implement')

        self._cb_group = QtGui.QComboBox()
        prefixes = ['openalea', 'oalab', 'vpltk']
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
            self.groupby(criteria=filter_name)
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

    app = QtGui.QApplication(sys.argv)

    plugin_selector = PluginExplorer()
    plugin_selector.show()

    app.exec_()

if __name__ == "__main__":
    show_plugins()
