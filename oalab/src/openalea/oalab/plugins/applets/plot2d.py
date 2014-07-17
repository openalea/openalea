
from openalea.oalab.plugins.applets import PluginApplet

class Plot2dWidget(PluginApplet):                     

    name = 'Plot2d'
    alias = 'Plot2d'

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
