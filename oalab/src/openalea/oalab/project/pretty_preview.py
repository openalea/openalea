from openalea.vpltk.qt import QtGui, QtCore
from openalea.vpltk.project.project import ConfigObj
from openalea.core.path import path
from openalea.oalab.gui import resources_rc
from openalea.oalab.project.preview import Preview, pretty_print
from math import sqrt


class PrettyPreview(QtGui.QPushButton):
    """
    PushButton initialized from a project : gets its name, icon and version and displays it.
    """

    def __init__(self, project, size=200, parent=None):
        super(PrettyPreview, self).__init__(parent)
        wanted_size = size
        qsize = QtCore.QSize(wanted_size, wanted_size)

        self.setMinimumSize(wanted_size, wanted_size)
        self.setMaximumSize(wanted_size, wanted_size)
        self.project = project

        layout = QtGui.QGridLayout(self)
        icon_name = ":/images/resources/openalealogo.png"
        if project.icon:
            if not project.icon.startswith(':'):
                #local icon
                icon_name = path(project.path) / project.name / project.icon
                #else native icon from oalab.gui.resources

        text = pretty_print(project.name)

        pixmap = QtGui.QPixmap(icon_name)
        label = QtGui.QLabel()
        label.setScaledContents(True)

        painter = QtGui.QPainter()
        painter.begin(pixmap)
        painter.setPen(QtCore.Qt.darkRed)
        qsize = pixmap.size()
        ytext = 0.85*qsize.height()
        painter.drawText(0, ytext, qsize.width(), 0.2*qsize.height(), QtCore.Qt.AlignHCenter, text)
        painter.end()

        label.setPixmap(pixmap)

        layout.addWidget(label, 0, 0)

        """
        pixmap_icon = QtGui.QPixmap(icon_name)
        size = pixmap_icon.size()
        label = QtGui.QLabel()

#        if (size.height() > wanted_size) or (size.width() > wanted_size):
        #     # Auto-rescale if image is bigger than (wanted_size x wanted_size)
        pixmap_icon = pixmap_icon.scaled(qsize, QtCore.Qt.KeepAspectRatio)
        # #     label.setScaledContents(True)

        pixmap = QtGui.QPixmap(qsize)
        ytext = 0.8*qsize.height()

        painter = QtGui.QPainter()
        painter.begin(pixmap)
        # painter.fillRect(0, 0, qsize.width(), qsize.height(), QtCore.Qt.white)
        painter.drawPixmap(0, 0, wanted_size, wanted_size, pixmap_icon)
#        painter.setPen()
#         painter.fillRect(0, ytext, qsize.width(), 0.2*qsize.height(), QtCore.Qt.white)
        painter.setPen(QtCore.Qt.white)
        painter.drawText(0, ytext, qsize.width(), 0.2*qsize.height(), QtCore.Qt.AlignLeft, text)
        painter.end()

        label.setPixmap(pixmap)"""


class ProjectSelector(QtGui.QWidget):
    def __init__(self, projects, parent=None):
        super(ProjectSelector, self).__init__(parent)
        layout = QtGui.QGridLayout(self)

        self.current_preview = None

        # Auto select number of lines and columns to display
        # Here number of lines <= number of columns
        # <=4 -> 2x2 or 2x1, <=9 -> 3x3 or 3x2, <=16 -> 4x4 or 4x3, ...
        maxcolumn = int(sqrt(len(projects))) + 1


        i, j = 0, -1
        for project in projects:
            project.load_manifest()
            # Create widget
            preview_widget = PrettyPreview(project, size=180)
            preview_widget.clicked.connect(self.showDetails)

            if j < maxcolumn - 1:
                j += 1
            else:
                j = 0
                i += 1
            layout.addWidget(preview_widget, i, j)

    def showDetails(self):
        sender = self.sender()
        self.current_preview = Preview(project=sender.project)
        self.current_preview.show()

        #preview_widget = Preview(project=sender.project)

        ## remove old widget
        #item = layout.itemAtPosition(maxcolumn,0)
        #if item:
        #wid = item.widget()
        #layout.removeWidget(wid)
        #wid.setParent(None)

        #layout.addWidget(preview_widget, maxcolumn, 0, maxcolumn, maxcolumn)

def main():
    from openalea.vpltk.project.manager import ProjectManager
    import sys

    app = QtGui.QApplication(sys.argv)

    project_manager = ProjectManager()
    project_manager.discover()
    widget = ProjectSelector(project_manager.projects)

    # Display
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main()
