# -*-python-*-
#--------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@inria.fr>
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


import os, sys, warnings
from openalea.sconsx.config import *

class Eigen:
   def __init__(self, config):
      self.name = 'eigen'
      self.config = config
      self._default = {}


   def default(self):
       name = str(platform)
       if isinstance(platform, Linux):
           dist = platform.distribution()
           name += " "+dist
           if dist == "ubuntu":
              inc_path = "/usr/include/eigen2/"
           else:
              inc_path = "/usr/include/"
       else:
         warnings.warn("Currently unhandled system : " + name + ". Implement me please.")

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

