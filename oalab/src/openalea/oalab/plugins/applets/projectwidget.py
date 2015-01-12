
from openalea.oalab.plugins.applets import PluginApplet


class ProjectManager(PluginApplet):

    name = 'ProjectManager'
    alias = 'Project'
    icon = 'adwaita_accessories-dictionary.png'

    def __call__(self):
        from openalea.oalab.project.projectwidget import ProjectManagerWidget
        return ProjectManagerWidget

    def graft(self, **kwds):
        mainwindow = kwds['oa_mainwin'] if 'oa_mainwin' in kwds else None
        applet = kwds['applet'] if 'applet' in kwds else None

        if applet is None or mainwindow is None:
            return

        self._fill_menu(mainwindow, applet)

        mainwindow.menu_classic['Project'].addSeparator()
        mainwindow.menu_classic['Project'].addMenu(applet.menu_available_projects)
        mainwindow.menu_classic['Project'].addSeparator()

        mainwindow.add_applet(applet, self.alias, area='inputs')
