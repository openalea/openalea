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


@PluginDef
class ContextualMenu(object):

    name = 'ContextualMenu'
    alias = 'Contextual Menu'

    def __call__(self):
        from openalea.oalab.widget.menu import ContextualMenu
        return ContextualMenu


@PluginDef
class ControlManager(object):

    name = 'ControlManager'
    alias = 'Controls'
    icon = 'controlmanager.png'

    def __call__(self):
        from openalea.oalab.control.manager import ControlManagerWidget
        return ControlManagerWidget


@PluginDef
class EditorManager(object):

    name = 'EditorManager'
    alias = 'Model Editor'
    icon = 'oxygen_text-x-python.png'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.paradigm.container import ParadigmContainer
        return ParadigmContainer


@PluginDef
class FileBrowser(object):

    name = 'FileBrowser'
    alias = 'File Browser'
    icon = 'oxygen_system-file-manager.png'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.widget.browser import FileBrowser
        return FileBrowser


@PluginDef
class HelpWidget(object):

    name = 'HelpWidget'
    alias = 'Help'
    icon = 'oxygen_system-help.png'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.widget.help import HelpWidget
        return HelpWidget


@PluginDef
class HistoryWidget(object):
    name = 'HistoryWidget'
    alias = 'History'
    icon = 'Crystal_Clear_app_clock.png'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.widget.history import HistoryWidget as History
        return History


@PluginDef
class Logger(object):

    name = 'Logger'
    alias = 'Logger'
    icon = 'icon_logger2.png'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.widget.logger import Logger as LoggerWidget
        return LoggerWidget


@PluginDef
class PkgManagerWidget(object):

    name = 'PkgManagerWidget'
    alias = 'VisualeaPkg'
    icon = ":/images/resources/openalealogo.png"

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.package.widgets import PackageManagerTreeView
        return PackageManagerTreeView


class MplFigureWidget(object):

    name = 'FigureWidget'
    alias = 'Figure (Matplotlib)'
    icon = 'icon_mplfigure.png'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.plot2d.figurewidget import MplFigureWidget
        return MplFigureWidget


class MplTabWidget(object):

    name = 'Plot2d'
    alias = '2D Plots (Matplotlib)'
    icon = 'icon_mplwidget.png'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.plot2d.mplwidget import MplTabWidget
        return MplTabWidget


@PluginDef
class ProjectManager(object):

    name = 'ProjectManager'
    alias = 'Project'
    icon = 'adwaita_accessories-dictionary.png'

    def __call__(self):
        from openalea.oalab.project.projectwidget import ProjectManagerWidget
        return ProjectManagerWidget


@PluginDef
class ShellWidget(object):

    name = 'ShellWidget'
    alias = 'Shell'
    icon = 'oxygen_utilities-terminal.png'

    def __call__(self):
        from openalea.oalab.shell.shell import get_shell_class
        return get_shell_class()


@PluginDef
class SplitterApplet(object):
    icon = 'oxygen_view-split-top-bottom.png'
    name = 'SplitterApplet'
    alias = 'Splitter'

    def __call__(self):
        from openalea.oalab.widget.splittablewindow import SplitterApplet
        return SplitterApplet


@PluginDef
class Store(object):

    name = 'Store'
    alias = 'Store'

    def __call__(self):
        from openalea.oalab.widget.store import Store
        return Store


@PluginDef
class World(object):

    name = 'World'
    alias = 'World'
    icon = 'oxygen_world.png'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.widget.world import WorldBrowser
        return WorldBrowser


@PluginDef
class WorldControl(object):

    name = 'WorldControl'
    alias = 'WorldControl'
    icon = 'oxygen_world_control.png'

    def __call__(self):
        # Load and instantiate graphical component that actually provide feature
        from openalea.oalab.widget.world import WorldControlPanel
        return WorldControlPanel
