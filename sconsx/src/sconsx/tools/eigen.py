# -*-python-*-
#--------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
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
""" Eigen configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id$"


import os, sys, platform
from openalea.sconsx.config import *


class Eigen:
   def __init__(self, config):
      self.name = 'eigen'
      self.config = config
      self._default = {}


   def default(self):
       system = platform.system().lower()
       if system == "linux":
           dist, number, name = platform.linux_distribution()
           if dist.lower() == "ubuntu":
               inc_path = "/usr/include/eigen"
           else:
               warnings.warn("Currently unhandled system : " + dist + ". Implement me please.")
       else:
            warnings.warn("Currently unhandled system : " + system + ". Implement me please.")

      self._default['include'] = inc_path

   def option( self, opts):
      self.default()
      opts.AddVariables(
         PathVariable('eigen_includes', 'eigen include files',
                     self._default['include']),
     )

   def update(self, env):
      """ Update the environment with specific flags """
      env.AppendUnique(CPPPATH=[env['eigen_includes']])

   def configure(self, config):
      if not config.conf.CheckCHeader('Eigen/Core'):
         print """Error: Eigen headers not found !!!
         Please install eigen and start again."""
         sys.exit(-1)


def create(config):
   " Create eigen tool "
   eigen = Eigen(config)

   return eigen

