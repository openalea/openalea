# -*-python-*-

# AMAPmod SCons build script
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: CECILL-C

#from path import path
from SCons.Script.SConscript import SConsEnvironment, DefaultEnvironmentCall
import SCons.Builder
import SCons.Action
import SCons.Node.FS

Alias = DefaultEnvironmentCall( "Alias" )


def ALEALibrary( env, target, source, *args, **kwds ):
  if env[ "static" ]:
    lib = env.StaticLibrary( "$build_libdir/%s" % ( target, ), source, *args, **kwds )
  else:
    lib = env.SharedLibrary( "$build_libdir/%s" % ( target, ), source, *args, **kwds )
  Alias( "build", lib )
  # Bug on mingw with .exp
  if env["compiler"]== "mingw":
    lib= [l for l in lib if not str(l).endswith('.exp') ]
    
  inst_lib = env.Install( "$libdir", lib )
  Alias( "install", inst_lib )
  return ( lib, inst_lib )

def ALEAIncludes( env, target, includes, *args, **kwds ):
  inc = env.Install( "$build_includedir/$package_name", includes, *args, **kwds )
  Alias( "build", inc )
  inst_inc = env.Install( "$includedir/$package_name", includes, *args, **kwds )
  Alias( "install", inst_inc )
  return ( inc, inst_inc )

def ALEAProgram( env, target, source, *args, **kwds ):
  bin = env.Program( "$build_bindir/%s" % ( target, ), source, *args, **kwds )
  Alias( "build", bin )
  inst_bin = env.Install( "$bindir", bin )
  Alias( "install", inst_bin )
  return ( bin, inst_bin )

def ALEAWrapper( env, python_dir, target, source, *args, **kwds ):
  real_target = "%s/%s" % ( str( env.Dir( python_dir ).srcnode() ), target )
  wrap = env.SharedLibrary( real_target, source, SHLIBPREFIX='', *args, **kwds )
  Alias( "build", wrap )
  return wrap

## def ALEAPython( env, python_dir, depends = [], *args, **kwds ):
##   p = env.Dir( python_dir ).srcnode()
##   base = "$pythondir/$package_name"
##   base_py = len( path( python_dir ).abspath() )
##   fi = []
##   for d in depends:
##     real_d = "%s/%s" % ( str( env.Dir( python_dir ).srcnode() ), str( d ) )
##     fi.append( env.Install( base, d ) )
##   for f in p.walk():
##     fi.append( env.Install( "%s/%s" % ( base, f.parent[ base_py: ] ), str( f ) ) )
##   Alias( "install", fi )
##   return fi

SConsEnvironment.ALEALibrary = ALEALibrary
SConsEnvironment.ALEAIncludes = ALEAIncludes
SConsEnvironment.ALEAProgram = ALEAProgram
SConsEnvironment.ALEAWrapper = ALEAWrapper
##SConsEnvironment.ALEAPython = ALEAPython

