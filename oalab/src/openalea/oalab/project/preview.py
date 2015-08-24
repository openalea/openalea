
from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.project import Project
from openalea.core.project.manager import ProjectManager
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


def html_section(identifier, title, items):
    html = ''
    html += '<div class="section" id="%s">\n' % identifier
    html += '<div class="section-title">%s</div>' % title
    html += '  <ul>\n'
    for item in items:
        html += '    <li>%s</li>\n' % (item)
    html += '  </ul>\n'
    html += "</div>"
    return html


def pretty_print(obj):
    """
    :param obj: to decode. Can be a string/unicode or a list of string/unicod
    :return: object decoded into utf-8.
    """
    if isinstance(obj, list):
        text = ', '.join(obj).decode('utf-8')
    else:
        text = str(obj).decode('utf-8')
    return text


def html_item_summary(project):
    excluded_categories = ['cache', 'world']

    html = ''
    # Loop on all categories available in this project
    for category, desc in project.categories.items():
        if category in excluded_categories:
            continue
        title = desc['title']
        items = project.items(category)
        if not items:
            continue

        html_items = []
        for item_name in sorted(items):
            model = items[item_name]
            html_items.append(
                '<span class="item"><span class="item-namebase">%s</span><span class="item-ext">%s</span></span>\n' % (
                    model.filename.namebase, model.filename.ext))
        html += html_section(category, title, html_items)
    return html


def html_metainfo_summary(project):
    items = [
        '<span class="key">Name</span>: <span class="value">%s</span>\n' % (project.name),
        '<span class="key">Path</span>: <span class="value">%s</span>\n' % (project.path)
    ]
    for label in Project.DEFAULT_METADATA:
        if label in ('icon', 'alias'):
            continue
        value = pretty_print(getattr(project, label))
        if value:
            items.append(
                '<span class="key">%s</span>: <span class="value">%s</span>\n' %
                (label.capitalize(), value))
    return html_section('meta-information', 'Meta-information', items)


def html_project_summary(project):
    args = dict(image=qicon_path(project), title=project.title, name=project.name)
    html = '<p class="title"><img style="vertical-align:middle;" src="%(image)s" width="128" />' % args
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
