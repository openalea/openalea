from openalea.vpltk.qt import QtGui
from openalea.core.path import path


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


class Preview(QtGui.QWidget):
    """
    This widget displays meta-information about project.
    """
    def __init__(self, project, open_project=None, parent=None):
        super(Preview, self).__init__(parent)
        self.open_project = open_project
        wanted_size = 50
        self.project = project

        layout = QtGui.QGridLayout()
        icon_name = ":/images/resources/openalea_icon2.png"
        if len(project.icon):
            if project.icon[0] is not ":":
                #local icon
                icon_name = project.path / project.icon
                #else native icon from oalab.gui.resources

        image = QtGui.QImage(icon_name)
        label = QtGui.QLabel()
        label.setPixmap(QtGui.QPixmap(image))
        size = image.size()
        if size.height() > wanted_size or size.width() > wanted_size:
            # Auto-rescale if image is bigger than wanted_size x wanted_size
            label.setScaledContents(True)
        label.setMinimumSize(wanted_size, wanted_size)
        label.setMaximumSize(wanted_size, wanted_size)
        layout.addWidget(label, 0, 0)

        layout.addWidget(QtGui.QLabel("<b><FONT SIZE = 40>" + pretty_print(project.name) + "<\b>"), 0, 1)

        i = 1
        for label in ["author", "author_email", "description", "long_description", "version", "url", "citation", "license", "dependencies", "path"]:
            layout.addWidget(QtGui.QLabel(label), i, 0)
            # GBY Review:
            # QLabel expects a QString and QString is equivalent to unicode
            # so you must convert str to unicode to support non ASCII characters correctly (for example accent in author's name)
            # If project meta-info encoding is utf-8, you can write projet.author.decode('utf-8')
            # Just put accents or greek characters in test data to check such problems

            # GBY Review: if amount of metainfo grows, QTextEdit can be more convenient
            layout.addWidget(QtGui.QLabel(pretty_print(getattr(project, label))), i, 1)
            i += 1

        layout.addWidget(QtGui.QLabel("model:"), 12, 0)
        layout.addWidget(QtGui.QLabel(pretty_print(project.src.keys())), 12, 1)

        open_button = QtGui.QPushButton("Open this project")
        open_button.clicked.connect(self.on_project_opened)
        layout.addWidget(open_button, 13, 0, 13, 2)

        verticalSpacer = QtGui.QSpacerItem(0, 0);
        layout.addItem(verticalSpacer, 14, 0, 14, 1)
        horizontalSpacer = QtGui.QSpacerItem(0, 0)
        layout.addItem(horizontalSpacer, 0, 2, 14, 2)

        self.setLayout(layout)

    def on_project_opened(self):
        if self.open_project:
            self.open_project(self.project)
            self.hide()


def main():
    from openalea.vpltk.project.manager2 import ProjectManager
    import sys

    app = QtGui.QApplication(sys.argv)

    tabwidget = QtGui.QTabWidget()

    project_manager = ProjectManager()
    project_manager.discover()

    projects = project_manager.projects
    for project in projects:
        project.load_manifest()
        # Create widget
        preview_widget = Preview(project)
        tabwidget.addTab(preview_widget, project.name)

    # Display
    tabwidget.show()
    app.exec_()


if __name__ == "__main__":
    main()
