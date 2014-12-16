# -*- python -*-
#
#       OALab start here
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
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
import sys

from openalea.oalab.cli.parser import CommandLineParser
from openalea.core.service.plugin import debug_plugin, plugins


def main():
    """
    1. Parse command line arguments.
    2. If GUI enabled (session.gui), launch QApplication
    3. Search an extension in "oalab.extension" plugins.
        - If found, launch extension
        - If not found, quit application and shows available extensions
    """
    from openalea.oalab.project.symlink import create_project_shortcut
    from openalea.oalab.session.all import Session

    create_project_shortcut()
    session = Session()
    cli = CommandLineParser(sys.argv, session)

    if session.gui:
        from openalea.vpltk.qt import QtGui
        from openalea.oalab.gui.mainwindow import MainWindow

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
                plugin = plugin_class()
                win = MainWindow(session)
                debug_plugin('oalab.lab', func=plugin, func_args=[win])
                win.show()
                win.raise_()
                break

        if win:
            app.exec_()
        else:
            print 'Extension %r not found' % session.extension
            print 'Please choose a valid \033[94mextension\033[0m:'
            print '\n'.join(available_extensions)


def main2():
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
        from openalea.oalab.gui.splittablewindow import OALabMainWin
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
                plugin = plugin_class()
                lab = plugin()
                layout_path = Path(get_openalea_home_dir()) / '%s.oaui' % lab.name
                OALabMainWin.DEFAULT_LAYOUT_PATH = layout_path
                OALabMainWin.DEFAULT_LAYOUT = lab.layout
                OALabMainWin.DEFAULT_MENU_NAMES = lab.menu_names
                win = OALabMainWin()
                win.setWindowTitle('OpenAleaLab "%s"' % lab.name)
                win.showMaximized()
                win.raise_()
                break

        if win:
            app.exec_()
        else:
            print 'Extension %r not found' % session.extension
            print 'Please choose a valid \033[94mextension\033[0m:'
            print '\n'.join(available_extensions)
if(__name__ == "__main__"):
    main()
