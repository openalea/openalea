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
__revision__ = "$Id$"

import os, sys, glob, re
from openalea.sconsx.config import *

from os.path import join as pj

reg  = r".*boost.*([0-9]\.[0-9][0-9]\.?[0-9]?).*"
regc = re.compile(reg)

class Boost:
    def __init__(self, config):
        self.name = self.__class__.__name__.lower()
        self.config = config
        self._default = {}
        self.__usingEgg = False

    def depends(self):
        deps = []
        if isinstance(platform, Posix):
            deps.append('pthread')
        return deps

    def default(self):
        self._default['libs_suffix'] = '$compiler_libs_suffix'
        self._default['flags'] = ''
        self._default['defines'] = ''

        isPosix = isinstance(platform, Posix)        

        print "This build is running under:", platform

        # -- lets now look for decent flags --
        self._default['flags'] = '-ftemplate-depth-100' if isPosix else ''
        self._default['defines'] = self.get_default_defines()

        # -- lets now look for decent include dirs --
        try:
            # Try to use openalea egg
            from openalea.deploy import get_base_dir
            base_dir = get_base_dir("boost")
            self._default['include'] = pj(base_dir, 'include')
            self._default['lib'] = pj(base_dir, 'lib')
            self.__usingEgg = True
        except:
            try:
                import openalea.config as conf
                self._default['include'] = conf.include_dir
                self._default['lib'] = conf.lib_dir

            except ImportError, e:                
                self._default['include'] = '/usr/include' if isPosix else pj(os.getcwd(), "include")
                self._default['lib']     = '/usr/lib' if isPosix else pj(os.getcwd(), "lib")

    def get_default_defines(self):
        return ''

    def option( self, opts):

        self.default()

        opts.AddVariables(
            PathVariable('boost_includes', 
                            'boost include files', 
                            self._default['include']),

            PathVariable('boost_lib', 
                            'boost libraries path', 
                            self._default['lib']),

            (self.name + '_flags', 
              self.name + ' compiler flags', 
              self._default['flags']),

            (self.name + '_defines', 
              self.name + ' defines', 
              self._default['defines']),

            ('boost_libs_suffix', 
              self.name + ' library suffix name like -vc80-mt or -gcc', 
              self._default['libs_suffix'])
      )


    def update(self, env):
        """ Update the environment with specific flags """

        env.AppendUnique(CPPPATH=[env['boost_includes']])
        env.AppendUnique(LIBPATH=[env['boost_lib']])
        env.Append(CPPDEFINES='$%s_defines'%(self.name,))
        env.Append(CPPFLAGS='$%s_flags'%(self.name,))

        #boost > 1.43 changed naming scheme.
        #get version, from user boost or system
        if not self.__usingEgg:
            boostInc = env['boost_includes']
            versionInInc = boostInc.count("-") > 0
            if versionInInc:
                version = boostInc.split("-")[1]
            else:
                boostLibs = glob.glob("/usr/lib/*boost*.so*")
                version   = None
                #find versions in there
                for lib in boostLibs:
                    res = regc.search(lib)
                    if res and len(res.groups()):
                        version = res.groups()[0]
                        break                
        #get version, from egg
        else:
            from openalea.deploy import get_metainfo
            version = get_metainfo("boost", "version").replace(".", "_")
            
        underScores = version.count("_")
        print "we foudn this version:", version, underScores
        if underScores == 1:
            maj, min = map(int, version.split("_"))
            patch = 0
        elif underScores == 2:
            maj, min, patch = map(int, version.split("_"))

        if maj >= 1 and min >= 43 and (env['compiler'] == 'mingw' or platform==Cygwin):            
            boost_name= self.name + env['boost_libs_suffix'] + "-" + version +".dll"
        else:
            boost_name= self.name + env['boost_libs_suffix']
        env.AppendUnique(LIBS=[boost_name])


    def configure(self, config):
        return



