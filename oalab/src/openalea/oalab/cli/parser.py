# -*- coding: utf-8 -*-
# -*- python -*-
#
#       Main Window class
#       VPlantsLab GUI is created here
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

__all__ = ['CommandLineParser']

import os
import argparse

from openalea.core.service.plugin import plugin_name
from openalea.core.plugin.display import list_plugins


class CommandLineParser(object):

    def __init__(self, args=None, session=None):
        if session is None:
            from openalea.oalab.session.all import Session
            session = Session()
        self.session = session

        self.parser = argparse.ArgumentParser(description='OALab Command Line')
        self.parser.add_argument('-e', '--extension', metavar='extension', type=str, default="",
                                 help='Lab extension to launch')
        self.parser.add_argument('-v', '--verbose', action='store_true', help='Display more information')
        group = self.parser.add_argument_group('Plugin development')
        group.add_argument('--list-plugins', metavar='category', type=str, default='',
                           help='List available plugin for given category. If all, list all plugins. If summary, list only categories')
        group.add_argument('--debug-plugins', metavar='category', default='',
                           help='Raise error while loading instead of passing it silently. Use "all" to debug all plugins')
        group.add_argument('--color', help='Color terminal output', action="store_true")

    def parse(self):

        args = self.parser.parse_args()
        self.session.gui = True

        if args.color:
            self.session.color_cli = True
            os.environ['OA_CLICOLOR'] = '1'

        if args.list_plugins:
            self.session.gui = False
            list_plugins(prefixes=args.list_plugins, verbose=args.verbose)

        if args.debug_plugins:
            debug = args.debug_plugins.split(',')
            if 'oalab.lab' not in debug:
                debug.append('oalab.lab')
            from openalea.core.service.plugin import PluginInstanceManager
            pim = PluginInstanceManager()
            pim.debug = debug

        self.session.extension = args.extension
        self.args = args
