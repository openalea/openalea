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

from openalea.vpltk.qt import QtGui
from openalea.core.path import path
from time import gmtime, strftime
from openalea.core import settings
from openalea.vpltk.project.project2 import Project
from openalea.oalab.service.qt_control import widget

class CreateProjectWidget(QtGui.QWidget):
    """
    Object which permit to create projects.
    """
    def __init__(self, proj=None, parent=None):
        super(CreateProjectWidget, self).__init__(parent)
        layout = QtGui.QGridLayout(self)

        layout.addWidget(QtGui.QLabel("Fill this to set metadata of your project"), 0, 0)
        categories = ["name", "author", "author_email", "description", "long_description", "citation", "url", "icon",
                      "dependencies", "license", "version"]
        i = 1
        for cat in categories:
            wid = QtGui.QLabel(cat)
            layout.addWidget(wid, i, 0)
            i += 1

        # GBY review: need to refactorize this code, copy/paste code is hard to read, extend or modify
        # CPL: First try. Need to add a classmethod to the project giving metadata defaults.
        # d = Project.default_metadata()
        # d.update(proj.metadata())
        date = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        name = 'project_%s' % date if not proj else proj.name

        author = 'OpenAlea Consortium' if not proj else proj.author
        author_email = '' if not proj else proj.author_email
        description = '' if not proj else proj.description
        long_description = '' if not proj else proj.long_description
        citation = '' if not proj else proj.citation
        url = '' if not proj else proj.url
        icon = '' if not proj else proj.icon
        dependencies = [] if not proj else proj.dependencies
        license = 'CeCILL-C' if not proj else proj.license
        version = '0.1.0' if not proj else proj.version
        directory = path(settings.get_project_dir()) if not proj else str(proj.projectdir)


        self.name_lineedit = QtGui.QLineEdit(name)
        self.name_lineedit.setMinimumWidth(300)
        layout.addWidget(self.name_lineedit, 1, 1)

        self.author_lineedit = QtGui.QLineEdit(author)
        layout.addWidget(self.author_lineedit, 2, 1)

        self.author_email_lineedit = QtGui.QLineEdit(author_email)
        layout.addWidget(self.author_email_lineedit, 3, 1)

        self.description_lineedit = QtGui.QLineEdit(description)
        layout.addWidget(self.description_lineedit, 4, 1)

        self.long_description_lineedit = QtGui.QLineEdit(long_description)
        layout.addWidget(self.long_description_lineedit, 5, 1)

        self.citation_lineedit = QtGui.QLineEdit(citation)
        layout.addWidget(self.citation_lineedit, 6, 1)

        self.url_lineedit = QtGui.QLineEdit(url)
        layout.addWidget(self.url_lineedit, 7, 1)

        self.icon_lineedit = QtGui.QLineEdit(icon)
        layout.addWidget(self.icon_lineedit, 8, 1)

        self.dependencies_lineedit = QtGui.QLineEdit(str(dependencies))
        layout.addWidget(self.dependencies_lineedit, 9, 1)

        self.license_lineedit = QtGui.QLineEdit(license)
        layout.addWidget(self.license_lineedit, 10, 1)

        self.version_lineedit = QtGui.QLineEdit(version)
        layout.addWidget(self.version_lineedit, 11, 1)

        layout.addWidget(QtGui.QLabel("path"), 12, 0)
        self.path_lineedit = widget('IDirStr', directory, shape='hline')

        # TODO: remove this line when Project Manager works fine and permit to search outside default directory
        # CPL: Allow the user to define the path
        # self.path_lineedit.setReadOnly(True)

        layout.addWidget(self.path_lineedit, 12, 1)

    def project(self):
        proj = Project(name=self.name_lineedit.text(),
                       projectdir=self.path_lineedit.value(),
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
        return proj

    def metadata(self):
        return self.project().metadata

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
