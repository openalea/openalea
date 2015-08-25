
from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.project import Project
from openalea.core.project.manager import ProjectManager
from openalea.core.project.html import html_metainfo_summary, html_item_summary, pretty_print
from openalea.core.path import path as Path

QI = QtGui.QIcon
DEFAULT_PROJECT_ICON = ":/images/resources/axiom2.png"

import openalea.core
from openalea.deploy.shared_data import shared_data
stylesheet_path = shared_data(openalea.core, 'stylesheet.css')

html_header = '<html>\n  <head>\n    <link rel="stylesheet" type="text/css" href="%s">\n  </head>' % stylesheet_path
html_footer = '</html>'


def qicon_path(project):
    """
    If icon is pysically on disk, return path.
    Else, save image in project dir and return it
    """
    from openalea.oalab.utils import obj_icon
    ext = '.png'
    icon_path = project.path / "._icon" + ext
    obj_icon(project, save_filepath=icon_path, paths=[project.path], default=DEFAULT_PROJECT_ICON)
    return icon_path


def html_project_summary(project):
    args = dict(image=qicon_path(project), title=project.title, name=project.name)
    html = '<div class="summary"><p class="title"><img style="vertical-align:middle;" src="%(image)s" width="128" />' % args
    html += '%(title)s</p>' % args
    html += '\n<hr>'
    html += html_metainfo_summary(project)
    html += html_item_summary(project)
    html += '</div>'
    return html


class Preview(QtGui.QTextEdit):

    """
    This widget displays meta-information about project.
    """

    def __init__(self, project, parent=None):
        super(Preview, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        html = html_header
        html += '<div class="title">' + pretty_print(project.title) + "</div>"
        html += html_footer

        html = html_header
        html += html_project_summary(project)
        html += html_footer

        self.setText(html)
        self.setReadOnly(True)


def main():
    from openalea.core.project.manager import ProjectManager
    import sys

    app = QtGui.QApplication(sys.argv)

    tabwidget = QtGui.QTabWidget()

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
