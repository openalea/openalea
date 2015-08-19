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
from openalea.core import settings
from openalea.core.observer import AbstractListener
from openalea.core.path import path
from openalea.core.plugin import iter_plugins
from openalea.core.service.data import DataClass, MimeType
from openalea.core.service.plugin import debug_plugin, plugins
from openalea.core.service.plugin import plugin_instance_exists, plugin_instance, plugins
from openalea.core.service.project import write_project_settings, default_project, projects
from openalea.core.settings import get_default_home_dir
from openalea.oalab.project.creator import CreateProjectWidget
from openalea.oalab.project.dialog import SelectCategory, RenameModel
from openalea.oalab.project.pretty_preview import ProjectSelectorScroll
from openalea.oalab.project.projectbrowser import ProjectBrowserWidget, ProjectBrowserView
from openalea.oalab.service.drag_and_drop import add_drag_format, encode_to_qmimedata
from openalea.oalab.utils import ModalDialog
from openalea.oalab.utils import qicon
from openalea.oalab.widget import resources_rc
from openalea.vpltk.qt import QtGui, QtCore


class ProjectEditorWidget(ProjectBrowserWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)

        layout = QtGui.QVBoxLayout(self)
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
            self.paradigm_container.paradigms_actions = self.view.paradigms_actions
            self.item_double_clicked.connect(self._on_item_double_clicked)
            self.item_removed.connect(self._on_item_removed)
            self.project_closed.connect(self._on_project_closed)
            self.project_open.connect(self._on_project_open)

    def _on_project_closed(self, project):
        welcome_actions = [self.actionNewProj, self.view.actionOpenProj]
        self.paradigm_container.set_welcome_actions(welcome_actions)
        self.paradigm_container.close_all()

    def _on_project_open(self, project):
        welcome_actions = self.view.paradigms_actions
        self.paradigm_container.set_welcome_actions(welcome_actions)
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

        self.paradigms = {}
        self._new_file_actions = {}
        self.paradigms_actions = []
        for plugin in plugins('oalab.plugin', criteria=dict(implement='IParadigmApplet')):
            applet = debug_plugin('oalab.plugin', func=plugin)
            if applet:
                self.paradigms[plugin.name] = applet
                action = QtGui.QAction(QtGui.QIcon(applet.icon), "New " + applet.default_name, self)
                action.triggered.connect(self.new_file)
                self.paradigms_actions.append(action)
                self._new_file_actions[action] = applet
                self._actions.append(["Project", "Manage", action, 1],)

    def open_project_item(self, category, item):
        if self.paradigm_container:
            self.paradigm_container.open_data(item)

    def add_new_file_actions(self, menu):
        menu.addActions(self._new_file_actions.keys())
        menu.addSeparator()

    def create_menu(self):

        menu = QtGui.QMenu(self)
        actions = ProjectBrowserView.create_menu(self).actions()
        if actions:
            menu.addActions(actions)
            menu.addSeparator()

        project, category, obj = self.selected_data()

        if category == 'category' and obj == 'model':
            self.add_new_file_actions(menu)

        elif category == 'category' and obj in ('startup', 'lib'):
            new_startup = QtGui.QAction(qicon('filenew.png'), 'New file', self)
            new_startup.triggered.connect(self._new_file)
            menu.addAction(new_startup)

        if category == 'model':
            self.add_new_file_actions(menu)

        return menu

    def _new_file(self):
        category = 'model'
        try:
            dtype = self._new_file_actions[self.sender()]
            name = '%s_%s.%s' % (dtype, category, DataClass(MimeType(name=dtype)).extension)
        except KeyError:
            dtype = None
            name = 'new_file.ext'

        category, data = self.add(self.project(), name, code='', dtype=dtype, category=category)
        if data:
            self.open_data(data)

    def new_file(self, dtype=None):
        try:
            applet = self._new_file_actions[self.sender()]
        except KeyError:
            dtype = None
        else:
            dtype = applet.default_name
        project, category, data = self.selected_data()
        code = ''
        project = self.project()

        if category == 'category':
            category = data
        elif category in project.DEFAULT_CATEGORIES:
            pass
        else:
            category = None

        if dtype is None and category in ['startup', 'lib']:
            dtype = 'Python'

        if category in ['startup', 'lib']:
            d = {'startup': 'start.py', 'lib': 'algo.py'}
            name = d[category]
        elif dtype:
            klass = DataClass(MimeType(name=dtype))
            name = '%s_%s.%s' % (klass.default_name, category, klass.extension)
        else:
            name = category
        category, data = self.add(project, name, code, dtype=dtype, category=category)
        self.open_project_item(category, data)

    def add(self, project, name, code, dtype=None, category=None):
        project = self.project()
        if dtype is None:
            dtypes = [pl.default_name for pl in plugins('openalea.core', criteria=dict(implement='IModel'))]
        else:
            dtypes = [dtype]

        if category:
            categories = [category]
        else:
            categories = project.DEFAULT_CATEGORIES.keys()
        selector = SelectCategory(filename=name, categories=categories, dtypes=dtypes)
        dialog = ModalDialog(selector)
        if dialog.exec_():
            category = selector.category()
            filename = selector.name()
            dtype = selector.dtype()
            path = project.path / category / filename
            data = project.get_item(category, filename)
            if path.exists() and data is None:
                box = QtGui.QMessageBox.information(self, 'Data yet exists',
                                                    'Data with name %s already exists in this project, just add it' % filename)
                code = None
                data = project.add(category=category, filename=filename, content=code, dtype=dtype)
            elif path.exists() and data:
                pass
            else:
                data = project.add(category=category, filename=filename, content=code, dtype=dtype)
            if data:
                self.open_project_item(category, data)
                return category, data
        return None, None
