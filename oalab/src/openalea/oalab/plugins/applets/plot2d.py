
from openalea.oalab.plugins.applets import PluginApplet


class MplFigureWidget(object):

    name = 'FigureWidget'
    alias = 'Figure (Matplotlib)'
    icon = 'icon_mplfigure.png'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.plot2d.figurewidget import MplFigureWidget
        return MplFigureWidget


class MplTabWidget(PluginApplet):

    name = 'Plot2d'
    alias = '2D Plots (Matplotlib)'
    icon = 'icon_mplwidget.png'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.plot2d.mplwidget import MplTabWidget
        return MplTabWidget

    def graft(self, **kwds):
        mainwindow = kwds['oa_mainwin'] if 'oa_mainwin' in kwds else None
        applet = kwds['applet'] if 'applet' in kwds else None

        if applet is None or mainwindow is None:
            return

        mainwindow.add_applet(applet, self.alias, area='outputs')

        actions = applet.get_plugin_actions()

        if actions:
            for action in actions:
                # Add actions in PanedMenu
                mainwindow.menu.addBtnByAction('Plot2d', *action)

                # add action in classical menu
                group_name, act, btn_type = action
                mainwindow.add_action_to_existing_menu(action=act, menu_name='Plot2d', sub_menu_name=group_name)
