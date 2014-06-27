
from openalea.oalab.plugins.applets import PluginApplet

class ProjectWidget(PluginApplet):

    name = 'ProjectWidget'
    alias = 'Project'

    def __call__(self, mainwindow):
        from openalea.oalab.project.treeview import ProjectLayoutWidget

        self._applet = self.new(self.name, ProjectLayoutWidget, mainwindow)
        self._fill_menu(mainwindow, self._applet)

        mainwindow.add_applet(self._applet, self.alias, area='inputs')

class ProjectManager2(PluginApplet):

    name = 'ProjectManager2'
    alias = 'Project'

    def __call__(self, mainwindow):
        from openalea.oalab.project.projectwidget import ProjectManagerWidget

        self._applet = self.new(self.name, ProjectManagerWidget)
        self._fill_menu(mainwindow, self._applet)
        mainwindow.menu_classic['Project'].addSeparator()
        mainwindow.menu_classic['Project'].addMenu(self._applet.menu_available_projects)
        mainwindow.menu_classic['Project'].addSeparator()
        mainwindow.add_applet(self._applet, self.alias, area='inputs')
