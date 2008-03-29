# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2008 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

import os, sys
from optparse import OptionParser

from openalea.core.pkgmanager import PackageManager



def show_help(argv):
    """ -h (--help) option """















def main():
    """ Parse optiosn """

        # options
    parser = OptionParser()
    parser.add_option( "-h", dest="name",
                       help="Query package or component",
                       default=None)

    (options, args)= parser.parse_args()

    print options, args



if(__name__ == "__main__"):
    main()
