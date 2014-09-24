from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.path import path
from openalea.oalab.gui import resources_rc
from openalea.oalab.project.preview import Preview, pretty_print
from openalea.core.project.manager import ProjectManager
import sys


class PrettyPreview(QtGui.QPushButton):
    """
    PushButton initialized from a project : gets its name, icon and version and displays it.
    """

    def __init__(self, project, size=200, parent=None):
        super(PrettyPreview, self).__init__(parent)
        wanted_size = size

        self.setMinimumSize(wanted_size, wanted_size)
        self.setMaximumSize(wanted_size, wanted_size)
        self.project = project

        layout = QtGui.QGridLayout(self)
        icon_path = project.icon_path
        icon_name = icon_path if icon_path else ":/images/resources/openalealogo.png"
        text = pretty_print(project.name)

        pixmap = QtGui.QPixmap(icon_name)
        label = QtGui.QLabel()
        label.setScaledContents(True)

        painter = QtGui.QPainter()
        painter.begin(pixmap)
        painter.setPen(QtCore.Qt.darkGreen)
        qsize = pixmap.size()
        ytext = 0.85 * qsize.height()
        painter.drawText(0, ytext, qsize.width(), 0.2 * qsize.height(), QtCore.Qt.AlignHCenter, text)
        painter.end()

        label.setPixmap(pixmap)

        layout.addWidget(label, 0, 0)


class ProjectSelector(QtGui.QWidget):
    def __init__(self, projects, open_project=None, parent=None):
        super(ProjectSelector, self).__init__(parent)
        self.projects = projects
        self.layout = QtGui.QGridLayout(self)
        self.open_project = open_project
        self.init()

    def init(self):
        button_size = 180
        self.current_preview = None

        # Auto select number of lines and columns to display
        # Here number of lines <= number of columns
        # <=4 -> 2x2 or 2x1, <=9 -> 3x3 or 3x2, <=16 -> 4x4 or 4x3, ...
        nb_proj = len(self.projects)
        # maxcolumn = int(sqrt(nb_proj))

        # Pb: we want the size of QScrollArea and not self
        actual_width = self.size().width()
        maxcolumn = int(actual_width / nb_proj)


        if maxcolumn > 5:
            maxcolumn = 5

        refresh_widget = QtGui.QPushButton("Refresh")
        refresh_widget.clicked.connect(self.refresh_project_list)
        add_widget = QtGui.QPushButton("Search Projects")
        add_widget.clicked.connect(self.add_path_to_search_project)

        i, j = 1, -1
        for project in self.projects:
            # Create widget
            preview_widget = PrettyPreview(project, size=button_size)
            preview_widget.clicked.connect(self.showDetails)

            if j < maxcolumn - 1:
                j += 1
            else:
                j = 0
                i += 1
            self.layout.addWidget(preview_widget, i, j)

        self.layout.addWidget(refresh_widget, 0, 0)
        self.layout.addWidget(add_widget, 0, 1)

    def showDetails(self):
        sender = self.sender()
        self.current_preview = Preview(project=sender.project, open_project=self.open_project)
        self.current_preview.show()

    def refresh_project_list(self):
        project_manager = ProjectManager()
        project_manager.discover()
        self.projects = project_manager.projects
        self.init()

    def add_path_to_search_project(self):
        fname = self.showOpenProjectDialog()
        if fname:
            pm = ProjectManager()
            pm.repositories.append(fname)
            pm.write_settings()
            self.refresh_project_list()

    def showOpenProjectDialog(self):
        fname = QtGui.QFileDialog.getExistingDirectory(self, 'Select Directory to search Projects', None)
        return fname


class ProjectSelectorScroll(QtGui.QScrollArea):
    def __init__(self, projects, open_project=None, parent=None):
        super(ProjectSelectorScroll, self).__init__(parent)
        widget = ProjectSelector(projects, open_project=open_project, parent=parent)
        self.setWidget(widget)


def main():
    app = QtGui.QApplication(sys.argv)

    project_manager = ProjectManager()
    project_manager.discover()
    scroll = ProjectSelectorScroll(project_manager.projects)

    # Display
    scroll.show()
    app.exec_()


if __name__ == "__main__":
    main()
