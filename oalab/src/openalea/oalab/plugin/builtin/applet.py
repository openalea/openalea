# -*- coding: utf-8 -*-
# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014-2015 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
__revision__ = ""

from openalea.core.plugin import PluginDef

gmalandain = {'name': u'Grégoire Malandain', 'email': u'gregoire.malandain@inria.fr'}
gmichelin = {'name': u'Gaël Michelin', 'email': u'gael.michelin@inria.fr'}

agabor = {'email': u'annamaria.kiss@ens-lyon.fr', 'name': u'Annamaria Gabor'}
agpr = {'email': u'vincent.mirabet@ens-lyon.fr', 'name': u'Vincent Mirabet'}
akonig = {'email': u'alizon.konig@inria.fr', 'name': u'Alizon K\xf6nig'}
asbriand = {'email': u'as.briand@hotmail.fr', 'name': u'Anne-Sarah Briand'}
dbarbeau = {'email': u'daniel.barbeau@inria.fr', 'name': u'Daniel Barbeau'}
dufourko = {'email': u'samuel.dufour@cirad.fr', 'name': u'Samuel Dufour-Kowalski'}
fernande = {'email': u'romainfernandez06@gmail.com', 'name': u'Romain Fernandez'}
gbaty = {'email': u'guillaume.baty@inria.fr', 'name': u'Guillaume Baty'}
gcerutti = {'email': u'guillaume.cerutti@inria.fr', 'name': u'Guillaume Cerutti'}
godin = {'email': u'christophe.godin@inria.fr', 'name': u'Christophe Godin'}
jcoste = {'email': u'julien.coste@inria.fr', 'name': u'Julien Coste'}
jlegra02 = {'email': u'jonathan.legrand@ens-lyon.fr', 'name': u'Jonathan Legrand'}
leoguignard = {'email': u'leo.guignard@inria.fr', 'name': u'L\xe9o Guignard'}
moscardi = {'email': u'eric.moscardi@gmail.com', 'name': u'Eric Moscardi'}
oali = {'email': u'olivier.ali@inria.fr', 'name': u'Olivier Ali'}
pfernique = {'email': u'pierre.fernique@inria.fr', 'name': u'Pierre Fernique'}
pradal = {'email': u'christophe.pradal@inria.fr', 'name': u'Christophe Pradal'}
refahi = {'email': u'yassin.refahi@gmail.com', 'name': u'Yassin Refahi'}
sribes = {'email': u'sophie.ribes@inria.fr', 'name': u'Sophie Ribes'}
diener = {'email': u'julien.diener@gmail.com', 'name': u'Julien Diener'}
boudon = {'email': u'frederic.boudon@cirad.fr', 'name': u'Frederic Boudon'}


class AppletPlugin(object):
    name_conversion = PluginDef.DROP_PLUGIN


@PluginDef
class ContextualMenu(AppletPlugin):
    label = 'Contextual Menu'
    authors = [jcoste, gbaty]

    def __call__(self):
        from openalea.oalab.widget.menu import ContextualMenu
        return ContextualMenu


@PluginDef
class ControlManager(AppletPlugin):
    label = 'Controls'
    icon = 'controlmanager.png'
    authors = [gbaty]

    def __call__(self):
        from openalea.oalab.control.manager import ControlManagerWidget
        return ControlManagerWidget


@PluginDef
class EditorManager(AppletPlugin):
    label = 'Model Editor'
    icon = 'oxygen_text-x-python.png'
    authors = [jcoste, gbaty]

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.paradigm.container import ModelEditorApplet
        return ModelEditorApplet


@PluginDef
class FileBrowser(AppletPlugin):
    label = 'File Browser'
    icon = 'oxygen_system-file-manager.png'
    authors = [jcoste, gbaty]

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.widget.browser import FileBrowser
        return FileBrowser


@PluginDef
class HelpWidget(AppletPlugin):
    label = 'Help'
    icon = 'oxygen_system-help.png'
    authors = [jcoste]

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.widget.help import HelpWidget
        return HelpWidget


@PluginDef
class HistoryWidget(AppletPlugin):
    label = 'History'
    icon = 'Crystal_Clear_app_clock.png'
    authors = [jcoste]

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.widget.history import HistoryWidget as History
        return History


@PluginDef
class Logger(AppletPlugin):
    icon = 'icon_logger2.png'
    authors = [dbarbeau, pradal]

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.widget.logger import Logger as LoggerWidget
        return LoggerWidget


@PluginDef
class PkgManagerWidget(AppletPlugin):
    label = 'VisualeaPkg'
    icon = ":/images/resources/openalealogo.png"
    authors = [dufourko, pradal, gbaty, jcoste]

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.package.widgets import PackageManagerTreeView
        return PackageManagerTreeView


@PluginDef
class MplFigureWidget(AppletPlugin):

    name = 'FigureWidget'
    label = 'Figure (Matplotlib)'
    icon = 'icon_mplfigure.png'
    authors = [diener, gbaty]

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.plot2d.figurewidget import MplFigureWidget
        return MplFigureWidget


class MplTabWidget(AppletPlugin):

    name = 'Plot2d'
    label = '2D Plots (Matplotlib)'
    icon = 'icon_mplwidget.png'
    authors = [diener, gbaty]

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.plot2d.mplwidget import MplTabWidget
        return MplTabWidget


@PluginDef
class ProjectManager(AppletPlugin):
    label = 'Project'
    icon = 'adwaita_accessories-dictionary.png'
    authors = [jcoste, gbaty]

    def __call__(self):
        from openalea.oalab.project.projecteditor import ProjectEditorWidget
        return ProjectEditorWidget


@PluginDef
class ShellWidget(AppletPlugin):
    label = 'Shell'
    icon = 'oxygen_utilities-terminal.png'
    authors = [boudon, jcoste, gbaty, pradal]

    def __call__(self):
        from openalea.oalab.shell.shell import get_shell_class
        return get_shell_class()


@PluginDef
class SplitterApplet(AppletPlugin):
    icon = 'oxygen_view-split-top-bottom.png'
    label = 'Splitter'
    authors = [gbaty]

    def __call__(self):
        from openalea.oalab.widget.splittablewindow import SplitterApplet
        return SplitterApplet


@PluginDef
class Store(AppletPlugin):

    def __call__(self):
        from openalea.oalab.widget.store import Store
        return Store


@PluginDef
class World(AppletPlugin):
    icon = 'oxygen_world.png'

    authors = [gbaty, jcoste, gcerutti]

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.widget.world import WorldBrowser
        return WorldBrowser


@PluginDef
class WorldControl(AppletPlugin):
    label = 'World Controls'
    icon = 'oxygen_world_control.png'
    authors = [gcerutti, gbaty]

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.widget.world import WorldControlPanel
        return WorldControlPanel
