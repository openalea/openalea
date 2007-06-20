# -*-python-*-
#-------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2005-2007 INRIA - CIRAD - INRA  
#
#       File author(s): 
#               Christophe Pradal <christophe.prada@cirad.fr>
#               Pierre Barbier de Reuille <pierre.barbier@sophia.inria.fr>
#               Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#--------------------------------------------------------------------------------

__doc__ = """
This module add some facilities to simplify the SConscript files to
the minimum.  It contains wrapper functions that extend the SCons
environment and abstract the operating system.

Each function defines or populate global aliases like build or install.
"""

__license__ = "Cecill-C"
__revision__ = "$Id$"

import os

#from path import path
from SCons.Script.SConscript import SConsEnvironment, DefaultEnvironmentCall
import SCons.Builder
import SCons.Action
import SCons.Node.FS

Alias = DefaultEnvironmentCall("Alias")


def ALEALibrary(env, target, source, *args, **kwds):
  """
  Build static or dynamic library depending on user flags.
  Install the build library and associated files in specific directories.
  Define 'build' and 'install' target.
  """
  if env["static"]:
    lib = env.StaticLibrary("$build_libdir/%s" % (target,), source, *args, **kwds)
  else:
    if (env['compiler'] == 'msvc') and ('8.0' in env['MSVS_VERSION']):
      kwds['SHLINKCOM'] = [env['SHLINKCOM'], 
        'mt.exe -nologo -manifest ${TARGET}.manifest -outputresource:$TARGET;2']
    lib = env.SharedLibrary("$build_libdir/%s" % (target,), source, *args, **kwds)
  # Bug on mingw with .exp
  if env["compiler"] == "mingw":
    lib = [l for l in lib if not str(l).endswith('.exp')]
  Alias("build", lib)
    
  inst_lib = env.Install("$libdir", lib)
  Alias("install", inst_lib)
  return (lib, inst_lib)

def ALEAIncludes(env, target, includes, *args, **kwds):
  """
  Install the headers in the directory .../include/mypackage
  Define 'build' and 'install' target.
  """
  inc = env.Install("$build_includedir/%s" % (target,), includes, *args, **kwds)
  env.Alias("build", inc)
  inst_inc = env.Install("$includedir/%s" % (target,), includes, *args, **kwds)
  Alias("install", inst_inc)
  return (inc, inst_inc)

# def ALEAIncludes(env, target, includes, *args, **kwds):
#   """
#   Install the headers in the directory .../include/mypackage
#   Define 'build' and 'install' target.
#   """
#   # check recursive includes for installation
#   bn = os.path.basename
#   dn = os.path.dirname 
#   pj = os.path.join
#   inc, inst_inc= [], []
#   for include in includes:
#     print include
#     d = dn(include)
#     f = bn(include)
#     inc += env.Install("$build_includedir/%s" % (pj(target,d),), f, *args, **kwds)
#     inst_inc += env.Install("$includedir/%s" % (target,), includes, *args, **kwds)
#   Alias("build", inc)
#   Alias("install", inst_inc)
#   return (inc, inst_inc)

def ALEAProgram(env, target, source, *args, **kwds):
  """
  Build a program and install it in local and system directories.
  """
  bin = env.Program("$build_bindir/%s" % (target,), source, *args, **kwds)
  Alias("build", bin)
  inst_bin = env.Install("$bindir", bin)
  Alias("install", inst_bin)
  return (bin, inst_bin)

def ALEAWrapper(env, python_dir, target, source, *args, **kwds):
  """
  Build a python wrapper and install it in a python package.
  """
  real_target = "%s/%s" % (str(env.Dir(python_dir).srcnode()), target)
  if (env['compiler'] == 'msvc') and ('8.0' in env['MSVS_VERSION']):
    kwds['SHLINKCOM'] = [env['SHLINKCOM'], 
      'mt.exe -nologo -manifest ${TARGET}.manifest -outputresource:$TARGET;2']
  if os.name == 'win32':
    SHLIBSUFFIX = '.pyd'
  else:
    SHLIBSUFFIX = env['SHLIBSUFFIX']

  wrap = env.SharedLibrary(real_target, source, 
                           SHLIBPREFIX='',SHLIBSUFFIX=SHLIBSUFFIX, 
                           *args, **kwds)

  Alias("build", wrap)
  return wrap

## def ALEAPython(env, python_dir, depends = [], *args, **kwds):
##   """
##   Install recursively python package and data.
##   """
##   p = env.Dir(python_dir).srcnode()
##   base = "$pythondir/$package_name"
##   base_py = len(path(python_dir).abspath())
##   fi = []
##   for d in depends:
##     real_d = "%s/%s" % (str(env.Dir(python_dir).srcnode()), str(d))
##     fi.append(env.Install(base, d))
##   for f in p.walk():
##     fi.append(env.Install("%s/%s" % (base, f.parent[base_py:]), str(f)))
##   Alias("install", fi)
##   return fi

def ALEAGlob(env, pattern, dir = '.'):
    import os, fnmatch, glob
    files = []
    dirs = []
    is_multidirs = False
    if '*' in dir:
        here = env.Dir('.').srcnode().abspath
        d = os.path.join(here,dir)
        dirs = filter(os.path.isdir,glob.glob(d))
        is_multidirs = True
    else: 
        here = env.Dir(dir).srcnode().abspath
        dirs = [here]

    for d in dirs: 
        for file in os.listdir(d):
            if fnmatch.fnmatch(file, pattern) :
                if is_multidirs:
                    files.append(os.path.join(os.path.basename(d), file))
                else:
                    files.append(os.path.join(dir, file))
    return files

def ALEAGlobDir(env, pattern, dir='.'):
    import os, fnmatch, glob

    here = env.Dir(dir).srcnode().abspath
    d = os.path.join(here,pattern)
    dirs = filter(os.path.isdir,glob.glob(d))
    dirs = map(lambda d: d.replace(here,dir), dirs)

    return dirs

SConsEnvironment.ALEALibrary = ALEALibrary
SConsEnvironment.ALEAIncludes = ALEAIncludes
SConsEnvironment.ALEAProgram = ALEAProgram
SConsEnvironment.ALEAWrapper = ALEAWrapper
SConsEnvironment.ALEAGlob = ALEAGlob
SConsEnvironment.ALEAGlobDir = ALEAGlobDir
##SConsEnvironment.ALEAPython = ALEAPython

