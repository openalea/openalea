SConsX
======

You can read an update version of this file on the OpenAlea Website
(see http://openalea.gforge.inria.fr).

SConsX is a package of the OpenAlea project.

===== About =====

**SConsX** is an extension package of the famous [[http://www.scons.org|SCons]] build tool.
SConsX aims to simplify the build of complex multi-platform packages (i.e. using C++, Boost.Python and Python).

Like **Boost.Jam** or **qmake**, it knows about different types of compiler, and the different steps involved in compiling for Windows and Linux.
This knowledge allows the user to describe what needs to be built in high-level terms, without concern for low-level details such as the compiler's specific flags, the way that the operating system handles dynamic libraries. 
The goal is to be able to write a single, simple, build description (SConsctruct and SConscript ) that is likely to work for several compilers on Linux and Windows. It also has built-in support for variant builds ( e.g.debug, release), options (e.g. include paths and threading options) and dependencies associated with the usage of particular libraries.
The build objects are created in a separate build directory, not in the source directory.

**SConsX** extend **SCons** by adding knowledge to existing tools that are system dependent (e.g. default options and path, dependencies between tools). All the internal options can be overwited in an external configuration file (named **option.py**).
For each tools, **SConsX** add also configuration capabilities that mimic autoconf functionalities.

**SConsX** is just a thin wrapper over SCons. It's easily extendible. You can add new tools as well as new high-level commands.

**SConsX** is under development. Lot of work have to be done for a better support of new compiler (e.g. Visual C++, mingw), new tools and new functionalities.

=== Description ===
SconsX provides a set of tools with default options, configurations  and dependencies.

Each tool provides:
  * A set of options with default values dependeing on the OS.
  * A list of dependecies. For instance, Boost.Python depends on Python.
  * A configuration method that use **SConf**, the configuartion tool used by **SCons**.
  * An update method that update the SCons environment with specific flags.

Available tools are limited but can be easily extended :
  * **compiler**: Define a set of generic flags (e.g. debug or warning) for compilers on various OS.
  * **builddir**: Define a build directory for build objects and sub directories for header files, lib and bin files created during the build.
  * **install**:  Define install directories used during the install stage, i.e. exec and exec_prefix, libdir, bindir and includedir as well as datadir.
  * Other tools: **OpenGL**, **QT**, **bison**, **flex**, **Boost.Python**, ...


===== Quick Example =====
This is a SConstruct file. 
See the [[http://www.scons.org|SCons]] documentation for more information.

<code python>
import sconsx
from sconsx import config

# Creation of a SCons object
# Set an option file as well as command line args.
option= Options("options.py", ARGUMENTS)

# Creation of a SConsX object 
conf = config.Config([ 'install', 'boost.python', 'qt'])

# Update the SCons option with the default settings of each tools
conf.UpdateOptions( options )

# Creation of the Scons Environment
env= Environment( options= option )

# Update the environment with specific flags defined by SConsX and the user.
conf.Update( env )

SConscript(...)
</code>

===== Installation =====

=== Download ===

SConsX is available on the [[http://gforge.inria.fr/projects/openalea/|GForge repositery]].

=== Requirements ===

There are two requirements:
  * SCons (http://www.scons.org) version >= 0.96.93
  * OpenAlea.DistX 

=== Installation ===

Extract the tarball, jump into the created directory and run :

	python setup.py install

For installation options, see :

	python setup.py install --help


