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

from openalea.core.service.plugin import plugin_implementation, plugin_name


def print_plugin_name(plugin):
    interface = plugin_implementation(plugin)
    if interface:
        print '%s (implements: %s)' % (plugin_name(plugin), interface)
    else:
        print plugin_name(plugin)


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
            from openalea.core.plugin.manager import PluginManager
            pm = PluginManager()
            self.session.gui = False
            import pkg_resources
            from openalea.core.plugin import iter_groups

            if args.list_plugins in ['summary', 'all']:
                prefixes = ['oalab', 'vpltk', 'openalea']
            else:
                prefixes = [args.list_plugins]
            for category in sorted(iter_groups()):
                match = False
                for prefix in prefixes:
                    if category.startswith(prefix):
                        match = True
                        break
                if match:
                    eps = [ep for ep in pkg_resources.iter_entry_points(category)]
                    if args.list_plugins == 'summary':
                        print '\n\033[91m%s\033[0m (%d plugins)' % (category, len(eps))
                        for ep in eps:
                            parts = [str(s) for s in (ep.module_name, ep.name)]
                            identifier = ':'.join(parts)
                            print '  - %s \033[90m%s (%s)\033[0m' % (ep.name, identifier, ep.dist.egg_name())
                    else:
                        print '\033[44m%s\033[0m' % category
                        UNDEF = 'Not defined'
                        plugin_groups = {UNDEF: []}
                        for plugin in pm.plugins(category):
                            interface = plugin_implementation(plugin)
                            if interface:
                                plugin_groups.setdefault(interface, []).append(plugin)
                            else:
                                plugin_groups[UNDEF].append(plugin)
                        for group, plugins in plugin_groups.items():
                            if not plugins:
                                continue
                            print '  implements: \033[91m%s\033[0m' % group
                            for plugin in plugins:
                                print '    - \033[93m%s \033[90m%s:%s\033[0m' % (plugin_name(plugin), plugin.__module__, plugin.__name__)
                                if args.verbose:
                                    print '        plugin: %s, egg: %s\n        path: %s' % (
                                        ep.name, ep.dist.egg_name(), ep.dist.location)

                        print
                        print

        if args.debug_plugins:
            debug = args.debug_plugins.split(',')
            if 'oalab.lab' not in debug:
                debug.append('oalab.lab')
            from openalea.core.service.plugin import PluginInstanceManager
            pim = PluginInstanceManager()
            pim.debug = debug

        self.session.extension = args.extension
        self.args = args
