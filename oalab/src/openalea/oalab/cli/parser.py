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
from openalea.oalab.session.all import Session


def print_plugin_name(ep):
    try:
        name = ep.load().name
    except ImportError:
        pass
    except AttributeError:
        print '  - %s (%s)' % (ep.name, ep)
    else:
        print '  - %s (%s)' % (name, ep)


class CommandLineParser(object):

    def __init__(self, args, session=None):
        if session is None:
            session = Session()
        self.session = session

        self.parser = argparse.ArgumentParser(description='OALab Command Line')
        self.parser.add_argument('-e', '--extension', metavar='extension', type=str, default="default",
                                 help='Lab extension to launch')
        group = self.parser.add_argument_group('Plugin development')
        group.add_argument('--list-plugins', metavar='category', type=str, default='',
                           help='List available plugin for given category. If all, list all plugins. If summary, list only categories')
        group.add_argument('--debug-plugins', metavar='category', default='',
                           help='Raise error while loading instead of passing it silently. Use "all" to debug all plugins')
        group.add_argument('--color', help='Color terminal output', action="store_true")

        args = self.parser.parse_args()
        self.session.gui = True

        if args.color:
            self.session.color_cli = True
            os.environ['OA_CLICOLOR'] = '1'

        if args.list_plugins:
            self.session.gui = False
            import pkg_resources
            from openalea.core.plugin import iter_groups

            if args.list_plugins in ['summary', 'all']:
                for category in sorted(iter_groups()):
                    if category.startswith('oalab') or category.startswith('vpltk'):
                        eps = [ep for ep in pkg_resources.iter_entry_points(category)]
                        if args.list_plugins == 'all':
                            print '\033[91m%s\033[0m' % category
                            print
                            for ep in eps:
                                print_plugin_name(ep)
                            print
                            print
                        else:
                            print '  - \033[91m%s\033[0m (%d plugins)' % (category, len(eps))

            elif args.list_plugins:
                print 'Plugins for category %r' % args.list_plugins
                for ep in pkg_resources.iter_entry_points(args.list_plugins):
                    print_plugin_name(ep)

        if args.debug_plugins:
            debug = args.debug_plugins.split(',')
            if 'oalab.lab' not in debug:
                debug.append('oalab.lab')
            self.session.plugin_manager.debug = debug

        self.session.extension = args.extension
