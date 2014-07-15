
from openalea.oalab.plugins.applets import PluginApplet

class MatplotlibWidget(PluginApplet):

    name = 'MatplotlibWidget'
    alias = 'Matplotlib'

    def __call__(self, mainwindow):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.matplotlib import activate_in_pyplot
        from openalea.oalab.matplotlib.widget import MplTabWidget
        from matplotlib import pyplot as plt

        self._applet = MplTabWidget.get_singleton()
        activate_in_pyplot()
        plt.ion()
        mainwindow.add_applet(self._applet, self.alias, area='outputs')
