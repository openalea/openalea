


Technical Documentation
=======================

SConsX provides a set of tools with, for each tools, a set of options with default values depending on the OS and on the value of previous parameters.

Options may be set on a file (e.g. options.py) or via command line arguments. Each tool may also provide a configure method to test the validity of the configuration.

The Config object
-----------------

SConsX add the Config class to SCons.

A Config object maintains a list of tools in a Directed Acyclic Graph. It checks if there is no cyclic dependencies between the tools. If a tool depends on an other tool, it will add automagically its dependencies.

When a method is called on a Config instance, the method will be called on each tools.
Config methods


Config Constructor
------------------

To create a specific configuration, just create a Config object with the list of require tools::

    conf = config.Config([ 'install', 'boost.python'])

In this example, boost.python will add python tool to the list of tools.

Some tools are added by default at the creation, i.e. the compiler tool and the builddir tool.

add_tool
--------

You can also add a tool after the creation of the Config object::

    conf.add_tool('qt')


Options
-------

This method is used to build and to populate a SCons Option object based on the various tools maintain by the config object. In the next example, the values of the parameters will be retrieved in the option.py file or in the command line parameters. For each parameter, a default value is specified in each tool::

    options= conf.Options('option.py',ARGUMENTS)

Add to your SConstruct the following command to generate the list of optional parameters with their default value::

    Help(options.GenerateHelpText(env))

On the command line, type::

    scons -h

UpdateOptions
-------------

This method is the same than the previous Options method, but you pass as parameter an existing SCons Options object::

    # Create a SCons Options instance
    options= Options('option.py',ARGUMENTS)
    conf.Update( options )

Thus, a same set of options can be shared between various Config instances.

Update
------

This is the main method. The Update method update the Environment instance based on each tool strategy and on the values of the default parameters and by the parameters set by the user via the configuration file (e.g. option.py)::

    conf.Update(env)

For instance, the boost_python tool update the environment as is::

    class Boost_Python:
        def update( self, env ):
            """ Update the environment with specific flags """
 
            env.AppendUnique( CPPPATH= [ env['boost_includes'] ] )
            env.AppendUnique( LIBPATH= [ env['boost_lib'] ] )
            env.Append( CPPDEFINES= '$boost_defines' )
            env.Append( CPPFLAGS= '$boost_flags' )
 
            boost_name= 'boost_python'+ env['boost_libs_suffix']
            env.AppendUnique( LIBS= [ boost_name ] )

Configure
---------

The Configure method test on each tool the validity of the configuration by generating a simple program and trying to build it::

    conf.Configure( env )

Available Tools with Options
Compiler

The compiler tool is set by default when creating a Config object. It defines OS and compiler independant flags like debug or warning. These abstract settings are converted in specific flags for each compiler.

Available compilers are:

    * gcc: gcc on linux and win32 with cygwin
    * mingw: gcc compiler for win32
    * msvc: Visual Studio 6., 7. and 8.

=================== =========================================   ================================
Variable name       Semantic                                    Default
=================== =========================================   ================================
debug               Build in a debug mode                       False
warnings            Compilation with -Wall and similar          False
static              Build static libraries (not dynamic)        False
compiler            Compiler tool used for the build            Linux:gcc, Windows:msvc or mingw
rpath               List of paths to shared libraries (linux    None
EXTRA_CXXFLAGS      Specific user flags for c++ compiler        None
EXTRA_CPPDEFINES    Specific c++ defines                        None
EXTRA_LINKFLAGS     Specific user flags for c++ linker          None
EXTRA_CPPPATH       Specific user include path                  None
EXTRA_LIBPATH       Specific user library path                  None
EXTRA_LIBS          Specific user libraries                     None
=================== =========================================   ================================

Build Directory
---------------

The builddir tool is set by default when creating a Config object.

It set a build directory that allows to separate built files from sources.


=================== =============================================== ========================================
Variable name       Semantic                                        Default
=================== =============================================== ========================================
with_build_dir      build files in a separate directory? (yes/no)   True, yes, 1
build_prefix        root of the build directory                     Linux: build-linux, Windows: build-win32
=================== =============================================== ========================================


Install
-------

The install tool defines where to install various built files on the system like programs, libraries, headers and so on.


=============== =============================================================== ====================================
Variable name   Semantic                                                        Default
=============== =============================================================== ====================================
prefix          install architecture-independent files ( /path/to/prefix )      Linux: /usr/local, Windows: C:\local
exec_prefix     install architecture-dependent files ( /path/to/exec_prefix )   $prefix
bindir          user executables ( /path/to/bindir )                            $prefix/bin
libdir          object code libraries ( /path/to/libdir )                       $prefix/lib
includedir      header files ( /path/to/includedir )                            $prefix/include
datadir         data ( /path/to/datadir )   $prefix/share
program_prefix  prepend prefix to installed program names   
program_suffix  append suffix to installed program names    
lib_prefix      prepend prefix to installed library names   
lib_suffix      append suffix to installed library names    
=============== =============================================================== ====================================



Python
------

The python tool allows to link with the Python library.

=================== =================================================== =======
Variable name       Semantic                                            Default
=================== =================================================== =======
python_includes     Python include files ( /path/to/python_includes )   
python_lib          Python library path ( /path/to/python_includes )    
=================== =================================================== =======






Boost.Python
-------------

The boost_python tool allows to link with the Boost.Python library. It depends on the python tool.


    
=================== ======================================================= =============
Variable name       Semantic                                                Default
=================== ======================================================= =============
boost_includes      Boost_python include files ( /path/to/boost_includes )  /usr/include
boost_lib           Boost_python libraries path ( /path/to/boost_lib )      /usr/lib
boost_flags         Boost_python compiler flags     None
boost_defines       Boost_python defines    None
boost_libs_suffix   Boost_python library suffix name like -vc80-mt or -gcc  None
=================== ======================================================= =============

QT 3
----


The qt tool allows configure the QT environment. The multithreaded qt library is used rather than the default library if available.

=============== ======================= ==========================
Variable name   Semantic                Default
=============== ======================= ==========================
QTDIR           QT directory            QTDIR environment variable
QT_CPPPATH      QT include directory    $QTDIR/include
QT_LIBPATH      QT lib directory        $QTDIR/lib
QT_BINPATH      QT bin directory        $QTDIR/bin
=============== ======================= ==========================

OpenGL
------

The opengl tool allows to build with the OpenGL library.

=============== ========================================== =======================================================
Variable name   Semantic    Default
=============== ========================================== =======================================================
gl_includes     GL include files ( /path/to/gl_includes)   Posix: /usr/X11R6/include Windows: Visual include path
gl_lib          GL library path ( /path/to/gl_lib)         Posix: /usr/X11R6/lib Windows: Visual lib path
=============== ========================================== =======================================================

QHull
-----

The qhull tool allows to build with the C qhull library.

=================== =============================================== =============
Variable name       Semantic                                        Default
=================== =============================================== =============
qhull_includes      Qhull include files                             /usr/include
qhull_lib           Qhull library path                              /usr/lib
qhull_libs_suffix   Qhull library suffix name like -vc80 or -mingw  None
=================== =============================================== =============

Bison and Flex
--------------

bison and flex tools for setting binary and/or lib path.

============== ======================
Variable name  Semantic
============== ======================
bison_bin      Bison binary path
flex_bin       Flex binary path
flex_lib       Flex library path
============== ======================

gnuplot
-------


gnuplot tool for setting the binary path

==============  ============================================
Variable name   Semantic
==============  ============================================
gnuplot_bin     Gnuplot binary path ( /path/to/gnuplot_bin )
==============  ============================================

Posix only tools
----------------

pthread, readline and termcap. These tools are required by other tools on Posix system.

==================  ======================= ====================
Variable name       Semantic                Default
==================  ======================= ====================
pthread_includes    pthread include files   /usr/include
pthread_lib         pthread library path    /usr/lib
readline_includes   readline include files  /usr/include
readline_lib        readline library path   /usr/lib
termcap_includes    termcap include files   /usr/include
termcap_lib         termcap library path    /usr/lib
==================  ======================= ====================


High-level functions for OpenAlea developpers

SConsX provide high level functions to simplify the complexity of building an OpenAlea package:
Usage

A simple script that build a library mypkg from all the cpp files in the current directory, and install all the headers in a specific directory::

    includes= env.ALEAGlob('*.h')
    env.ALEAIncludes('mypkg',includes)

    sources= env.ALEAGlob('*.cpp')
    env.ALEALibrary('mypkg', sources)

ALEASolution
------------

    * Configure a default environment with user options and set of tools.
    * Generate the help obtained by `scons -h`
    * Define the build directory to copy libraries, binaries and includes files.

>>>    env = ALEASolution(options, tools=...)

ALEALibrary
-----------

    * Build static or dynamic library based on user flags.
    * Install the built library and associated files in specific directories.
    * Define build and install target.

>>> env.ALEALibrary("mylib", sources, CPPDEFINES=...)

ALEAIncludes
------------

    * Install the headers in a specific directory.
    * Define build and install target.

>>> env.ALEAIncludes("TheNameOfMyHeaderDirectory", headers)

ALEAProgram
-----------

    * Build a program and install it in local and system directories.

>>> env.ALEAProgram("myprog", headers)

ALEAWrapper
-----------

Build a python wrapper and install it directly in the python package directory. It is used to build Boost.Python wrappers.

>>> env.ALEAWrapper('../../myPythonDir','_mylib',sources)

ALEAGlob
--------

Glob files by taking into account the build directory which is not the same as the source directory.

>>> files= env.ALEAGlob('*.cpp',dir= '.')
>>> # or
>>> scons_files= env.ALEAGlob('SConscript','dir='*')

ALEAGlobDir
-----------

Idem that ALEAGlob, but return a list of directory only.

>>> # return all the directories contain in the current directory.
>>> dirs= env.ALEAGlobDir('*',dir= '.')


