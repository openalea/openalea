

from openalea.core.project import Project
from openalea.core.service.plugin import plugins
from openalea.core.service.project import write_project_settings
from openalea.oalab.project.creator import CreateProjectWidget
from openalea.oalab.utils import ModalDialog
from openalea.vpltk.qt import QtGui, QtCore


def rename_model(project, category, name):
    filelist = getattr(project, category).keys()
    renamer = RenameModel(filelist, name)
    dialog = ModalDialog(renamer)
    if dialog.exec_():
        old_name = renamer.old_name()
        new_name = renamer.new_name()
        project.rename_item(category, old_name, new_name)


def edit_metadata(project):
    if project:
        project_creator = CreateProjectWidget(project)
        dialog = ModalDialog(project_creator)
        if dialog.exec_():
            _proj = project_creator.project()
            if _proj.name != project.name or _proj.projectdir != project.projectdir:
                project.move(_proj.path)
            project.metadata = project_creator.metadata()
            project.save()


def new_project():
    project_creator = CreateProjectWidget()
    dialog = ModalDialog(project_creator)
    if dialog.exec_():
        project = project_creator.project()
        project.save()
        write_project_settings()
        return project


class SelectCategory(QtGui.QWidget):

    def __init__(self, filename="", categories=None, dtypes=None, parent=None):
        super(SelectCategory, self).__init__(parent=parent)

        if categories is None:
            categories = Project.DEFAULT_CATEGORIES.keys()
        if dtypes is None:
            dtypes = [
                plugin.default_name for plugin in plugins(
                    'oalab.plugin',
                    criteria=dict(
                        implement='IParadigmApplet'))]
            dtypes.append('Other')
        self.categories = categories

        layout = QtGui.QFormLayout(self)

        self.label = QtGui.QLabel("Select in which category you want to add this file: ")
        self.l_dtypes = QtGui.QLabel("Data type")
        self.label2 = QtGui.QLabel("New filename: ")

        self.combo = QtGui.QComboBox(self)
        self.combo.addItems(categories)
        if 'model' in categories:
            self.combo.setCurrentIndex(categories.index('model'))

        self.combo_dtypes = QtGui.QComboBox(self)
        self.combo_dtypes.addItems(dtypes)
        self.combo_dtypes.setCurrentIndex(0)

        self.line = QtGui.QLineEdit(filename)

        layout.addRow(self.label, self.combo)
        layout.addRow(self.l_dtypes, self.combo_dtypes)
        layout.addRow(self.label2, self.line)

        self.setLayout(layout)

    def category(self):
        return str(self.combo.currentText())

    def name(self):
        return str(self.line.text())

    def dtype(self):
        return str(self.combo_dtypes.currentText())


class RenameModel(QtGui.QWidget):

    def __init__(self, models, model_name="", parent=None):
        super(RenameModel, self).__init__(parent=parent)
        self.models = models

        layout = QtGui.QGridLayout(self)

        self.label = QtGui.QLabel("Select model you want to rename: ")
        self.label2 = QtGui.QLabel("Write new name: ")
        self.combo = QtGui.QComboBox(self)
        self.combo.addItems(self.models)
        if not model_name:
            model_name = self.models[0]
        self.combo.setCurrentIndex(self.models.index(model_name))
        self.line = QtGui.QLineEdit(str(model_name))

#         self.ok_button = QtGui.QPushButton("Ok")

        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.combo, 0, 1)
        layout.addWidget(self.label2, 1, 0)
        layout.addWidget(self.line, 1, 1)
#         layout.addWidget(self.ok_button, 2, 0, 2, 2)

        self.setLayout(layout)

    def new_name(self):
        return self.line.text()

    def old_name(self):
        return self.combo.currentText()
