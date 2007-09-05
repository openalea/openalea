# -*- python -*-
#--------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Pierre Barbier de Reuille <pierre.barbier@sophia.inria.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#--------------------------------------------------------------------------------

__license__= "Cecill-C"
__revision__="$Id$"

__doc__=""" See OpenAlea WebSite / Packages / SConsX """


import os, sys
import string
pj = os.path.join

from SCons.Script import *
from SCons.Options import PathOption, BoolOption, EnumOption, Options
from SCons.Util import Split, WhereIs
from SCons.Tool import Tool
from SCons.SConf import SConf
from SCons.Environment import Environment
from SCons.Builder import Builder
from SCons.Node.FS import Dir, File


#--------------------------------------------------------------------------------
# Errors

class ToolNotFound(UserWarning): 
    pass

class CircularDependency(Exception):
    pass



#--------------------------------------------------------------------------------
# Utilitaries

def import_tool(name, import_dir):
    """
    Import a module based on its name from a list of directories.
    """
    old_syspath = sys.path

    if tool_path not in sys.path: 
        sys.path.insert(0, tool_path)
    
    sys.path = import_dir + sys.path

    try:
        mod = __import__(name)
    except ImportError:
        sys.path = old_syspath
        raise ToolNotFound(name)

    sys.path = old_syspath

    return mod

   
    

def exist(s,path):
   """ Test if the file s exist in the path """

   files= os.listdir(path)
   for f in files:
      if string.find(f,s) != -1:
         return True
   return False


def getLocalPath():
   """ Return the absolute path of this package """
   return os.path.dirname(__file__)


#--------------------------------------------------------------------------------
# Global Path settings

tool_path = os.path.join(getLocalPath() , 'tools')
sys.path = [tool_path] + sys.path


#--------------------------------------------------------------------------------
# Method to build bison and flex files for AMAPmod software

def BisonFlex(env, bison, flex, prefix):
  """ Smart autoscan function. """

  LEXFLAGS = env.get("LEXFLAGS")[:]
  YACCFLAGS = env.get("YACCFLAGS")[:]

  if prefix :
     LEXFLAGS += ["-P"+prefix]
     YACCFLAGS +=  ["-p "+prefix]

  targets=[]
  bison_ext= ".hpp"
  if not env.get("BISON_HPP"):
    bison_ext = ".cpp.h"

  (bison_name, ext)= os.path.splitext(bison)
  h= env.CXXFile(source= bison,
                 target= [bison_name+".cpp", bison_name + bison_ext],
                 LEXFLAGS=LEXFLAGS,
                 YACCFLAGS=YACCFLAGS)
  targets.append(h[0])

  (flex_name, ext) = os.path.splitext(flex)
  cpp = env.CXXFile(source=flex,
                    LEXFLAGS=LEXFLAGS,
                    YACCFLAGS=YACCFLAGS)

  targets.append(cpp)

  return targets



#----------------------------------
# Platform class

class Platform(object):
   def __init__(self):
      self.name= ""

class Posix(Platform):
   def __init__(self):
      self.name= "posix"

class Linux(Posix):
   def __init__(self):
      self.name= "linux"

class Irix(Posix):
   def __init__(self):
      self.name= "irix"

class Cygwin(Posix):
   def __init__(self):
      self.name= "cygwin"

class Darwin(Posix):
   def __init__(self):
      self.name= "darwin"

class Win32(Platform):
   def __init__(self):
      self.name= "win32"


def GetPlatform():
    """
    Factory function returning the correct platform instance.
    """
    osname = os.name.lower()
    pfname = sys.platform.lower()

    if osname == "posix" :
        if pfname.find("linux") >= 0 :
            return Linux()
        elif pfname.find("cygwin") >= 0 :
            return Cygwin()
        elif pfname.find("darwin") >= 0 :
            return Darwin()
        elif pfname.find("irix") >= 0 :
            return Irix()
        else:
            return Posix()
    elif(osname == "nt" and pfname== "win32"):
        return Win32()
    else:
        raise "Unknown Platform (%s,%s)" % (osname,pfname)

# Create a static instance ... 
# (very pythonic way, isn't it?)

platform= GetPlatform()


#--------------------------------------------------------------------------------
# User Configuration class

default_tools= ['compiler', 'builddir']

class Config(object):

    def __init__(self, tools=[], dir=[]):

        self.init_tools = default_tools + tools
        self.tools = []
        self.tools_dict = {}
        self._walk = []
        if not dir: 
            self.dir = [os.getcwd()]
        self.custom_tests = { }

        for t in self.init_tools:
            self.add_tool(t)


    def add_tool(self, tool):
        """
        Add a specific tool and its dependencies recursively in the tool set.
        Check the circular dependencies.
        """

        if tool in self.tools:
            return

        if tool in self._walk:
            raise CircularDependencies(tool)

        self._walk.append(tool)

        # Try to import SConsX tool
        try:
            mod = import_tool(tool, self.dir)
            t = mod.create(self)
        except:
            # Try to import EGG LIB
            mod = import_tool("egglib", self.dir)
            t = mod.create(tool, self)
            
            
        self._walk.pop()
        self.tools.append(t)


    def __str__(self):
        return str([t.name for t in self.tools])


    def Options(self, *args, **kwds):
        """
        Add each tool options
        """
        opts = Options(*args, **kwds)
        self.UpdateOptions(opts)

        return opts


    def UpdateOptions(self, opts):
        for tool in self.tools:
            tool.option(opts)


    def Configure(self, env):
        """
        Configure each tools
        """
        # Create Configure
        self.conf = SConf(env, self.custom_tests)

        for tool in self.tools:
            tool.configure(self)

        env = self.conf.Finish()
        return env


    def Update(self, env):
        """
        Update the environment for each tools.
        """

        # Create Configure
        for tool in self.tools:
            tool.update(env)


#--------------------------------------------------------------------------------
# Specific OpenAlea facilities.

class ALEAConfig(Config):
    def __init__(self, package_name, *args, **kwds):
        Config.__init__(self, *args, **kwds)
        self.package_name = package_name

    def Update(self, env):
        Config.Update(self, env)
        env["package_name"] = self.package_name


def ALEAEnvironment(conf, *args, **kwds):
    if 'options' in kwds:
        opts= kwds['options']
        conf.UpdateOptions(opts)
    else:
        opts= conf.Options(*args, **kwds)
    env= Environment(options=opts)
    conf.Update(env)
    env.Prepend(CPPPATH='$build_includedir')
    env.Prepend(LIBPATH='$build_libdir')
    return env
