# -*-python-*-
#--------------------------------------------------------------------------------
#
#        OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#--------------------------------------------------------------------------------
""" Boost.Python configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id: boost_python.py 3049 2010-11-04 15:11:28Z dbarbeau $"

import os, sys
from openalea.sconsx.config import *
from boost_base import Boost

class Boost_Thread(Boost):

    # -- reimplement this from boost_base.Boost --
    def get_default_flags(self):
        isPosix = isinstance(platform, Posix)
        return ' -ftemplate-depth-100 ' if isPosix else ''


    # -- reimplement this from boost_base.Boost --
    def configure(self, config):
        if not config.conf.CheckCXXHeader('boost/thread.hpp'):
            print "Error: boost.thread headers not found."
            sys.exit(-1)


def create(config):
    " Create boost tool "
    boost = Boost_Thread(config)

    deps= boost.depends()
    for lib in deps:
        config.add_tool(lib)

    return boost

