# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
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
__revision__ = ""

from openalea.oalab.plugins.applets import PluginApplet


class World(PluginApplet):

    name = 'World'
    alias = 'World'
    icon = 'oxygen_world.png'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.gui.world import WorldBrowser
        return WorldBrowser

    def graft(self, **kwds):
        mainwindow = kwds['oa_mainwin'] if 'oa_mainwin' in kwds else None
        applet = kwds['applet'] if 'applet' in kwds else None

        if applet is None or mainwindow is None:
            return

        self._fill_menu(mainwindow, applet)
        mainwindow.add_applet(applet, self.alias, area='inputs')


class WorldControl(PluginApplet):

    name = 'WorldControl'
    alias = 'WorldControl'
    icon = 'oxygen_world_control.png'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.gui.world import WorldControlPanel
        return WorldControlPanel
