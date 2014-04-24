
from openalea.oalab.applets.plugin import PluginApplet

class ProjectManager(PluginApplet):

    name = 'ProjectManager'
    alias = 'ProjectManager'

    def __call__(self, mainwindow):
        from openalea.oalab.project.manager import ProjectManagerWidget

        self._applet = ProjectManagerWidget(mainwindow.session, mainwindow)
        self._fill_menu(mainwindow, self._applet)

        mainwindow.add_applet(self._applet, self.alias, area='inputs')
