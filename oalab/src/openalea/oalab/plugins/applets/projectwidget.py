
from openalea.oalab.plugins.applets import PluginApplet

class ProjectManager(PluginApplet):

    name = 'ProjectManager'
    alias = 'Project'

    def __call__(self):
        from openalea.oalab.project.projectwidget import ProjectManagerWidget
        return ProjectManagerWidget

    def graft(self, mainwindow):
        self._applet = self.new(self.name, self())
        self._fill_menu(mainwindow, self._applet)
        mainwindow.menu_classic['Project'].addSeparator()
        mainwindow.menu_classic['Project'].addMenu(self._applet.menu_available_projects)
        mainwindow.menu_classic['Project'].addSeparator()
        mainwindow.add_applet(self._applet, self.alias, area='inputs')
