# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
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

import logging

import sys

from openalea.core.service.plugin import debug_plugin, plugins
from openalea.oalab.cli.parser import CommandLineParser

def launch_lab(plugin_class):
    from openalea.oalab.widget.splittablewindow import OALabMainWin
    from openalea.core.settings import get_openalea_home_dir
    from openalea.core.path import path as Path
    from openalea.core.service.introspection import label
    from openalea.oalab.utils import qicon

    plugin = plugin_class()
    lab_class = plugin()
    layout_path = Path(get_openalea_home_dir()) / '%s.oaui' % lab_class.name
    OALabMainWin.DEFAULT_LAYOUT_PATH = layout_path
    OALabMainWin.DEFAULT_LAYOUT = lab_class.layout
    OALabMainWin.DEFAULT_MENU_NAMES = lab_class.menu_names
    OALabMainWin.LAB = lab_class
    if hasattr(lab_class, "start"):
        lab_class.start()

    win = OALabMainWin(lab=lab_class, autosave=True)
    win.setWindowIcon(qicon(lab_class.icon))

    if hasattr(lab_class, 'connect_applet'):
        win.appletSet.connect(lab_class.connect_applet)

    win.emit_applet_set()
    win.initialize()

    if hasattr(lab_class, "initialize"):
        lab_class.initialize()

    win.setWindowTitle('OpenAleaLab "%s"' % label(plugin))
    win.showMaximized()
    win.raise_()

    return win

def main():
    """
    1. Parse command line arguments.
    2. If GUI enabled (session.gui), launch QApplication
    3. Search an extension in "oalab.extension" plugins.
        - If found, launch extension
        - If not found, quit application and shows available extensions
    """
    class Session(object):
        pass

    session = Session()
    cli = CommandLineParser(session=session)
    cli.parse()

    if session.gui:
        from Qt import QtGui, QtWidgets
        from openalea.core.settings import get_openalea_home_dir
        from openalea.core.path import path as Path

        app = QtWidgets.QApplication(sys.argv)

        win = None
        # Run all extension matching session.extension
        available_extensions = []

        for plugin in plugins('oalab.lab'):
            plugin_class = plugin.__class__

            try:
                ext = plugin_class.name
            except AttributeError:
                continue
            else:
                # register plugin info for user.
                args = dict(EXT=ext, MODULE=plugin_class.__module__, CLASS=plugin_class.__name__)
                text = '  - \033[94m%(EXT)s\033[0m (provided by class %(CLASS)s defined in %(MODULE)s)' % args
                available_extensions.append(text)

            if session.extension == ext:
                win = launch_lab(plugin_class)
                break

        if win is None:
            from openalea.oalab.manager.selector import select_manager_item
            from openalea.core.service.plugin import default_plugin_manager
            from openalea.oalab.widget.pages import WelcomePage
            plugin_class = select_manager_item(default_plugin_manager(), 'oalab.lab', title='Select a Laboratory',
                                               style=WelcomePage.STYLE_LARGE)
            if plugin_class:
                win = launch_lab(plugin_class)

        if win:
            app.exec_()
        else:
            print 'Extension %r not found' % session.extension
            print 'Please choose a valid \033[94mextension\033[0m:'
            print '\n'.join(available_extensions)

if(__name__ == "__main__"):
    main()
