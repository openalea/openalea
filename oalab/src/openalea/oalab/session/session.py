# -*- coding: utf-8 -*-
# -*- python -*-
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
__revision__ = ""

__all__ = ['Session']

import os
import sys
from openalea.core.service.ipython import interpreter
from openalea.core.service.run import get_model
from openalea.oalab.package.manager import package_manager
from openalea.core.project.manager import ProjectManager
from openalea.core.control.manager import ControlManager
from openalea.core.settings import get_openalea_tmp_dir
from openalea.oalab.config.main import MainConfig
from openalea.oalab.world.world import World
from openalea.core.singleton import Singleton
from openalea.core.path import path


class Session(object):

    """
    Session is a non graphical class that centralize managers for ...

      - application settings (:class:`~openalea.oalab.config.main.MainConfig`)
      - projects (:class:`~openalea.oalab.project.manager.ProjectManager`)
      - world (:class:`~openalea.oalab.world.world.World`)
      - interpreter (see :mod:`~openalea.vpltk.shell.shell`)

    """

    __metaclass__ = Singleton
    instantiated = False

    def __init__(self):
        self._project = None
        self._is_proj = False
        self.debug_plugins = ''
        self._debug = False
        self.gui = True

        self.tmpdir = path(get_openalea_tmp_dir())

        self._config = MainConfig()
        self.extension = None

        self.applet = {}
        self.manager = {}

        self.package_manager = package_manager
        self.control_manager = ControlManager()
        self.project_manager = ProjectManager()

        self.manager['control'] = self.control_manager
        self.manager['package'] = self.package_manager
        self.manager['project'] = self.project_manager

        self.world = World()

        self.interpreter = interpreter()

        # Hack if interpreter is an object from class TerminalInteractiveShell
        if not hasattr(self.interpreter, "shell"):
            self.interpreter.shell = self.interpreter
        if hasattr(self.interpreter.shell, "events"):
            self.interpreter.shell.events.register("post_execute", self.add_to_history)
        else:
            print("You need ipython >= 2.0 to use history.")

#         self.project_manager.set_shell(self.interpreter.shell)

        self.interpreter.locals['session'] = self

        self.old_syspath = sys.path

        self.load_default()

        self.__class__.instantiated = True

    @property
    def project(self):
        """
        :return: current project if one is opened. Else return None.
        """
        return self.project_manager.cproject

    def load_config_file(self, filename, path=None):
        self._config.load_config_file(filename=filename, path=path)

    def clear(self):
        self.world.clear()
        self.control_manager.clear()

    def load_default(self):
        self.project_manager.load_default()
        self.update_namespace()

    def update_namespace(self):
        """
        Definition: Update namespace
        """
        self.interpreter.locals['world'] = self.world
        self.interpreter.locals['get_control'] = self.control_manager.control
        self.interpreter.locals['follow'] = self.control_manager.register_follower
        self.interpreter.locals['unfollow'] = self.control_manager.unregister_follower

        if self.project:
            if self.project.path.exists():
                os.chdir(self.project.path)
                sys.path.insert(0, str(self.project.path / 'lib'))
            else:
                os.chdir(self.tmpdir)
                sys.path.insert(0, str(self.tmpdir / 'lib'))
            self.interpreter.locals.update(self.project.ns)
            self.interpreter.locals['project'] = self.project
            self.interpreter.locals['Model'] = get_model
            self.interpreter.locals['data'] = self.project.path / 'data'
        else:
            # close
            sys.path = self.old_syspath

    def add_to_history(self, *args, **kwargs):
        """
        Send the last sent of history to the components that display history
        """
        from openalea.oalab.service.history import display_history
        records = self.interpreter.shell.history_manager.get_range()

        input_ = ''
        # loop all elements in iterator to get last one.
        # TODO: search method returning directly last input
        for session, line, input_ in records:
            pass
        display_history(input_)

    config = property(fget=lambda self: self._config.config)

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, enable):
        """
        If True, add some objects useful for debug in shell namespace:
            - applet: dict containing weak references to all applets
            - manager: dict containing all managers
        """
        self._debug = enable
        env = self.interpreter.locals
        if self._debug is True:
            env['manager'] = self.manager
            env['applet'] = self.applet
        else:
            for varname in ('applet', 'manager'):
                if varname in env:
                    del env[varname]
