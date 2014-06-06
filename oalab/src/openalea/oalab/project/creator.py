# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
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
__revision__ = "$Id: "

from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.path import path
from time import gmtime, strftime
from openalea.core import settings
from openalea.vpltk.project import Project


class CreateProjectWidget(QtGui.QWidget):
    """
    Object which permit to create projects.
    """
    def __init__(self, proj=None, parent=None):
        super(CreateProjectWidget, self).__init__(parent)
        self.project = None
        layout = QtGui.QGridLayout(self)

        layout.addWidget(QtGui.QLabel("Fill this to set metadata of your project"), 0, 0)
        categories = ["name", "author", "author_email", "description", "long_description", "citation", "url", "icon",
                      "dependencies", "license", "version"]
        i = 1
        for cat in categories:
            wid = QtGui.QLabel(cat)
            layout.addWidget(wid, i, 0)
            i += 1

        if not proj:
            date = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
            self.name_lineedit = QtGui.QLineEdit('project_%s' % date)
            self.name_lineedit.setMinimumWidth(300)
            layout.addWidget(self.name_lineedit, 1, 1)
            self.author_lineedit = QtGui.QLineEdit('OpenAlea Consortium')
            layout.addWidget(self.author_lineedit, 2, 1)
            self.author_email_lineedit = QtGui.QLineEdit('')
            layout.addWidget(self.author_email_lineedit, 3, 1)
            self.description_lineedit = QtGui.QLineEdit('')
            layout.addWidget(self.description_lineedit, 4, 1)
            self.long_description_lineedit = QtGui.QLineEdit('')
            layout.addWidget(self.long_description_lineedit, 5, 1)
            self.citation_lineedit = QtGui.QLineEdit('')
            layout.addWidget(self.citation_lineedit, 6, 1)
            self.url_lineedit = QtGui.QLineEdit('')
            layout.addWidget(self.url_lineedit, 7, 1)
            self.icon_lineedit = QtGui.QLineEdit('')
            layout.addWidget(self.icon_lineedit, 8, 1)
            self.dependencies_lineedit = QtGui.QLineEdit('[]')
            layout.addWidget(self.dependencies_lineedit, 9, 1)
            self.license_lineedit = QtGui.QLineEdit('CeCILL-C')
            layout.addWidget(self.license_lineedit, 10, 1)
            self.version_lineedit = QtGui.QLineEdit('0.1')
            layout.addWidget(self.version_lineedit, 11, 1)

            layout.addWidget(QtGui.QLabel("path"), 12, 0)
            path_ = path(settings.get_project_dir())
            self.path_lineedit =  QtGui.QLineEdit(str(path_))

            # TODO: remove this line when Project Manager works fine and permit to search outside default directory
            self.path_lineedit.setReadOnly(True)

            layout.addWidget(self.path_lineedit, 12, 1)

            # TODO: uncomment this lines ...
            # self.btn_path = QtGui.QPushButton("   ...   ")
            # layout.addWidget(self.btn_path, 12, 2)
            # self.connect(self.btn_path, QtCore.SIGNAL('clicked()'), self.select_path)

            self.ok_btn = QtGui.QPushButton("Create metadata set")
            layout.addWidget(self.ok_btn, 13, 0, 1, 3)
            self.connect(self.ok_btn, QtCore.SIGNAL('clicked()'), self.ok_clicked)
        else:
            self.name_lineedit = QtGui.QLineEdit(proj.name)
            self.name_lineedit.setMinimumWidth(300)
            layout.addWidget(self.name_lineedit, 1, 1)
            self.author_lineedit = QtGui.QLineEdit(proj.author)
            layout.addWidget(self.author_lineedit, 2, 1)
            self.author_email_lineedit = QtGui.QLineEdit(proj.author_email)
            layout.addWidget(self.author_email_lineedit, 3, 1)
            self.description_lineedit = QtGui.QLineEdit(proj.description)
            layout.addWidget(self.description_lineedit, 4, 1)
            self.long_description_lineedit = QtGui.QLineEdit(proj.long_description)
            layout.addWidget(self.long_description_lineedit, 5, 1)
            self.citation_lineedit = QtGui.QLineEdit(proj.citation)
            layout.addWidget(self.citation_lineedit, 6, 1)
            self.url_lineedit = QtGui.QLineEdit(proj.url)
            layout.addWidget(self.url_lineedit, 7, 1)
            self.icon_lineedit = QtGui.QLineEdit(proj.icon)
            layout.addWidget(self.icon_lineedit, 8, 1)
            self.dependencies_lineedit = QtGui.QLineEdit(str(proj.dependencies))
            layout.addWidget(self.dependencies_lineedit, 9, 1)
            self.license_lineedit = QtGui.QLineEdit(proj.license)
            layout.addWidget(self.license_lineedit, 10, 1)
            self.version_lineedit = QtGui.QLineEdit(proj.version)
            layout.addWidget(self.version_lineedit, 11, 1)

            layout.addWidget(QtGui.QLabel("path"), 12, 0)
            self.path_lineedit =  QtGui.QLineEdit(str(proj.path))

            # TODO: remove this line when Project Manager works fine and permit to search outside default directory
            self.path_lineedit.setReadOnly(True)

            layout.addWidget(self.path_lineedit, 12, 1)

            # TODO: uncomment this lines ...
            # self.btn_path = QtGui.QPushButton("   ...   ")
            # layout.addWidget(self.btn_path, 12, 2)
            # self.connect(self.btn_path, QtCore.SIGNAL('clicked()'), self.select_path)

            self.ok_btn = QtGui.QPushButton("Set metadata")
            layout.addWidget(self.ok_btn, 13, 0, 1, 3)
            self.connect(self.ok_btn, QtCore.SIGNAL('clicked()'), self.ok_clicked)

    def ok_clicked(self):
        proj = Project(name=self.name_lineedit.text(),
                       path=self.path_lineedit.text(),
                       icon=self.icon_lineedit.text(),
                       author=self.author_lineedit.text(),
                       author_email=self.author_email_lineedit.text(),
                       description=self.description_lineedit.text(),
                       long_description=self.long_description_lineedit.text(),
                       citation=self.citation_lineedit.text(),
                       url=self.url_lineedit.text(),
                       dependencies=self.url_lineedit.text(),
                       license=self.license_lineedit.text(),
                       version=self.version_lineedit.text())
        self.project = proj
        self.emit(QtCore.SIGNAL('ProjectMetadataSet(PyQt_PyObject)'), proj)
        self.hide()

    def select_path(self):
        text = "Select path where to save your project"
        my_path = self.path_lineedit.text()
        fpath = QtGui.QFileDialog.getExistingDirectory(self.parent(), text, my_path)
        if fpath:
            self.path_lineedit.setText(fpath)


def main():
    import sys

    app = QtGui.QApplication(sys.argv)
    widg = CreateProjectWidget()
    widg.show()
    app.exec_()


if __name__ == "__main__":
    main()