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

from openalea.oalab.plugins.applets import PluginApplet

class FileBrowser(PluginApplet):

    name = 'FileBrowser'
    alias = 'File Browser'

    def __call__(self, mainwindow):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.gui.browser import FileBrowser
        self._applet = self.new(self.name, FileBrowser, controller=mainwindow)
        mainwindow.add_applet(self._applet, self.alias, area='inputs')


