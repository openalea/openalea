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

import warnings
from openalea.vpltk.shell.shell import get_interpreter_class
from openalea.vpltk.project.manager import ProjectManager
from openalea.oalab.config.main import MainConfig
from openalea.oalab.world.world import World


class Session(object):
    """
    Session is a non graphical class that centralize managers for ...

      - application settings (:class:`~openalea.oalab.config.main.MainConfig`)
      - projects (:class:`~openalea.oalab.project.manager.ProjectManager`)
      - world (:class:`~openalea.oalab.world.world.World`)
      - interpreter (see :mod:`~openalea.vpltk.shell.shell`)

    """
    def __init__(self):
        self._project = None
        self._is_proj = False

        self._config = MainConfig()
        self.extension = None

        self.project_manager = ProjectManager()

        self.world = World()

        interpreter_class = get_interpreter_class()
        self.interpreter = interpreter_class()
        self.interpreter.shell.events.register("post_execute", self.add_to_history)

        self.interpreter.locals['session'] = self
        self.debug_plugins = ''

        self.gui = True

    @property
    def project(self):
        """
        :return: current project if one is opened. Else return None.
        """
        return self._project

    @project.setter
    def project(self, project):
        """
        Set the project
        """
        self._project = project

    def current_is_project(self):
        """
        :return: True if current document is a project
        """
        return bool(self._is_proj)

    def get_project(self):
        warnings.warn('Deprecated get_project -> project')
        return self.project

    def load_config_file(self, filename, path=None):
        self._config.load_config_file(filename=filename, path=path)

    def update_namespace(self):
        """ Stub method from allwidgets. CPL: TODO

        Definition: Update namespace
        """
        if self.project:
            self.interpreter.locals['project'] = self.project
            self.interpreter.locals['Model'] = self.project.model
        self.interpreter.locals['scene'] = self.world
        self.interpreter.locals['world'] = self.world

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

    config = property(fget=lambda self:self._config.config)


