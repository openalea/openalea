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

from time import gmtime, strftime

from openalea.core import settings
from openalea.core.path import path
from openalea.core.project import Project, ProjectManager
from openalea.oalab.service.qt_control import widget
from openalea.vpltk.qt import QtGui, QtCore


class CreateProjectWidget(QtGui.QWidget):

    """
    Object which permit to create projects.
    """

    def __init__(self, proj=None, parent=None):
        super(CreateProjectWidget, self).__init__(parent)
        self.pm = ProjectManager()

        self.widget_metadata = QtGui.QWidget()
        self.widget_path = QtGui.QWidget()

        layout_path = QtGui.QFormLayout(self.widget_path)

        # Name and path
        if proj is None:
            date = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
            name = 'project_%s' % date if not proj else proj.name
            projectdir = self.pm.defaultdir
        else:
            name = proj.name
            projectdir = proj.path.parent

        self.editor_name = widget('IStr', name)
        self.editor_projectdir = widget('IDirStr', projectdir)

        layout_path.addRow(QtGui.QLabel('Name'), self.editor_name)
        layout_path.addRow(QtGui.QLabel('Project Directory'), self.editor_projectdir)
        layout_path.setLabelAlignment(QtCore.Qt.AlignLeft)

        # Metadata
        self._metadata = {}
        layout_metadata = QtGui.QFormLayout(self.widget_metadata)
        layout_metadata.setLabelAlignment(QtCore.Qt.AlignLeft)

        for cat, metadata in Project.DEFAULT_METADATA.iteritems():
            label = QtGui.QLabel(metadata.name.capitalize().replace('_', ' '))
            editor = widget(metadata.interface, metadata.value)
            editor.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
            self._metadata[cat] = editor
            layout_metadata.addRow(label, editor)

        if proj:
            for key in proj.DEFAULT_METADATA:
                self._metadata[key].setValue(proj.metadata[key])
            title = "Edit '%s' metadata" % proj.name
        else:
            title = "New Project"

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(QtGui.QLabel(title))
        layout.addWidget(self.widget_path)
        layout.addWidget(self.widget_metadata)

    def project(self):
        projectdir = self.editor_projectdir.value()
        name = self.editor_name.value()
        metadata = self.metadata()
        project = self.pm.create(name, projectdir, **metadata)
        return project

    def metadata(self):
        metadata = {}
        for key, editor in self._metadata.iteritems():
            metadata[key] = editor.value()
        return metadata


def main():
    import sys

    app = QtGui.QApplication(sys.argv)
#     pm = ProjectManager()
#     pm.discover()
#     proj = pm.load('Koch')
    proj = None
    widg = CreateProjectWidget(proj)
    widg.show()
    app.exec_()
    project = widg.project()
    print project
    for k, v in project.metadata.iteritems():
        print '    - %s: %s' % (k, v)


if __name__ == "__main__":
    main()
