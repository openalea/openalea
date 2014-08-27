
from openalea.oalab.plugins.applets import PluginApplet

class Plot2dWidget(PluginApplet):                     

    name = 'Plot2d'
    alias = 'Plot2d'
    dependencies = ["openalea.oalab.plot2d", "matplotlib"]

    def __call__(self, mainwindow):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.plot2d import activate_in_pyplot
        from openalea.oalab.plot2d.widget import MplTabWidget
        from matplotlib import pyplot as plt                     
        
        # work with qt4agg backend
        plt.switch_backend('qt4agg')

        self._applet = MplTabWidget.get_singleton()
        activate_in_pyplot()
        plt.ion()
        mainwindow.add_applet(self._applet, self.alias, area='outputs')
        
        actions = self._applet.get_plugin_actions()
        if actions:
            for action in actions:
                # Add actions in PanedMenu
                mainwindow.menu.addBtnByAction('Plot2d', *action)

                # add action in classical menu
                group_name, act, btn_type = action
                mainwindow.add_action_to_existing_menu(action=act, menu_name='Plot2d', sub_menu_name=group_name)

