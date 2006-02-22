#!/usr/bin/python
# AMAPmod SCons build script
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: GPL

import os, sys, string, re

import SCons.Defaults
import SCons.Util
import SCons.Tool
import SCons.Environment
import SCons.SConf
import SCons.Builder
from SCons.Util import WhereIs
import SCons.Node.FS

# SCons shorthand mappings
Environment= SCons.Environment.Environment
Configure= SCons.SConf.SConf
Dir= SCons.Node.FS.default_fs.Dir
File= SCons.Node.FS.default_fs.File
Builder= SCons.Builder.Builder
Tool= SCons.Tool.Tool
Split= SCons.Util.Split
pj= os.path.join

#abstract base class
class Platform:
    def __init__(self,name):
        self.name = name
        self.dict= {}

    def GetDefaultOptions(self, dir):
        self.dir= dir
        self.Prefix()
        self.BuildDirDefault()

        self.BoostDefault()
        self.QTDefault()
        self.BisonDefault()
        self.FlexDefault()
        self.GnuplotDefault()
        self.ReadlineDefault()
        self.TermcapDefault()
        
        return self.dict

    def BuildDirDefault(self):
        """ Set default Directories for local compilation & installation"""
        self.dict[ "build_prefix" ]= pj( self.dir, "build-" + self.name ) 

    def ReadlineDefault( self ):
        pass

    def TermcapDefault( self ):
        pass

    def SetCompilerFlags(self, env):
        "appends platform specific flags to environment"
        pass

    def SetPythonInfo(self, env):
        "appends python params to environment"
        pass

    def SetBoostInfo(self, env):
        "appends boost params to environment"
        pass


class PosixPlatform(Platform):

    def Prefix( self ):
        self.dict[ "prefix" ]= "/usr/local"

    def ReadlineDefault( self ):
        self.dict[ 'readline_includes' ]= '/usr/include'
        self.dict[ 'readline_lib' ]= '/usr/lib'

    def TermcapDefault( self ):
        self.dict[ 'termcap_includes' ]= '/usr/include'
        self.dict[ 'termcap_lib' ]= '/usr/lib'

    def BisonDefault( self ):
        self.dict[ 'bison_bin' ]= '/usr/bin'

    def FlexDefault( self ):
        self.dict[ 'flex_bin' ]= '/usr/bin'
        self.dict[ 'flex_lib' ]= '/usr/lib'

    def GnuplotDefault( self ):
        self.dict[ 'gnuplot_bin' ]= '/usr/bin'

    def QTDefault( self ):
        qtdir= os.getenv( "QTDIR" )
        if not qtdir:
            qtdir= '/usr/lib'
        self.dict[ 'QTDIR' ]= qtdir

    def BoostDefault( self ):
        self.dict[ "boost_includes" ]= '/usr/include'
        self.dict[ "boost_lib" ]= '/usr/lib'

    def SetCompilerFlags(self, env):
        pass;

    def SetPythonInfo(self, env):
        (maj,min,d,d,d)=sys.version_info
        dname = "%s/include/python%d.%d"%(sys.prefix,maj,min)
        env.Append(CPPPATH = dname)
        lib= "%s/lib/python%d.%d/config"%(sys.prefix,maj,min)
        env.Append(LIBPATH = lib)

    def SetBoostInfo(self, env):
        "appends boost params to environment"

        boost_prefix=  env[ "boost_includes" ]
        if not boost_prefix:
         s="""
         Warning !!! Boost directory not defined !
         Please edit SConstruct file and change the boost variable. """

         print s
         exit(-1)

        env.Append(CPPPATH = boost_prefix)

        libdir= env["boost_lib"]
        env.Append(LIBPATH = libdir)

        env.Append(LIBS="boost_python")

        flags=Split("-ftemplate-depth-100 -DBOOST_PYTHON_DYNAMIC_LIB")
        env.Append(CXXFLAGS=flags)
        env["RPATH"]=env["RPATH"]+[libdir]
        # to do: turn this elegantly

        # pthread needed by boost_python
        # TODO: Add to options
        pthread_dir= "/lib/"
        env.Append(LIBPATH = pthread_dir)
        env.Append(LIBS="pthread")

        self.SetPythonInfo(env)


# linux specific
class LinuxPlatform(PosixPlatform):
    def SetCompilerFlags(self, env):
        PosixPlatform.SetCompilerFlags(self,env)
        env.Append(CPPFLAGS = "-DSYSTEM_IS__Linux")

        CXX = WhereIs('g++3') or 'g++'
        LINK = CXX
        if env["warnings"]:
            CXXFLAGS = ['-Wall']
        LINKFLAGS = []
        LIBPATH = [env["build_libdir"]]

        # Todo check GLDIR
        GLDIR="/usr/X11R6"
        LIBPATH+= [GLDIR+"/lib"]

        LIBS = Split("""glut GL GLU""")

        if env["debug"]:
           CXXFLAGS.extend(['-g'])
        else:
           CXXFLAGS.extend(['-DNDEBUG', '-O2'])

        # add rpath support for shared library
        '''
        if not env["static"]:
            env["RPATHPREFIX"] = "-Wl,-rpath "
            env["RPATH"] = [ LIBPATH[0] ]
            env["RPATHSUFFIX"] = ""
            env["_RPATHFLAGS"] = " $(${_concat(RPATHPREFIX, RPATH, RPATHSUFFIX, __env__)}$)"
        '''

        env.Replace(CXX = CXX)
        env.Replace(LINK = LINK)
        env.Replace(CXXFLAGS = CXXFLAGS)
        env.Replace(LINKFLAGS = LINKFLAGS)
        env.Replace(LIBS = LIBS)
        env.Replace(LIBPATH=LIBPATH)
        env.Append(RPATH=env["build_libdir"])
#        env.Append(LIBPATH=env["_RPATHFLAGS"])


# osx specific
class DarwinPlatform(PosixPlatform):
    def SetCompilerFlags(self, env):
        PosixPlatform.SetCompilerFlags(self,env)
        env.Append(CPPFLAGS = "-DSYSTEM_IS__OSX")

# sgi specific
class IrixPlatform(PosixPlatform):
    def SetCompilerFlags(self, env):
        PosixPlatform.SetCompilerFlags(self, env)
        env.Append(CPPFLAGS = "-DSYSTEM_IS__IRIX")

# win32 specific
class Win32Platform(Platform):

   def Prefix( self ):
       self.dict[ "prefix" ]= "C:"

   def BisonDefault( self ):
       self.dict[ 'bison_bin' ]= pj( 'C:', 'Tools' )

   def FlexDefault( self ):
       self.dict[ 'flex_bin' ]= pj( 'C:', 'Tools', 'Bin' )
       self.dict[ 'flex_lib' ]= pj( 'C:', 'Tools', 'Bin' )

   def GnuplotDefault( self ):
       # TODO
       self.dict[ 'gnuplot_bin' ]= 'C:'

   def QTDefault( self ):
       qtdir= os.getenv( "QTDIR" )
       if not qtdir:
          qtdir= pj( 'C:', 'QT' )
       self.dict[ 'QTDIR' ]= qtdir

   def BoostDefault( self ):
       # TODO
       self.dict[ "boost_includes" ]= 'C:'
       self.dict[ "boost_lib" ]= 'C:'


   def SetCompilerFlags(self, env):
       env.Append(CPPFLAGS = "-D_WIN32")

   def SetPythonInfo(self, env):
       dname = "%s/include/"%(sys.prefix)
       env.Append(CPPPATH = Dir(dname))

   def SetBoostInfo(self, env):
       "appends boost params to environment"
       pass;

#---------------------------------------------------------------------------#
# factory

def GetPlatform():
    import sys, os, string

    osname = string.lower(os.name)
    pfname = string.lower(sys.platform)

    if(osname == "posix"):
        if(string.find(pfname,"linux")>=0):
            return LinuxPlatform("linux")
        elif(string.find(pfname,"darwin")>=0):
            return DarwinPlatform("darwin")
        elif(string.find(pfname,"irix")>=0):
            return IrixPlatform("irix")
        else:
            return PosixPlatform(pfname)
    elif(osname == "nt" & pfname== "win32"):
        return Win32Platform("win32")
    else:
        raise "Unknown Platform (%s,%s)"%(osname,pfname)

#---------------------------------------------------------------------------#

# todo: add a class to compute an environment depending on platform
def BuildDefaultEnvironment( ):
   "Builds a base environment for other modules to build on."

   env = Environment( ENV = os.environ,
                      CPPPATH = ["$build_dir","."],
                      CXXFILESUFFIX=[".cpp"] )

   return env

#---------------------------------------------------------------------------#

# todo: add a class to compute an environment depending on platform
def BuildBaseEnvironment( env ):
   "Builds a base environment for other modules to build on."

   platform= GetPlatform()
   platform.SetCompilerFlags( env )
   return env

#---------------------------------------------------------------------------#

def BoostEnvironment( env ):
   "Add Boost configuration to env."

   platform= GetPlatform()

   boost= env.Copy()
   platform.SetBoostInfo( boost )

   return boost

#---------------------------------------------------------------------------#

def BuildConfig( env ):
   "Check configuration and update environment"

   amap= AMAPmodConfig(env)
   amap.configure()

   return amap.env

#---------------------------------------------------------------------------#

def exist(s,path):
   files= os.listdir(path)
   for f in files:
      if string.find(f,s) != -1:
         return True
   return False

class AMAPmodConfig:

  def __init__( self, env ):
    self.env= env
  #     self.conf= Configure(self.env,log_file=None)

  def updateOptions(self):
    """ Update options for modules dependencies """
    o= self.env
    env= self.env

    if o["with_treematching"] or o["with_mtg"]:
       o["with_mtg"]= True
       o["with_treematching"]= True
    if o["with_mtg"] or o["with_msvoxel"] or o["with_geomext"]:
       o["with_geom"]= True

#X     if o["with_stat"]: env.Append(CPPFLAGS = ["-DHAVE_STAT"])
#X     if o["with_geom"]: env.Append(CPPFLAGS = ["-DHAVE_GEOM"])
#X     if o["with_mtg"]: env.Append(CPPFLAGS = ["-DHAVE_MTG"])
#X     if o["with_geomext"]: env.Append(CPPFLAGS = ["-DHAVE_GEOMEXT"])
#X     if o["with_msvoxel"]: env.Append(CPPFLAGS = ["-DHAVE_MSVOXEL"])
#X     if o["with_treematching"]: env.Append(CPPFLAGS = ["-DHAVE_TREEMATCH"])

    if env["with_stattrees"]:
       env.Append(CPPFLAGS = ["-DHAVE_STAT_TREES"])
       env[ "with_boost" ]= True
    else:
       env[ "with_boost" ]= False

#X     if o["with_geom"]:
#X        geom_subdirs= Split("action appearance geometry scene util viewer")
#X        geom_dir="#src/GEOM/"
#X        geom_subdirs= map(lambda x:geom_dir+x,geom_subdirs)
#X        env.Append(CPPPATH=geom_subdirs)

  def configure(self):
    """ Check the configuration and update options """

    self.updateOptions()
    env= self.env


    #if self.options["with_geom"]:
    self.checkQT()

    self.checkGnuplot()
    self.checkLex()
    self.checkYacc()

  def checkQT(self):
   """ Use scons QT tools """
   
   env= self.env
   t= Tool('qt')
   t(self.env)
   
   # Add specific AMAPmod flags
   qtdir= env["QTDIR"]

   multithread= exist("qt-mt",pj(env["QTDIR"],"lib"))
   if multithread:
      env.Append( CPPFLAGS=["-DQT_THREAD_SUPPORT"] )
      env["QT_LIB"]=["qt-mt"]

   qgl= exist("qgl",pj(str(qtdir),"lib"))
   if qgl:
      env.AppendUnique(QT_LIB="qgl")

  def checkGnuplot(self):
    """ Check Gnuplot install """
    g= WhereIs("gnuplot")

    if not g:
      s="""
      Warning !!! Gnuplot not found !
      Please, install Gnuplot and try again.
      """
      print s
      exit( -1 )

  def checkLex(self):
    """ """
    self.env.Append( LIBS=["fl","m"] )
    t= Tool( 'lex', toolpath=["scons_util"] )
#X     t= Tool( 'lex' )
    t(self.env)


  def checkYacc(self):
    t= Tool( 'yacc', toolpath=["scons_util"] )
#X     t= Tool( 'yacc' )
    t(self.env)

    self.env.Append( YACCFLAGS="-d -v")

    if self.env.has_key("YACC"):
       bison=self.env["YACC"]
       f=os.popen(str(bison)+" --version")
       l=f.readline()
       l=l.split()
       version_text = re.compile(r"\d+.\d+").match(l[-1])
       if version_text is None:
          raise UserWarning, "Unable to retrieve bison version number"
       version= float( version_text.group(0) )
       f.close()
       if version >= 1.30:
          BISON_HPP=True
       else:
          BISON_HPP=False
       self.env.Append(BISON_HPP=BISON_HPP)
       if BISON_HPP:
          self.env.Append( CPPFLAGS=["-DBISON_HPP"] )

#---------------------------------------------------------------------------#

def BisonFlex( env, bison, flex, prefix ):
  """ Smart autoscan function. """
  
  if prefix :
     env.Append( LEXFLAGS="-P"+prefix)
     env.Append( YACCFLAGS="-p "+prefix)
  
  targets=[]
  bison_ext= ".hpp"
  if not env[ "BISON_HPP" ]:
    bison_ext= ".cpp.h"

  ( bison_name, ext )= os.path.splitext( bison )
  h= env.CXXFile( source= bison, target= [ bison_name+".cpp", bison_name + bison_ext ] )
  targets.append( h[0] )

  ( flex_name, ext )= os.path.splitext( flex )
  cpp= env.CXXFile( source= flex )
  targets.append( cpp )

  return targets


#---------------------------------------------------------------------------#


