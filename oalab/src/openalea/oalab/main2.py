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

import sys
from openalea.oalab.cli.parser import CommandLineParser
from openalea.core.service.plugin import debug_plugin, plugins


def launch_lab(plugin_class):
    from openalea.oalab.gui.splittablewindow import OALabMainWin
    from openalea.core.settings import get_openalea_home_dir
    from openalea.core.path import path as Path
    from openalea.core.service.introspection import alias

    plugin = plugin_class()
    lab_class = plugin()
    layout_path = Path(get_openalea_home_dir()) / '%s.oaui' % lab_class.name
    OALabMainWin.DEFAULT_LAYOUT_PATH = layout_path
    OALabMainWin.DEFAULT_LAYOUT = lab_class.layout
    OALabMainWin.DEFAULT_MENU_NAMES = lab_class.menu_names
    OALabMainWin.LAB = lab_class
    if hasattr(lab_class, "start"):
        lab_class.start()
    win = OALabMainWin()
    if hasattr(lab_class, 'connect_applet'):
        win.appletSet.connect(lab_class.connect_applet)
    win.emit_applet_set()

    if hasattr(lab_class, "initialize"):
        lab_class.initialize()
    if hasattr(lab_class, "finalize"):
        win.aboutToClose.connect(lab_class.finalize)
    if hasattr(lab_class, "stop"):
        win.closed.connect(lab_class.stop)
    win.initialize()
    win.setWindowTitle('OpenAleaLab "%s"' % alias(plugin))
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
    cli = CommandLineParser(sys.argv, session)

    if session.gui:
        from openalea.vpltk.qt import QtGui
        from openalea.core.settings import get_openalea_home_dir
        from openalea.core.path import path as Path

        app = QtGui.QApplication(sys.argv)

        win = None
        # Run all extension matching session.extension
        available_extensions = []

        for plugin_class in plugins('oalab.lab'):
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
            from openalea.oalab.gui.pluginselector import select_plugin
            plugin_class = select_plugin('oalab.lab', size=(400, 10), title='Select a Laboratory')
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
