# -*- python -*-
#
# OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013-2015 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#                       Guillaume Baty <guillaume.baty@inria.fr>
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

"""
TODO:
    - use project known categories instead of hard coded 'model', 'src', ...

"""

from Qt import QtCore, QtGui, QtWidgets

from openalea.core.service.data import DataClass, MimeType
from openalea.core.service.plugin import plugin_instance_exists, plugin_instance

from openalea.oalab.paradigm.creator import ParadigmCreator, ParadigmInfoSelector
from openalea.oalab.project.projectbrowser import ProjectBrowserWidget, ProjectBrowserView
from openalea.oalab.utils import ModalDialog
from openalea.oalab.widget import resources_rc

class ProjectEditorWidget(ProjectBrowserWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        layout = QtWidgets.QVBoxLayout(self)
        self.view = ProjectEditorView()
        self._transfer_view_signals()

        self.model = self.view.model()
        layout.addWidget(self.view)
        layout.setContentsMargins(0, 0, 0, 0)

        self._create_actions()
        self._create_menus()

    def initialize(self):
        # Connect to ParadigmContainer if available
        if plugin_instance_exists('oalab.applet', 'EditorManager'):
            self.paradigm_container = plugin_instance('oalab.applet', 'EditorManager')
            self.item_double_clicked.connect(self._on_item_double_clicked)
            self.item_removed.connect(self._on_item_removed)
            self.item_added.connect(self._on_item_double_clicked)
            self.project_closed.connect(self._on_project_closed)
            self.project_open.connect(self._on_project_open)

    def toolbars(self):
        toolbars = ProjectBrowserWidget.toolbars(self)
        toolbar_paradigm = QtWidgets.QToolBar("Paradigms")
        toolbar_paradigm.addActions(self.view.paradigm.actions())
        return toolbars + [toolbar_paradigm]

    def _on_project_closed(self, project):
        welcome_actions = [self.actionNewProj, self.view.actionOpenProj]
        self.paradigm_container.set_welcome_actions(welcome_actions)
        self.paradigm_container.close_all()

    def _on_project_open(self, project):
        welcome_actions = self.view.paradigm.actions()
        self.paradigm_container.set_welcome_actions(welcome_actions)
        self.paradigm_container.close_all()
        #for model in project.model.values():
        #    self.paradigm_container.open_data(model)

    def _on_item_double_clicked(self, project, category, name):
        item = project.get_item(category, name)
        self.paradigm_container.open_data(item)

    def _on_item_removed(self, project, category, item):
        self.paradigm_container.close_data(item)


class ProjectEditorView(ProjectBrowserView):

    def __init__(self):
        ProjectBrowserView.__init__(self)

        self.paradigm_container = None
        self.contextual_creator = ParadigmCreator(self)
        self.contextual_creator.paradigm_clicked.connect(self.new_contextual_paradigm)

        self.paradigm = ParadigmCreator(self)
        self.paradigm.paradigm_clicked.connect(self.new_paradigm)

    def add_new_file_actions(self, menu, paradigms=None):
        if paradigms is None:
            menu.addActions(self.contextual_creator.actions())
        else:
            for paradigm in paradigms:
                menu.addAction(self.contextual_creator.action(paradigm))
        menu.addSeparator()

    def create_menu(self):

        menu = QtWidgets.QMenu(self)
        actions = ProjectBrowserView.create_menu(self).actions()
        if actions:
            menu.addActions(actions)
            menu.addSeparator()

        project, category, obj = self.selected_data()

        if category == 'category' and obj == 'model':
            self.add_new_file_actions(menu)

        elif category == 'category' and obj in ('startup', 'lib'):
            self.add_new_file_actions(menu, ['Python'])

        if category == 'model':
            self.add_new_file_actions(menu)

        return menu

    def _new_paradigm(self, project, category=None, dtype=None, name=None):
        klass = DataClass(MimeType(name=dtype))
        if name is None:
            # Builtin default name for some categories
            if category in ['startup', 'lib']:
                d = {'startup': 'start.py', 'lib': 'algo.py'}
                name = d[category]
            else:
                # If category defined, use it in name
                if category:
                    name = '%s_%s.%s' % (klass.default_name.lower(), category.lower(), klass.extension)
                else:
                    name = 'file.%s' % klass.extension

        # Change extension to fit dtype (case name is given with wrong extension)
        parts = name.split('.')
        parts[-1] = klass.extension
        default_name = '.'.join(parts)

        if category:
            categories = [category]
        else:
            categories = project.categories.keys()

        # Show dialog
        w = ParadigmInfoSelector(default_name, categories, [dtype],
                                 project=project)
        dialog = ModalDialog(w)
        w.validity_changed.connect(dialog.set_valid)
        dialog.set_valid(w.is_valid())
        if dialog.exec_():
            name = w.name()
            category = w.category()
            dtype = w.dtype()
            p = project.path / category / name
            if p.exists():
                project.add(category, path=p)
            else:
                project.add(category, filename=name, content="", dtype=dtype)
            self.item_added.emit(project, category, name)

    def new_contextual_paradigm(self, dtype):
        project, category, data = self.selected_data()
        name = None
        if category == 'category':
            category = data
        elif category in project.categories:
            name = data
        else:
            category = None

        self._new_paradigm(project, category, dtype, name)

    def new_paradigm(self, dtype):
        project = self.project()
        self._new_paradigm(project, dtype=dtype)
