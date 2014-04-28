
from openalea.oalab.applets.plugin import PluginApplet

class ProjectWidget(PluginApplet):

    name = 'ProjectWidget'
    alias = 'Project'

    def __call__(self, mainwindow):
        from openalea.oalab.project.treeview import ProjectLayoutWidget

        self._applet = ProjectLayoutWidget(mainwindow.session, mainwindow)
        self._fill_menu(mainwindow, self._applet)

        mainwindow.add_applet(self._applet, self.alias, area='inputs')
