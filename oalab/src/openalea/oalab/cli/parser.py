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
        self.parser.add_argument('-e', '--extension', metavar='extension', type=str, default="mini",
                                 help='Lab extension to launch')
        self.parser.add_argument('--list-interfaces', action='store_true',
                                 help='List available interfaces')
        self.parser.add_argument('--list-implementations', action='store_true',
                                 help='List available implementations')
        args = self.parser.parse_args()

        if args.list_interfaces:
            from openalea.vpltk.catalog import list_interfaces
            list_interfaces()

        if args.list_implementations:
            from openalea.vpltk.catalog import list_implementations
            list_implementations()

        self.session.extension = args.extension
