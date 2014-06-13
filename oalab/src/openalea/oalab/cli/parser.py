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

import argparse
from openalea.oalab.session.all import Session

class CommandLineParser(object):
    def __init__(self, args, session=None):
        if session is None:
            session = Session()
        self.session = session
        
        self.parser = argparse.ArgumentParser(description='OALab Command Line')
        self.parser.add_argument('-e', '--extension', metavar='extension', type=str, default="full",
                                 help='Lab extension to launch')
        self.parser.add_argument('--list-plugin-categories', action='store_true',
                                 help='List plugin categories used in OpenAleaLab')
        self.parser.add_argument('--list-plugins', metavar='category', type=str, default='',
                                 help='List available plugin for given category')
        self.parser.add_argument('--debug-plugins', metavar='category', default='',
                                 help='Raise error while loading instead of passing it silently')

        args = self.parser.parse_args()
        self.session.gui = True


        if args.list_plugin_categories:
            self.session.gui = False
            from openalea.vpltk.plugin import iter_groups
            for category in sorted(iter_groups()):
                if category.startswith('oalab') or category.startswith('vpltk'):
                    print '  - %s' % category

        if args.list_plugins:
            self.session.gui = False
            import pkg_resources
            print 'Plugins for category %r' % args.list_plugins
            for ep in pkg_resources.iter_entry_points(args.list_plugins):
                print '  -', ep

        if args.debug_plugins:
            self.session.debug_plugins = args.debug_plugins


        self.session.extension = args.extension
