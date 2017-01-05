# Version: $Id$
#
#

# Commentary:
#
#

# Change Log:
#
#

# Code:

from Qt import QtWidgets, QtGui, QtCore

from openalea.core.project import Project
from openalea.core.project.manager import ProjectManager
from openalea.core.project.formatting.html import html_metainfo_summary, html_item_summary
from openalea.core.formatting.util import pretty_print
from openalea.core.path import path as Path

QI = QtGui.QIcon

DEFAULT_PROJECT_ICON = ":/images/resources/axiom2.png"

import openalea.core
from openalea.deploy.shared_data import shared_data

from openalea.oalab.utils import qicon_path

stylesheet_path = shared_data(openalea.core, 'stylesheet.css')

html_header = '<html>\n  <head>\n    <link rel="stylesheet" type="text/css" href="%s">\n  </head>' % stylesheet_path
html_footer = '</html>'


def html_project_summary(project):
    args = dict(
        image=qicon_path(project, project.path, paths=[project.path], packages=[openalea.core, openalea.oalab],
                         default=DEFAULT_PROJECT_ICON),
        label=project.label,
        name=project.name)
    html = '<div class="summary"><p class="title"><img style="vertical-align:middle;" src="%(image)s" width="128" />' % args
    html += '%(label)s</p>' % args
    html += '\n<hr>'
    html += html_metainfo_summary(project)
    html += html_item_summary(project)
    html += '</div>'
    return html


class Preview(QtWidgets.QTextEdit):

    """
    This widget displays meta-information about project.
    """

    def __init__(self, project, parent=None):
        super(Preview, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        html = html_header
        html += '<div class="label">' + pretty_print(project.label) + "</div>"
        html += html_footer

        html = html_header
        html += html_project_summary(project)
        html += html_footer

        self.setText(html)
        self.setReadOnly(True)


def main():
    from openalea.core.project.manager import ProjectManager
    import sys

    app = QtWidgets.QApplication(sys.argv)

    tabwidget = QtWidgets.QTabWidget()

    project_manager = ProjectManager()
    project_manager.discover()

    projects = project_manager.projects
    for project in projects:
        # Create widget
        preview_widget = Preview(project)
        tabwidget.addTab(preview_widget, project.name)

    # Display
    tabwidget.show()
    app.exec_()


if __name__ == "__main__":
    main()

#
# preview.py ends here
