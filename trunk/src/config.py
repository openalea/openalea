#!/usr/bin/python
# AMAPmod SCons build script
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: GPL

import os, sys
import string
import environ

import SCons.Util
import SCons.Tool
import SCons.Environment
import SCons.SConf
import SCons.Builder
from SCons.Util import WhereIs
import SCons.Node.FS
import SCons.Options

# SCons shorthand mappings
Environment= SCons.Environment.Environment
SConf= SCons.SConf.SConf
Dir= SCons.Node.FS.Dir
File= SCons.Node.FS.File
Builder= SCons.Builder.Builder
Tool= SCons.Tool.Tool
Split= SCons.Util.Split
Options= SCons.Options.Options
PathOption= SCons.Options.PathOption
BoolOption= SCons.Options.BoolOption
pj= os.path.join

#----------------------------------
# Errors

class ToolNotFound( UserWarning ): 
    pass

class CircularDependency( Exception ):
    pass

#----------------------------------
# Utils

def import_tool( name, import_dir ):

    old_syspath= sys.path

    if tool_path not in sys.path: 
        sys.path.insert( 0, tool_path )
    
    sys.path= import_dir + sys.path

    try:
        mod= __import__( name )
    except ImportError:
        sys.path= old_syspath
        raise ToolNotFound( name )

    sys.path= old_syspath

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
   return os.path.dirname( __file__ )

#---------------------------------------
# Method to compile bison and flex files

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


#----------------------------------
# Path setting

tool_path= os.path.join( getLocalPath() , 'tools' )
sys.path= [tool_path] + sys.path

#----------------------------------
# Platform

class Platform( object ):
   def __init__( self ):
      self.name= ""

class Posix( Platform ):
   def __init__( self ):
      self.name= "posix"

class Linux( Posix ):
   def __init__( self ):
      self.name= "linux"

class Irix( Posix ):
   def __init__( self ):
      self.name= "irix"

class Darwin( Posix ):
   def __init__( self ):
      self.name= "darwin"

class Win32( Platform ):
   def __init__( self ):
      self.name= "win32"

# factory
def GetPlatform():
   osname = os.name.lower()
   pfname = sys.platform.lower()

   if osname == "posix" :
     if pfname.find( "linux" ) >= 0 :
         return Linux()
     elif pfname.find( "darwin" ) >= 0 :
         return Darwin()
     elif pfname.find( "irix" ) >= 0 :
         return Irix()
     else:
         return Posix()
   elif(osname == "nt" and pfname== "win32"):
     return Win32()
   else:
     raise "Unknown Platform (%s,%s)"%(osname,pfname)

# Create a static instance ... 
# ( very pythonic way, isn't it? )
platform= GetPlatform()

# User Configuration class

default_tools= [ 'compiler', 'builddir', 'install' ]

class Config( object ):

    def __init__( self, tools= [], dir= [] ):
        self.init_tools= default_tools + tools
        self.tools= []
        self.tools_dict= {}
        self._walk= []
        if not dir: 
            self.dir= [ os.getcwd() ]
        self.custom_tests= { }

        for t in self.init_tools:
            self.add_tool( t )


    def add_tool( self, tool ):
        """ Add a tool. """

        if tool in self.tools:
            return

        if tool in self._walk:
            raise CircularDependencies( tool )

        self._walk.append( tool )

        mod= import_tool( tool, self.dir )
        t= mod.create( self )

        self._walk.pop()
        self.tools.append( t )


    def __str__( self ):
        return str([ t.name for t in self.tools ])

    def Options( self, *args, **kwds ):
        """
        Add each tool options
        """

        opts= Options( *args, **kwds )
        self.UpdateOptions( opts )

        return opts

    def UpdateOptions( self, opts ):
        for tool in self.tools:
            tool.option( opts )


    def Configure( self, env ):
        """
        Configure each tools
        """

        # Create Configure
        self.conf= SConf( env, self.custom_tests )

        for tool in self.tools:
            tool.configure( self )

        env= self.conf.Finish()
        return env


    def Update( self, env ):
        """
        Update the environment for each tools.
        """

        # Create Configure
        for tool in self.tools:
            tool.update( env )


class ALEAConfig( Config ):
   def __init__( self, package_name, *args, **kwds ):
      Config.__init__( self, *args, **kwds )
      self.package_name = package_name

   def Update( self, env ):
      Config.Update( self, env )
      env[ "package_name" ] = self.package_name

