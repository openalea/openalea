# -*- python -*-
#
#       openalea.deploy.dependency_builder
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "Cecill-C"
__revision__ = " $Id$"

# README!

# This script builds binary dependencies for OpenAlea:
# Qt4, SIP, PyQt4, [Py]QSCintilla, [Py]QGLViewer, CGAL, BOOST, etc...
# It downloads, unpacks, configures, compiles, install each dependency
# and then builds eggs out of them.

# It is not smart! It builds things in the (hardcoded) order they are specified.
# Projects are configured and installed one after another. the system $PATH, $PYTHONPATH
# and sys.path are extended as projects get installed, which lets the following projects
# correctly access the required binaries and python packages.
# Here is what is built, in the order they are processed :
    # - Qt4
    # - Sip
    # - PyQt4
    # - QScintilla
    # - PyQScintilla
    # - QGLViewer
    # - PyQGLViewer
    # - BOOST
    # [- CGAL]
        
# Then the eggs are built.

# TODO! This can be merged with the utility that makes windows installers
# and the system_dependecies utility.
    
import traceback
import platform
import os
import sys
import shutil
import urllib2
import urllib
import subprocess
import glob
import time
import pprint
import fnmatch
import re
import string
import argparse
import datetime
import zipfile
import tarfile
from os.path import join as pj, splitext, getsize, exists, abspath, split
from collections import namedtuple, OrderedDict, defaultdict
from setuptools import find_packages

Project = namedtuple("Project", "name url")
Egg = namedtuple("Egg", "name license authors description")
sj = os.pathsep.join

verbose = False


# A Project with a None url implicitely means the sources are already here because some other proj installed it.
projs = OrderedDict ( (p.name,p) for p in  [ 
                                             Project("mingwrt"     , None),
                                             Project("qt4"         , "http://download.qt.nokia.com/qt/source/qt-everywhere-opensource-src-4.7.4.zip"),
                                             Project("sip"         , "http://www.riverbankcomputing.co.uk/static/Downloads/sip4/sip-4.13.zip"),
                                             Project("pyqt4"       , "http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-win-gpl-4.8.6.zip"),
                                             Project("qscintilla"  , "http://www.riverbankcomputing.co.uk/static/Downloads/QScintilla2/QScintilla-gpl-2.6.zip"),
                                             Project("pyqscintilla", None), # shares the same as qscintilla
                                             Project("qglviewer"   , "https://gforge.inria.fr/frs/download.php/28138/libQGLViewer-2.3.9-py.tgz"),
                                             Project("pyqglviewer" , "https://gforge.inria.fr/frs/download.php/28212/PyQGLViewer-0.9.1.zip"),
                                             Project("boost"       , "http://switch.dl.sourceforge.net/project/boost/boost/1.48.0/boost_1_48_0.zip"),
                                             #Project("ann"         , "http://www.cs.umd.edu/~mount/ANN/Files/1.1.2/ann_1.1.2.zip"),
                                             #Project("gnuplot"     , "http://heanet.dl.sourceforge.net/project/gnuplot/gnuplot/4.4.4/gp444win32.zip"),
                                             #Project("qhull"       , "http://www.qhull.org/download/qhull-2011.2.zip"),
                                             #Project("rpy2"       , "http://cran.cict.fr/bin/windows/base/R-2.14.0-win.exe"),
                                           ]
                    )
                        
eggs = OrderedDict ( (p.name,p) for p in  [Egg("mingw", 
                                               "PublicDomain for MingW runtime. GLP or LGPL for some libraries.",
                                               "The Mingw Project",
                                               "Mingw Development (compiler, linker, libs, includes)"
                                               ),
                                               
                                           Egg("mingw_rt", 
                                               "PublicDomain for MingW runtime. GLP or LGPL for some libraries.",
                                               "The Mingw Project",
                                               "Mingw Runtime"
                                               ), 
                                               
                                           Egg("qt4", 
                                               "General Public License V3",
                                               "Riverbank Computing (Sip+PyQt4+QSCintilla) & Nokia (Qt4)",
                                               "Sip+PyQt4+QScintilla Runtime packaged as an egg for windows-gcc"
                                               ), 
                                               
                                           Egg("qt4_dev", 
                                               "General Public License V3",
                                               "Riverbank Computing (Sip+PyQt4+QSCintilla) & Nokia (Qt4)",
                                               "Sip+PyQt4+QScintilla Development packaged as an egg for windows-gcc"
                                               ), 
                                               
                                           Egg("pyqglviewer", 
                                               "General Public License",
                                               "libQGLViewer developers for libQGLViewer, PyQGLViewer (INRIA) developers for PyQGLViewer",
                                               "Win-GCC version of PyQGLViewer"
                                               ),
                                               
                                           Egg("boost", 
                                               "Boost Software License 1.0",
                                               "Boost contributors",
                                               "Windows gcc libs and includes of Boost"
                                               ),                                               

                                           # Egg("ann", 
                                               # "GNU Lesser Public License",
                                               # "Copyright (c) 1997-2010 University of Maryland and Sunil Arya and David Mount",
                                               # "Windows gcc libs and includes of ANN"
                                               # ),
                                               
                                           # Egg("gnuplot", 
                                               # "GNUPlot license",
                                               # "Copyright 1986 - 1993, 1998, 2004 Thomas Williams, Colin Kelley",
                                               # "Windows gcc libs and includes of gnuplot"
                                               # ),
                                               
                                           # Egg("qhull", 
                                               # "GNUPlot license",
                                               # "Copyright (c) 1993-2011 C.B. Barber, Arlington, MA and The Geometry Center, University of Minnesota",
                                               # "Windows gcc libs and includes of qhull"
                                               # ),
                                               
                                           # Egg("rpy2", 
                                               # "rpy2 license",
                                               # "RPy2 Contributors",
                                               # "Windows gcc libs and includes of rpy2"
                                               # ),
                                               
                                           # The following eggs require the PYTHON libs to be installed on your computer.
                                           Egg("numpy", 
                                               "Numpy License",
                                               "(c) Numpy Developers",
                                               "Numpy packaged as an egg"
                                               ), 
                                               
                                           Egg("scipy", 
                                               "Scipy License",
                                               "(c) Entought",
                                               "Scipy packaged as an egg"
                                               ),     
                                               
                                           Egg("matplotlib", 
                                               "Python Software Foundation License Derivative - BSD Compatible.",
                                               "Matplotlib developers",
                                               "Scipy packaged as an egg"
                                               ),         
                                               
                                           Egg("PIL", 
                                               "PIL License.",
                                               "Copyright (c) 1997-2011 by Secret Labs AB, Copyright (c) 1995-2011 by Fredrik Lundh.",
                                               "PIL packaged as an egg"
                                               ),  
                                               
                                           Egg("pylsm", 
                                               "PYLSM License.",
                                               "Freesbi.ch",
                                               "Patched version of PyLSM"
                                               ),                                                

                                           # Egg("pylibtiff", 
                                               # "BSD License.",
                                               # "Pearu Peterson & friends.",
                                               # "Precompiled pylibtiff for Windows."
                                               # ),                                                
                                           ]
                   )

# Some utilities
def merge_list_dict(li):
    """ Converts li which is a list of (key,value) into
    a dictionnary where items with the same keys get appended
    to a list instead of overwriting the key."""    
    d = defaultdict(list)
    for k, v in li:
        d[k].extend(v)        
    return dict( (k, sj(v)) for k,v in d.iteritems() )

compile = re.compile    
CompiledRe = type(compile(""))    
def recursive_glob(dir_, patterns=None, strip_dir_=False, levels=-1):
    """ Goes down a file hierarchy and returns files paths
    that match filepatterns or regexp."""
    files = []
    if isinstance(patterns, CompiledRe):
        filepatterns, regexp = None, patterns
    else:
        filepatterns, regexp = patterns.split(","), None
        
    lev = 0
    for dir_path, sub_dirs, subfiles in os.walk(dir_):
        if lev == levels:
            break
        if filepatterns:
            for pat in filepatterns:
                for fn in fnmatch.filter(subfiles, pat):
                    files.append( os.path.join(dir_path, fn) )
        elif regexp:
            for fn in subfiles:
                if regexp.match(fn): files.append(os.path.join(dir_path, fn))
        lev += 1
    dirlen = len(dir_)
    return files if not strip_dir_ else [ f[dirlen+1:] for f in files]
    
def recursive_glob_as_dict(dir_, patterns=None, strip_dir_=False, 
                           strip_keys=False, prefix_key=None, dirs=False, levels=-1):
    """Recursively globs files and returns a list of the glob files.
    The globbing can use regexps or shell wildcards. 
    """
    files     = recursive_glob(dir_, patterns, strip_dir_, levels)
    by_direct = defaultdict(list)
    dirlen = len(dir_)
    for f in files:        
        target_dir = split(f)[0]
        if strip_keys:
            target_dir = target_dir[dirlen+1:]
        if prefix_key:
            target_dir = pj(prefix_key, target_dir)
        if dirs:
            f = os.path.split(f)[0]
            if f not in by_direct[target_dir]:
                by_direct[target_dir].append(f)
        else:
            by_direct[target_dir].append(f)
    return by_direct

def makedirs(pth, verbose=False):
    """ A wrapper around os.makedirs that prints what 
    it's doing and catches harmless errors. """
    #print "creating", pth, "...",
    try:
        os.makedirs( pth )
        #print "ok"
    except os.error, e:
        #print "already exists or access denied"
        if verbose:
            traceback.print_exc()    
    
def copy(source, dest, patterns):
    """ A copy function that copies by 
    pattern (filepattern, NOT regexp) """
    patterns = patterns.split(",")
    files = []
    for pat in patterns:
        files += glob.glob( pj(source, pat) )
    for f in files: 
        shutil.copy(f, dest)

def recursive_copy(sourcedir, destdir, patterns=None, levels=-1, flat=False):
    """Like shutil.copytree except that it accepts a filepattern or a file regexp."""
    src = recursive_glob( sourcedir, patterns, levels=levels )
    dests = [destdir]*len(src) if flat else \
            [ pj(destdir, f[len(sourcedir)+1:]) for f in src]            
    bases = set([ split(f)[0] for f in dests])
    for pth in bases:
        makedirs(pth)
    for src, dst in zip(src, dests):
        #print src, dst
        shutil.copy(src, dst)               

def ascii_file_replace(fname, oldstr, newstr):
    """ Tries to find oldstr in file fname and replaces it with newstr. 
    Doesn't do anything if oldstr is not found.
    File is overwritten. Doesn't handle any exception.
    """
    txt = ""
    patch = False
    with open(fname) as f:
        txt = f.read()
        
    if oldstr in txt:
        patch = True        
        txt = txt.replace(oldstr, newstr)
        
    if patch:
        with open(fname, "w") as f:
            print "patching", fname
            f.write(txt)
                               
class Later(object):
    """ Just a way to be able to check if a process should be done later,
    and not mark it as done or failed"""
    pass
    
# Every class used here is a Singleton. Hum, maybe this == bad-design.
 # - The base Singleton metaclass is just that: a metaclass that converts
   # the classes that use it into Singletons
 # - The (Project|Egg)Builders metaclasses are also singleton metaclasses
   # but they act as registries for the classes that use them.
   # The classes are stored in the (Project|Egg)Builders.builders dicts.
   # These dicts are referred to in the build_proj function

class Singleton(type):
    """ Singleton Metaclass """
    def __init__(cls, name, bases, dic):
        type.__init__(cls, name, bases, dic)
        cls.instance=None
    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance=type.__call__(cls, *args, **kw)
        return cls.instance
        
class ProjectBuilders(Singleton):
    """ A Project Builder registry and Singleton Metaclass """
    builders = {}
    def __init__(cls, name, bases, dic):
        Singleton.__init__(cls, name, bases, dic)
        ProjectBuilders.builders[name] = cls
        
class EggBuilders(Singleton):
    """ An Egg Builder registry and Singleton Metaclass """
    builders = {}
    def __init__(cls, name, bases, dic):
        Singleton.__init__(cls, name, bases, dic)
        if "egg_" in name: #dunno why "EggBuilder" gets passed here.
            EggBuilders.builders[cls.__eggname__] = cls        
        
class NullOutput(object):
    def write(self, s):
        pass
        
# -- we define a micro build environment --
class BuildEnvironment(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.options = {}
        self.proj_builders = None
        self.egg_builders  = None
        self.options = {}
        self.working_path    = None
        self.proc_file_path  = None
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr        
        self.null_stdout     = NullOutput()
        
    def set_options(self, options):
        self.options = options.copy()
        self.init()
        
    def init(self):
        self.working_path   = pj( self.options.get("wdr", abspath(".")), self.get_platform_string() )
        self.proc_file_path = pj(self.working_path,"proc_flags.pk")
        self.create_working_directories()        
        recursive_copy( split(__file__)[0], self.working_path, "setup.py.in", levels=1)
        recursive_copy( split(__file__)[0], self.working_path, "qmake_main.cpp.sub", levels=1)
        self.__fix_environment()
        self.__fix_sys_path()              

    def __fix_environment(self):
        # TODO : Clean env so that we do not propagate preexisting installations in subprocesses        
        # give priority to OUR compiler!
        os.environ["PATH"] = sj([self.get_compiler_bin_path(), os.environ["PATH"]])    
        
    def __fix_sys_path(self):
        # Clean sys.path for this process so that we don't import 
        # existing eggs or site-installed thingys.
        our_egg_names = EggBuilders.builders.keys()
        for pth in sys.path[:] :
            pth_p = pth.lower()
            for egg_name in our_egg_names:
                if egg_name in pth_p:
                    sys.path.remove(pth)
                    break
        
    # -- context manager protocol --
    def __enter__(self):
        try:
            with open(self.proc_file_path, "rb") as f:
                txt  = f.read()
                self.done_tasks = eval(txt)
        except:
            traceback.print_exc()
            self.done_tasks = {}
            
    def __exit__(self, exc_type, exc_value, traceback):
        with open(self.proc_file_path, "wb") as f:
            pprint.pprint(self.done_tasks, f)
                
    # -- Project building --
    def __init_builders(self):
        self.proj_builders = [self.__get_project_builder(spec) for spec in projs.itervalues()]
        self.egg_builders  = [self.__get_egg_builder(spec) for spec in eggs.itervalues()]
                
    def __get_project_builder(self, spec):
        builder = ProjectBuilders.builders[spec.name]
        return builder
        
    def __get_egg_builder(self, spec):
        builder = EggBuilders.builders[spec.name]
        return builder
            
    def build(self):
        self.__init_builders()  
        for buildercls in self.proj_builders + self.egg_builders:
            builder = buildercls()
            if builder.has_pending and builder.enabled:
                builder.process_me()
            
    def task_is_done(self, name, task):
        """ Marks that the `task` step has been accomplished for `proj`.
        name is a string (class name)
        task is a key from proj_taskess_map or egg_taskess_map
        """
        if task not in self.done_tasks.setdefault(name, ""):
            self.done_tasks[name] += task
            
    def is_task_done(self, name, task):
        """ Marks that the `proc` step has been accomplished for `proj`.
        name is a string (class name)
        proc is a key from proj_process_map or egg_process_map
        """
        return task in self.done_tasks.setdefault(name, "")
        
    def task_is_forced(self, name, task):
        """ Marks that the `proc` step has been accomplished for `proj`.
        name is a string (class name)
        proc is a key from proj_process_map or egg_process_map
        """
        return task in self.options.setdefault(name, "")

    def make_silent(self, silent):
        if silent:
            sys.stdout = self.null_stdout
            sys.stderr = self.null_stdout            
        else:
            sys.stdout = self.original_stdout
            sys.stderr = self.original_stderr            

            # Some info to tell us where to build
    def get_platform_string(self):
        # TODO : do smart things according to self.options
        return "_".join([platform.python_version(),
                        platform.system(),
                        platform.architecture()[0]])

    def get_working_path(self):
        # TODO : do smart things according to self.options
        return self.working_path

    def get_dl_path(self):
        # TODO : do smart things according to self.options
        return pj( self.get_working_path(), "dl")

    def get_src_path(self):
        # TODO : do smart things according to self.options
        return pj( self.get_working_path(), "src")

    def get_install_path(self):
        # TODO : do smart things according to self.options
        return pj( self.get_working_path(), "install")

    def get_egg_path(self):
        # TODO : do smart things according to self.options
        return pj( self.get_working_path(), "egg")

    def create_working_directories(self):
        pths = [self.get_working_path(),
                self.get_dl_path(),
                self.get_src_path(),
                self.get_install_path(),
                self.get_egg_path()]
        for pth in pths:
            makedirs(pth)

    # Obtaining Compiler Info - We only want MINGW compiler
    def install_compiler(self):
        raise NotImplementedError

    def get_compiler_bin_path(self):
        # TODO : do smart things according to self.options
        
        # -- try to find it in eggs --
        try:
            from pkg_resources import Environment
            env = Environment()
            return pj(env["mingw"], "bin")
        except:
            return r"c:\mingw\bin"
        return r"c:\mingw\bin"
#a shorthand:
BE=BuildEnvironment

# -- a few decorators to factor out some code --
def try_except( f ) :
    """Encapsulate the function in a try...except structure
    which prints the exception traceback and returns False on exceptions
    or returns the result of f on success."""
    def wrapper(self, *args, **kwargs):
        try:
            ret = f(self, *args, **kwargs)
        except:
            traceback.print_exc()
            return False
        else:
            return ret
    return wrapper

def in_dir(directory):    
    def dir_changer( f ) :
        """Encapsulate f in a structure that changes to self.sourcedir,
        calls f and moves back to BuildEnvironment.get_working_path()"""
        def wrapper(self, *args, **kwargs):
            d_ = getattr(self, directory)
            print "changing to", directory, "for", f
            os.chdir(d_)
            ret = f(self, *args, **kwargs)
            os.chdir(self.env.get_working_path())
            return ret
        return wrapper
    return dir_changer
    

class BaseBuilder(object):
    supported_procs = None
    all_procs       = None
    silent_procs    = ""
    enabled         = True
    
    def __init__(self):
        self.env = BE()
        if self.spec is None:
            raise Exception("cannot find " + self.name + " specifications")
        self.pending = None
        
    @property
    def options(self):
        return self.env.options
    @property
    def spec(self):
        raise NotImplementedError
    @property
    def name(self):
        return self.__class__.__name__
    @property
    def has_pending(self):
        if self.pending is None:
            self.__find_pending_tasks()
        return len(self.pending) != 0
        
    def __find_pending_tasks(self):
        tasks = []
        name  = self.name
        for task in self.supported_procs:
            task_func, skippable = self.all_procs[task]
            done   = self.env.is_task_done(name, task)
            forced = self.env.task_is_forced(name, task)
            skip = done and not forced and skippable
            if not skip:
                tasks.append((task, task_func, skippable))
        self.pending = tasks

    def __has_pending_verbose_tasks(self):
        for task, func, skippable in self.pending:
            if task not in self.silent_procs:
                return True
        return False     
        
    def process_me(self):
        self.env.make_silent( not self.__has_pending_verbose_tasks() )

        proc_str  = "PROCESSING " + self.name         
        print "\n",proc_str
        print "="*len(proc_str)
        # forced_tasks is a string containing self.all_procs keys.
        # if a process is in forced_tasks it gets forced.
        forced_tasks = self.options.get(self.spec, "")
        print "forced tasks are:", forced_tasks   

        for task, task_func, skippable in self.pending:
            nice_func = task_func.strip("_")
            print "\t-->performing %s for %s"%(nice_func, self.name)
            success = getattr(self, task_func)()
            if success == Later:
                print "\t-->%s for %s we be done later"%(nice_func, self.name)
            elif success == False:
                print "\t-->%s for %s failed"%(nice_func, self.name)
                sys.exit(-1)
            else:
                self.env.task_is_done(self.name, task)
                
        self.env.make_silent(False)        
      


  
class BaseProjectBuilder(BaseBuilder):
    __metaclass__ = ProjectBuilders
        
    all_procs       = OrderedDict([ ("d",("download_source",True)),
                                    ("u",("unpack_source",True)),
                                    ("f",("fix_source_dir",False)),
                                    ("c",("_configure",True)),
                                    ("b",("_build",True)),
                                    ("i",("_install",True)),
                                    ("p",("_patch", True)), #where should you be?
                                    ("x",("_extend_sys_path",False)),
                                    ("y",("_extend_python_path",False)),
                                    ])
    silent_procs    = "fxy"
    supported_procs = "".join(all_procs.keys())
    
    download_name  = None
    archive_subdir = None
    
    def __init__(self):
        BaseBuilder.__init__(self)   
        self.archname  = pj( self.env.get_dl_path() , self.download_name)
        self.sourcedir = pj( self.env.get_src_path(), splitext(self.download_name)[0] )
        self.installdir = pj( self.env.get_install_path(), splitext(self.download_name)[0] )
        
    @property
    def spec(self):
        return projs.get(self.__class__.__name__)        
        
    def download_source(self):
        def download_reporter(bk, bksize, bytes):
            if bytes == 0:
                raise urllib2.URLError("Url doesn't point to a valid resource (version might have changed?)")
            progress= float(bk)/(bytes/bksize) * 100
            sys.stdout.write(("Dl %s from %.20s to %s: %.1f %%"%(self.spec.name, self.spec.url, self.download_name, progress))+"\r")
            sys.stdout.flush()

        # a proj with a none url implicitely means 
        # the sources are already here because some
        # other proj installed it.
        if self.spec.url is None:
            return True
        remote_sz = float("inf")
        try:
            remote    = urllib.urlopen(self.spec.url)
        except IOError:
            traceback.print_exc()
            return False
        remote_sz = int(remote.info().getheaders("Content-Length")[0])
        remote.close()
        ret = True
        try:
            local_sz = getsize(self.archname) #raises os.error if self.archname doesn't exist
            if local_sz<remote_sz :
                raise os.error # download is incomplete, raise error to download
        except os.error:
            try:
                urllib.urlretrieve(self.spec.url, self.archname, download_reporter)
            except:
                traceback.print_exc()
                ret = False
        return ret

    def unpack_source(self):
        # a proj with a none url implicitely means 
        # the sources are already here because some
        # other proj installed it.
        if self.spec.url is None:
            return True
        if exists(self.sourcedir):
            return True
        base, ext = splitext( self.download_name )
        print "unpacking", self.download_name
        if ext == ".zip":
            zipf = zipfile.ZipFile( self.archname, "r" )
            # TODO : verify that there is no absolute path inside zip.
            zipf.extractall( path=self.sourcedir )
        elif ext == ".tgz":
            tarf = tarfile.open( self.archname, "r:gz")
            tarf.extractall( path=self.sourcedir )
        print "done"
        return True

    def fix_source_dir(self):
        try:
            print "fixing sourcedir", self.sourcedir,
            if self.archive_subdir is not None:
                self.sourcedir = glob.glob(pj(self.sourcedir,self.archive_subdir))[0]
            print self.sourcedir
        except:
            traceback.print_exc()
            return False
        else:
            return True

    def _extend_sys_path(self):
        exp = self.extra_paths()
        if exp is not None:
            if isinstance(exp, tuple):
                exp = sj(exp)           
            os.environ["PATH"] = sj([exp,os.environ["PATH"]])
        return True

    def _extend_python_path(self):
        exp = self.extra_python_paths()
        if exp is not None:
            if isinstance(exp, tuple):
                sys.path.extend(exp)
                exp = sj(exp)       
            elif isinstance(exp, str):
                sys.path.extend(exp.split(os.pathsep))
            os.environ["PYTHONPATH"] = sj([exp,os.environ.get("PYTHONPATH","")])
        return True

    # -- Top level process, they delegate to abstract methods, try not to override --
    @in_dir("sourcedir")
    @try_except
    def _configure(self):
        return self.configure()        
    @in_dir("sourcedir")
    @try_except
    def _build(self):
        return self.build()
    @in_dir("sourcedir")
    @try_except
    def _patch(self):
        return self.patch()
    @in_dir("sourcedir")
    @try_except
    def _install(self):
        return self.install()

    # -- The ones you can override are these ones --
    def extra_paths(self):
        return None
    def extra_python_paths(self):
        return None
    def configure(self):
        raise NotImplementedError
    def build(self):
        return subprocess.call("mingw32-make") == 0
    def patch(self):
        return True
    def install(self):
        return subprocess.call("mingw32-make install") == 0


        
class TemplateStr(string.Template):
    delimiter = "@"

def with_original_sys_path(f):
    def func(*args,**kwargs):
        cursyspath = sys.path[:]
        sys.path = BaseEggBuilder.__oldsyspath__[:]
        ret = f(*args, **kwargs)
        sys.path = cursyspath
        return ret
    return func
       
class BaseEggBuilder(BaseBuilder):
    __metaclass__  = EggBuilders
    __oldsyspath__ = sys.path[:]
    all_procs       = OrderedDict([("c",("_configure_script",True)),
                                   ("e",("_eggify",True)),
                                   ("u",("_upload_egg",True))
                                  ]) 
    supported_procs = "".join(all_procs.keys())
    
    py_dependent   = True
    arch_dependent = True
    
    def __init__(self,**kwargs):
        BaseBuilder.__init__(self, **kwargs)
        if "no_env" in kwargs:      
            self.eggdir         = ""
            self.setup_in_name  = ""
        else:
            self.eggdir         = pj(self.env.get_egg_path(), self.__eggname__)
            self.setup_in_name  = pj(self.env.get_working_path(), "setup.py.in")
        self.setup_out_name = pj(self.eggdir, "setup.py")
        self.use_cfg_login  = False
        makedirs(self.eggdir)
        
        self.default_substitutions = dict( NAME      = self.__eggname__,
                                           VERSION   = "1.0",
                                           THIS_YEAR = datetime.date.today().year,
                                           SETUP_AUTHORS = "Openalea Team",
                                           CODE_AUTHOR   = self.spec.authors,
                                           DESCRIPTION   = self.spec.description,
                                           URL           = "",
                                           LICENSE       = self.spec.license,
                                           
                                           ZIP_SAFE       = False,
                                           PYTHON_MODS    = None,
                                           PACKAGES       = None,
                                           PACKAGE_DIRS   = None,
                                           PACKAGE_DATA   = {},
                                           DATA_FILES     = None,
                                           
                                           INSTALL_REQUIRES = None,
                                           
                                           BIN_DIRS = None,
                                           LIB_DIRS = None,
                                           INC_DIRS = None,
                                           )
                            
    @property
    def spec(self):
        return eggs.get(self.__eggname__) 
        
    def _configure_script(self):
        try:
            with open( self.setup_in_name, "r") as input, \
                 open( self.setup_out_name, "w") as output:
                conf = self.default_substitutions.copy()
                conf.update(self.script_substitutions())
                conf = dict( (k,repr(v)) for k,v in conf.iteritems() )
                template = TemplateStr(input.read())
                output.write(template.substitute(conf))
        except Exception, e:
            traceback.print_exc()
            return False
        else:
            return True
        
    @in_dir("eggdir")
    @try_except
    def _eggify(self):
        ret     = self.eggify()
        # -- fix file name --
        eggname = glob.glob( pj(self.eggdir, "dist", "*.egg") )[0]
        dir_, filename = split(eggname)
        pyver   = "-py"+sys.winver
        archver = "-"+sys.platform
        if not self.py_dependent:
            filename = filename.replace(pyver, "")
        if not self.arch_dependent:
            filename = filename.replace(archver, "")            
        os.rename(eggname, pj(dir_, filename))
        return ret
                
    @in_dir("eggdir")
    @try_except
    def _upload_egg(self):
        if not self.options["login"] or not self.options["passwd"]:
            self.use_cfg_login = True
            ret = self.upload_egg()
            if not ret:
                print "No login or passwd provided, skipping egg upload"
                return Later
            return ret
        return self.upload_egg()

    def script_substitutions(self):
        return {}
        
    def eggify(self):
        #ret0 =  subprocess.call(sys.executable + " setup.py egg_info --egg-base=%s"%self.eggdir ) == 0
        return subprocess.call(sys.executable + " setup.py bdist_egg") == 0
        
    def upload_egg(self):
        if not self.use_cfg_login:
            opts = self.options["login"], self.options["passwd"], \
                    self.__eggname__, "\"ThirdPartyLibraries\"", "vplants" if not self.options["release"] else "openalea" 
            return subprocess.call(sys.executable + " setup.py egg_upload --yes-to-all --login %s --password %s --release %s --package %s --project %s"%opts) == 0
        else:
            opts = self.__eggname__, "\"ThirdPartyLibraries\"", "vplants" if not self.options["release"] else "openalea" 
            return subprocess.call(sys.executable + " setup.py egg_upload --yes-to-all --release %s --package %s --project %s"%opts) == 0
        

# -- Glob and regexp patterns --
class Pattern:
    # -- generalities --
    any     = "*"
    exe     = "*.exe"
    dynlib  = "*.dll"
    stalib  = "*.a"
    include = "*.h,*.hxx"
    
    # -- pythonities --
    pymod   = "*.py"
    pyext   = "*.pyd"
    pyall   = ",".join([pymod, pyext])
        
    # -- scintillacities --
    sciapi  = "*.api"
    
    # -- sip --
    sipfiles = "*.sip"
    
    # -- Qtities --
    qtstalib = "*.a,*.prl,*.pri,*.pfa,*.pfb,*.qpf,*.ttf,README"
    qtsrc    = "*.pro,*.pri,*.rc,*.def,*.h,*.hxx"
    qtinc    = compile(r"^Q[0-9A-Z]\w|.*\.h")
    qtmkspec = "*"
    qttransl = "*.qm"
        
        
####################################################################################################
# - PROJECT BUILDERS - PROJECT BUILDERS - PROJECT BUILDERS - PROJECT BUILDERS - PROJECT BUILDERS - #
####################################################################################################
class mingwrt(BaseProjectBuilder):
    supported_procs = "i" 
    download_name  = "mingw"
    archive_subdir = None    
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        self.sourcedir = pj(self.env.get_compiler_bin_path(), os.pardir)
        self.install_dll_dir = pj(self.installdir, "dll")
    def install(self):
        recursive_copy( pj(self.sourcedir, "bin"), self.install_dll_dir, Pattern.dynlib, levels=1)
        return True
        
class qt4(BaseProjectBuilder):
    download_name  = "qt4_src.zip"
    archive_subdir = "qt-every*"    
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        # define installation paths
        self.inst_paths = pj(self.installdir, "bin"), pj(self.installdir, "dll"), \
                          pj(self.installdir, "lib"), pj(self.installdir, "src"), \
                          pj(self.installdir, "include"), pj(self.installdir, "dll"), \
                          pj(self.installdir, "plugins_lib"), pj(self.installdir, "mkspecs"), \
                          pj(self.installdir, "translations")
        self.install_bin_dir, self.install_dll_dir, self.install_lib_dir, self.install_src_dir, self.install_inc_dir, self.install_plu_dir, self.install_plu_lib_dir, self.install_mks_dir, self.install_tra_dir = self.inst_paths        
    def configure(self):              
        pop = subprocess.Popen("configure.exe -platform win32-g++ -release -opensource -shared -nomake demos -nomake examples -mmx -sse2 -3dnow -declarative -webkit -no-s60 -no-cetest",
                               stdin=subprocess.PIPE) # PIPE is required or else pop.comminicate won't do anything!
        time.sleep(2) #give enough time for executable to load before it asks for license agreement.
        pop.communicate("y\r") #accepts license agreement, also waits for configure to finish                       
        return pop.returncode == 0
    def install(self):
        # create the installation directories
        for pth in self.inst_paths:
            makedirs(pth)            
        # copy binaries
        recursive_copy( pj(self.sourcedir, "bin"), self.install_bin_dir, Pattern.exe )
        # add a qt.conf file that tells qmake to look into directories that are relative to the executable.
        with open( pj(self.install_bin_dir, "qt.conf"), "w") as qtconf:
            qtconf.write("[Paths]")
        # copy dlls
        recursive_copy( pj(self.sourcedir, "bin"), self.install_dll_dir, Pattern.dynlib )        
        # copy libs
        recursive_copy( pj(self.sourcedir, "lib"), self.install_lib_dir, Pattern.qtstalib )
        # copy src -- actually only header files in src --
        recursive_copy( pj(self.sourcedir, "src"), self.install_src_dir, Pattern.qtsrc )
        # copy include
        recursive_copy( pj(self.sourcedir, "include"), self.install_inc_dir, Pattern.qtinc )
        # copy plugins
        recursive_copy( pj(self.sourcedir, "plugins"), self.install_plu_dir, Pattern.dynlib, flat=True )
        # copy plugins
        recursive_copy( pj(self.sourcedir, "plugins"), self.install_plu_lib_dir, Pattern.qtstalib )
        # copy plugins
        recursive_copy( pj(self.sourcedir, "mkspecs"), self.install_mks_dir, Pattern.qtmkspec )
        # copy translations
        recursive_copy( pj(self.sourcedir, "translations"), self.install_tra_dir, Pattern.qttransl )        
        return True
    def extra_paths(self):
        return pj(self.sourcedir, "bin"), self.install_dll_dir
    def patch(self):
        """ Patch qt *.exes and *.dlls so that they do not contain hard coded paths anymore. """
        import qtpatch
        try:
            qtpatch.patch("*.exe", qtDirPath=self.sourcedir, where=self.installdir)
        except:
            traceback.print_exc()
            return False
        else:
            return True

class sip(BaseProjectBuilder):
    download_name  = "sip_src.zip"
    archive_subdir = "sip*"
    regexp         = re.compile(r"\s*'\w*':\s*'C:\\\\.*\\\\.*'")
    
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        # define installation paths
        # we install sip binaries in the qt bin installation directory to easily recover it
        # for the egg. 
        qt4_ = qt4()
        self.inst_paths = qt4_.install_bin_dir, pj(self.installdir, "site"), pj(self.installdir, "include"), pj(self.installdir, "sip")
        self.install_bin_dir, self.install_site_dir, self.install_inc_dir, self.install_sip_dir = self.inst_paths    
    def configure(self):
        # -- The -S flag is needed or else configure.py sees any existing sip installation and can fail. --
        return subprocess.call(sys.executable + " -S configure.py --platform=win32-g++ -b %s -d %s -e %s -v %s"%self.inst_paths) == 0
    def extra_paths(self):
        return self.install_bin_dir
    def extra_python_paths(self):
        return self.install_site_dir
    def patch(self):
        # Feel free to do better
        header = """
import re
from os.path import join as pj     
from pkg_resources import Environment

# Default Path. 
qtdev = os.environ.get('QTDIR') if 'QTDIR' in os.environ else 'C:\\Qt\\4.6.0'
sip_bin     = pj(sys.prefix,'sip')
sip_include = pj(sys.prefix, 'include')
env = Environment()
if 'qt4' in env:
    qt = env['qt4'][0].location # Warning: 0 is the active one
if 'qt4-dev' in env:
    qtdev       = env['qt4-dev'][0].location # Warning: 0 is the active one
    sip_bin     = pj(qtdev,'bin','sip.exe')
    sip_include = pj(qtdev, 'include')
    """
        
        txt = ""
        print "sip patching", os.getcwd()
        with open("sipconfig.py") as f:
            txt = f.read()
        
        txt = txt.replace("import re", header)
        prefix = sys.prefix.replace("\\", r"\\\\")
        txt = re.sub(r"(\s*'default_bin_dir':\s*)'%s'"%prefix,    r"\1sys.prefix", txt)
        txt = re.sub(r"(\s*'default_mod_dir':\s*)'%s.*'"%prefix,  r"\1pj(sys.prefix,'Lib\site-packages')", txt)
        txt = re.sub(r"(\s*'default_sip_dir':\s*)'[A-Z]:\\\\.*'", r"\1pj(qtdev,'sip')", txt)
        txt = re.sub(r"(\s*'py_conf_inc_dir':\s*)'%s.*'"%prefix,  r"\1pj(sys.prefix,'include')", txt)
        txt = re.sub(r"(\s*'py_inc_dir':\s*)'%s.*'"%prefix,       r"\1pj(sys.prefix,'include')", txt)
        txt = re.sub(r"(\s*'py_lib_dir':\s*)'%s.*'"%prefix,       r"\1pj(sys.prefix,'libs')", txt)
        txt = re.sub(r"(\s*'sip_bin':\s*)'[A-Z]:\\\\.*'",         r"\1sip_bin", txt)
        txt = re.sub(r"(\s*'sip_inc_dir':\s*)'[A-Z]:\\\\.*'",     r"\1sip_include", txt)
        txt = re.sub(r"(\s*'sip_mod_dir':\s*)'[A-Z]:\\\\.*'",     r"\1qt", txt)

        shutil.copyfile( "sipconfig.py", "sipconfig.py.old" )
        with open("sipconfig.py", "w") as f:
            f.write(txt)
                    
        return True

class pyqt4(BaseProjectBuilder) :
    download_name  = "pyqt4_src.zip"
    archive_subdir = "PyQt*"
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        # define installation paths
        # we install pyqt4 binaries in the qt bin installation directory to easily recover it
        # for the egg.
        qt4_ = qt4()
        self.inst_paths = qt4_.install_bin_dir, pj(self.installdir,"site"), pj(self.installdir,"sip")
        self.install_bin_dir, self.install_site_dir, self.install_sip_dir = self.inst_paths    
    def configure(self):
        # -- The -S flag is needed or else configure.py sees any existing sip installation and can fail. --
        return subprocess.call(sys.executable + " -S configure.py --confirm-license -b %s -d %s -v %s"%self.inst_paths) == 0
    def extra_paths(self):
        return self.install_bin_dir
    def extra_python_paths(self):
        return self.install_site_dir
    def patch(self):
        header = """
import sipconfig
from sipconfig import pj as pj
from sipconfig import qtdev as qtdev
from sipconfig import qt as qt"""
        
        txt = ""
        with open("pyqtconfig.py") as f:
            txt = f.read()
            
        txt = txt.replace("import sipconfig", header)
        txt = re.sub(r"(\s*'pyqt_bin_dir':\s*)'[A-Z]:(\\\\|/).*'", r"\1pj(qtdev,'bin')", txt)
        txt = re.sub(r"(\s*'pyqt_mod_dir':\s*)'[A-Z]:(\\\\|/).*'", r"\1pj(qt,'PyQt4')", txt)
        txt = re.sub(r"(\s*'pyqt_sip_dir':\s*)'[A-Z]:(\\\\|/).*'", r"\1pj(qtdev,'sip')", txt)
        txt = re.sub(r"(\s*'qt_data_dir':\s*)'[A-Z]:(\\\\|/).*'",  r"\1qtdev.replace('\\','/')", txt)
        txt = re.sub(r"(\s*'qt_dir':\s*)'[A-Z]:(\\\\|/).*'",       r"\1qt", txt)
        txt = re.sub(r"(\s*'qt_inc_dir':\s*)'[A-Z]:(\\\\|/).*'",   r"\1pj(qtdev, 'include')", txt)
        txt = re.sub(r"(\s*'qt_lib_dir':\s*)'[A-Z]:(\\\\|/).*'",   r"\1pj(qtdev, 'lib')", txt)
        
        txt = re.sub(r"(\s*'INCDIR_QT':\s*)'[A-Z]:(\\\\|/).*'",    r"\1pj(qtdev, 'include')", txt)
        txt = re.sub(r"(\s*'LIBDIR_QT':\s*)'[A-Z]:(\\\\|/).*'",    r"\1pj(qtdev, 'lib')", txt)
        txt = re.sub(r"(\s*'MOC':\s*)'[A-Z]:(\\\\|/).*'",          r"\1pj(qtdev, 'bin', 'moc.exe')", txt)
        
        shutil.copyfile( "pyqtconfig.py", "pyqtconfig.py.old" )
        with open("pyqtconfig.py", "w") as f:
            f.write(txt)        
        prefix = sys.prefix

class qscintilla(BaseProjectBuilder):
    download_name  = "qscintilla_src.zip"
    archive_subdir = "QScint*/Qt4"
    def configure(self):
        # The install procedure will install qscintilla in qt's installation directories
        qt4_ = qt4()
        paths = qt4_.install_inc_dir, qt4_.install_tra_dir, qt4_.installdir, qt4_.install_dll_dir, 
        return subprocess.call("qmake -after header.path=%s trans.path=%s qsci.path=%s target.path=%s -spec win32-g++ qscintilla.pro"%paths) == 0
    def install(self):
        ret = BaseProjectBuilder.install(self)
        qt4_ = qt4()
        try:
            shutil.move( pj(qt4_.install_dll_dir, "libqscintilla2.a"), qt4_.install_lib_dir)
        except Exception, epyqt :
            print e
        return ret
        
class pyqscintilla(BaseProjectBuilder):
    download_name  = "qscintilla_src.zip"
    archive_subdir = "QScint*/Python"
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        # define installation paths
        qsci = qscintilla()
        qt4_ = qt4()
        pyqt = pyqt4()        
        self.install_paths = pj(qsci.sourcedir,"release"), pj(qt4_.installdir, "qsci"), qsci.sourcedir, pj(pyqt.install_site_dir, "PyQt4"), pyqt.install_sip_dir
        self.qsci_dir = self.install_paths[1]
    def configure(self):
        """pyqscintilla installs itself in PyQt4's installation directory"""
        # we want pyqscintilla to install itself where pyqt4 installed itself.
        # -- The -S flag is needed or else configure.py sees any existing sip installation and can fail. --
        return subprocess.call(sys.executable + " -S configure.py -o %s -a %s -n %s -d %s -v %s"%self.install_paths ) == 0 #make this smarter

class qglviewer(BaseProjectBuilder):
    download_name  = "qglviewer_src.tgz"
    archive_subdir = "libQGLV*/QGLViewer"
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        # qmake is annoying with backslashes
        self.install_inc_dir = pj(self.installdir, "include", "QGLViewer")
        self.install_dll_dir = pj(self.installdir, "dll")
        self.install_lib_dir = pj(self.installdir, "lib")
    def configure(self):        
        return subprocess.call("qmake QGLViewer*.pro") == 0
    def build(self):
        # by default, and since we do not use self.options yet, we build in release mode
        return subprocess.call("mingw32-make release") == 0
    def install(self):
        # The install procedure will install qscintilla in qt's directories   
        recursive_copy( self.sourcedir               , self.install_inc_dir, Pattern.include)
        recursive_copy( pj(self.sourcedir, "release"), self.install_lib_dir, Pattern.qtstalib)
        recursive_copy( pj(self.sourcedir, "release"), self.install_dll_dir, Pattern.dynlib)
        return True
    def extra_paths(self):
        return self.install_dll_dir

class pyqglviewer(BaseProjectBuilder):
    download_name  = "pyqglviewer_src.zip"
    archive_subdir = "PyQGLV*"
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        qglbuilder = qglviewer()
        self.qglbuilderbase = pj(qglbuilder.sourcedir, os.path.pardir),        
        self.install_sip_dir  = pj(qglbuilder.installdir, "sip")
        self.install_site_dir = qglbuilder.installdir
        self.install_exa_dir  = pj(qglbuilder.installdir, "examples")        
    def configure(self):
        # -- The -S flag is needed or else configure.py sees any existing sip installation and can fail. --
        return subprocess.call(sys.executable + " -S configure.py -Q %s "%self.qglbuilderbase) == 0
    def install(self):
        """ pyqglviewer installs itself into the same directory as qglviewer """
        recursive_copy( pj(self.sourcedir, "build"), self.install_site_dir, Pattern.pyext, levels=1)
        recursive_copy( pj(self.sourcedir, "src", "sip"), self.install_sip_dir, Pattern.sipfiles, levels=1)
        recursive_copy( pj(self.sourcedir, "examples"), self.install_exa_dir, Pattern.any)
        return True
    def extra_python_paths(self):
        qglbuilder = qglviewer()
        return qglbuilder.installdir

class boost(BaseProjectBuilder):
    download_name  = "boost_src.zip"
    archive_subdir = "boost*"
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        self.install_inc_dir = pj(self.installdir, "include")
        self.install_lib_dir = pj(self.installdir, "lib")
    def configure(self):
        """ bjam configures, builds and installs so nothing to do here"""
        return True
    def build(self):    
        # it is possible to bootstrap boost if no bjam.exe is found:
        if not exists( pj(self.sourcedir, "bjam.exe") ):
            if subprocess.call("bootstrap.bat") != 0:
                return False
            else:
                # The Bootstrapper top-level script ignores that gcc
                # was used and by default says it's msvc, even though
                # the lower level scripts used gcc.
                ascii_file_replace( "project-config.jam", 
                                    "using msvc",
                                    "using gcc")      
                        
        # try to fix a bug in python discovery which prevents
        # bjam from finding python on Windows NT and old versions.
        pyjam_pth = pj("tools","build","v2","tools","python.jam")
        ascii_file_replace(pyjam_pth, 
                           "[ version.check-jam-version 3 1 17 ] || ( [ os.name ] != NT )",
                           "[ version.check-jam-version 3 1 17 ] && ( [ os.name ] != NT )")                           
        
        paths = self.installdir, pj(sys.prefix, "include"), pj(sys.prefix,"libs")
        cmd = "bjam --debug-configuration --prefix=%s --without-test --layout=system variant=release link=shared threading=multi runtime-link=shared toolset=gcc include=%s library-path=%s install"%paths
        print cmd
        return subprocess.call(cmd) == 0
    def install(self):
        """ bjam configures, builds and installs so nothing to do here"""
        return self.build()

class ann(BaseProjectBuilder):
    download_name  = "ann_src.zip"
    archive_subdir = "ann*"
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        self.install_inc_dir = pj(self.installdir, "include")
        self.install_lib_dir = pj(self.installdir, "lib")
    def configure(self):
        """ bjam configures, builds and installs so nothing to do here"""
        return True
    def build(self):    
        return subprocess.call(cmd) == 0
    def install(self):
        """ bjam configures, builds and installs so nothing to do here"""
        return self.build()
        
################################################################################
# - EGG BUILDERS - EGG BUILDERS - EGG BUILDERS - EGG BUILDERS - EGG BUILDERS - #
################################################################################        
class egg_mingw_rt(BaseEggBuilder):
    __eggname__ = "mingw_rt"
    py_dependent   = False
    arch_dependent = True
    def script_substitutions(self):
        mgw = mingwrt()
        libdirs = {"bin":mgw.install_dll_dir}
        return dict( 
                    VERSION  = "5.1.4_3",
                    LIB_DIRS = libdirs,
                    )                

class egg_mingw(BaseEggBuilder):
    __eggname__ = "mingw"
    py_dependent   = False
    arch_dependent = True
    def script_substitutions(self):
        cpath = self.env.get_compiler_bin_path()
        mingwbase = pj(cpath,os.pardir)
        subd  = os.listdir( mingwbase )
        subd.remove("EGG-INFO")
        subd.remove("bin")
        subd.remove("include")
        data = []
        
        for dir in subd:
            dat = recursive_glob_as_dict(pj(mingwbase,dir), "*", strip_keys=True, prefix_key=dir).items()         
            data += [ (d, [f for f in t if not f.endswith(".dll")]) for d,t in dat]

        bindirs = {"bin": cpath}
        incdirs = {"include": pj(mingwbase, "include")}
            
        return dict( 
                    VERSION  = "5.1.4_3",
                    BIN_DIRS = bindirs,
                    INC_DIRS = incdirs,
                    DATA_FILES   = data,
                    )  
    
class egg_qt4(BaseEggBuilder):
    __eggname__ = "qt4"
    py_dependent   = True
    arch_dependent = True
    def script_substitutions(self):        
        qt4_   = qt4()
        pyqt4_ = pyqt4()
        pysci_ = pyqscintilla()
        sip_   = sip()
        # dlls are the union of qt dlls and plugins directories (which is actually the same!)
        # qscis apis are recursive from qt4 (need to list all files)        
        qscis    = recursive_glob_as_dict(pysci_.qsci_dir, Pattern.sciapi, strip_keys=True, prefix_key="qsci").items()
        sip_mods = recursive_glob_as_dict(sip_.install_site_dir, Pattern.pyall, strip_keys=True, levels=1).items()

        lib_dirs    = {"PyQt4": qt4_.install_dll_dir}
        package_dir = {"PyQt4": pj(pyqt4_.install_site_dir, "PyQt4"),
                       "PyQt4.uic": pj(pyqt4_.install_site_dir, "PyQt4", "uic")}
        
        from PyQt4 import Qt
        
        return dict( 
                    VERSION  = Qt.QT_VERSION_STR,
                    PACKAGES = ["PyQt4", "PyQt4.uic"],
                    PACKAGE_DIRS = package_dir,
                    PACKAGE_DATA = {'' : [Pattern.pyext]},
                    
                    LIB_DIRS         = lib_dirs,
                    DATA_FILES       = qscis+sip_mods,
                    INSTALL_REQUIRES = [egg_mingw_rt.__eggname__]
                    )  
                    
                 
class egg_qt4_dev(BaseEggBuilder):
    __eggname__ = "qt4_dev"
    py_dependent   = True
    arch_dependent = True
    def script_substitutions(self):
        qt4_   = qt4()
        pyqt4_ = pyqt4()
        sip_   = sip()
        # binaries are the union of qt, pyqt and sip binaries 
        bin_dirs = {"bin":qt4_.install_bin_dir}
        # includes are recursive subdirectories and the union of qt and sip includes               
        incs = recursive_glob_as_dict( qt4_.install_inc_dir, Pattern.qtinc, strip_keys=True, prefix_key="include", dirs=True).items() + \
               recursive_glob_as_dict( sip_.install_inc_dir, Pattern.qtinc, strip_keys=True, prefix_key="include", dirs=True).items()
        inc_dirs = merge_list_dict( incs )
        # libs are recursive subdirectories of qt libs          
        libs = recursive_glob_as_dict(qt4_.install_lib_dir, Pattern.qtstalib, strip_keys=True, prefix_key="lib").items()
        # sip files are recursive subdirectories and the union of pyqt4 and...
        sips = recursive_glob_as_dict(pyqt4_.install_sip_dir, Pattern.sipfiles, strip_keys=True, prefix_key="sip").items()
        # sources are recursive subdirectories and the union of qt4 and that all (CPP have been removed)...
        srcs = recursive_glob_as_dict(qt4_.install_src_dir, Pattern.qtsrc, strip_keys=True, prefix_key="src").items()
        # tra files are recursive subdirectories in qt4
        tra = recursive_glob_as_dict(qt4_.install_tra_dir, Pattern.qttransl, strip_keys=True, prefix_key="translations").items()
        # mks files are recursive subdirectories in qt4
        mks = recursive_glob_as_dict(qt4_.install_mks_dir, Pattern.qtmkspec, strip_keys=True, prefix_key="mkspecs").items()        
        # plugins files are recursive subdirectories in qt4
        plu = recursive_glob_as_dict(qt4_.install_plu_lib_dir, Pattern.qtstalib, strip_keys=True, prefix_key="plugins").items()        

        from PyQt4 import Qt
        
        return dict( 
                    VERSION  = Qt.QT_VERSION_STR,                   
                    BIN_DIRS         = bin_dirs,
                    INC_DIRS         = inc_dirs,
                    DATA_FILES       = libs+sips+srcs+tra+mks+plu,
                    INSTALL_REQUIRES = [egg_qt4.__eggname__]
                    )  
                    

class egg_pyqglviewer(BaseEggBuilder):
    __eggname__ = "pyqglviewer"
    py_dependent   = True
    arch_dependent = True
    def script_substitutions(self):
        qt4_   = qt4()
        qglv_   = qglviewer()
        pyqglv_   = pyqglviewer()
        
        pyqgl_mods = recursive_glob_as_dict(pyqglv_.install_site_dir, Pattern.pyall, strip_keys=True, levels=1).items()
        # includes are recursive subdirectories of qglviewer           
        incs = recursive_glob_as_dict( qglv_.install_inc_dir, Pattern.include, strip_keys=True, prefix_key="include", dirs=True).items()
        inc_dirs = merge_list_dict( incs )
        # libs are recursive subdirectories of qt libs          
        libs = recursive_glob_as_dict(qglv_.install_lib_dir, Pattern.qtstalib, strip_keys=True, prefix_key="lib").items()
        # sip files are recursive subdirectories of pyqglviewer sip installation directory
        sips = recursive_glob_as_dict(pyqglv_.install_sip_dir, Pattern.sipfiles, strip_keys=True, prefix_key="sip").items()
        # examples are recursive subdirectories of pyqglviewer examples installation directory contains various types of files
        exas = recursive_glob_as_dict(pyqglv_.install_exa_dir, Pattern.any, strip_keys=True, prefix_key="examples").items()        
        
        lib_dirs    = {"" : qglv_.install_dll_dir}
        data_files  = exas+sips+libs+pyqgl_mods
        
        import PyQGLViewer
        
        return dict( 
                    VERSION      = PyQGLViewer.QGLViewerVersionString(),                                  
                    PACKAGE_DATA = {'' : [Pattern.pyext]},
                    #PACKAGE_DIRS = package_dir,                    
                    LIB_DIRS     = lib_dirs,
                    INC_DIRS     = inc_dirs,
                    
                    DATA_FILES   = data_files,
                    INSTALL_REQUIRES = [egg_qt4.__eggname__]
                    )  
                    
class egg_boost(BaseEggBuilder):
    __eggname__ = "boost"
    version_re  = re.compile("^.*BOOST_VERSION\s:\s([\d\.]{4,8}).*$", re.MULTILINE|re.DOTALL)
    py_dependent   = True
    arch_dependent = True    
    def script_substitutions(self):
        boost_ = boost()
        qt4_   = qt4() # just to have the inc/lib regexp/glob patterns

        # includes are recursive subdirectories and the union of qt and sip includes               
        incs = recursive_glob_as_dict( boost_.install_inc_dir, Pattern.qtinc, strip_keys=True, prefix_key="include", dirs=True).items()
        inc_dirs = merge_list_dict( incs )
           
        # get the version from Jamroot file
        version = "UNKNOWN"        
        with open( pj(boost_.sourcedir, "Jamroot") ) as f:
            txt = f.read()
            se = self.version_re.search(txt)
            if se:
                version = se.groups()[0]
        lib_dirs    = {"lib": boost_.install_lib_dir}
        
        return dict( 
                    VERSION      = version,                 
                    LIB_DIRS         = lib_dirs,
                    INC_DIRS         = inc_dirs,
                    INSTALL_REQUIRES = [egg_mingw_rt.__eggname__]
                    )  

                    
############################################################
# The following egg builders require that you have the     #
# corresponding library installed. This is because they    #
# are too difficult to compile and that we don't actually  #
# need to compile them (no linkage from us to them)        #
# or that they come as .exes and not eggs already          #
############################################################
class InstalledPackageEggBuilder(BaseEggBuilder):
    __packagename__ = None
    def __init__(self):
        BaseEggBuilder.__init__(self)
        try:
            p = self.package
        except Exception, e:
            print e
            self.enabled = False
        else:
            self.enabled = True
    @property 
    def package(self):
        return __import__(self.packagename)
    @property
    def module(self):
        if self.__modulename__:
            return __import__(".".join([self.packagename,self.__modulename__]), fromlist=[self.__modulename__])
    @property 
    def packagename(self):
        return self.__packagename__ or self.__eggname__
    @property
    def install_dir(self):
        return os.path.dirname(self.package.__file__)

    def _filter_packages(self, pkgs):
        parpkg = self.packagename + "."
        return [ p for p in pkgs if (p == self.packagename or p.startswith(parpkg))]
        
    def find_packages(self):
        pkgs   = find_packages( pj(self.install_dir, os.pardir) )        
        pkgs = self._filter_packages(pkgs)
        return pkgs
        
    def find_packages_and_directories(self):
        pkgs = self.find_packages()
        dirs = {}
        base = abspath( pj(self.install_dir, os.pardir) )
        for pk in pkgs:
            dirs[pk] =  pj(base, pk.replace(".", os.sep))
        return pkgs, dirs
        
    def script_substitutions(self):        
        py_modules = recursive_glob(self.install_dir, Pattern.pymod)
        data_files = recursive_glob_as_dict(self.install_dir, 
                    ",".join(["*.example","*.txt",Pattern.pyext,"*.c",".1"])).items()                    
        packages, package_dirs = self.find_packages_and_directories()

        d = dict ( PACKAGES = packages,
                   PACKAGE_DIRS = package_dirs,
                   DATA_FILES  = data_files,
                  )        
        d.update(self.script_substitutions_2())
        return d
        
    def script_substitutions_2(self):    
        raise NotImplementedError
    
        
class egg_numpy(InstalledPackageEggBuilder):
    __eggname__ = "numpy"
    py_dependent   = True
    arch_dependent = True    
    def script_substitutions_2(self):
        return dict( VERSION = self.package.version.full_version )
        
class egg_scipy(InstalledPackageEggBuilder):
    __eggname__ = "scipy"
    py_dependent   = True
    arch_dependent = True        
    def script_substitutions_2(self):
        return dict( VERSION = self.package.version.full_version )
        
class egg_matplotlib(InstalledPackageEggBuilder):
    __eggname__ = "matplotlib"
    py_dependent   = True
    arch_dependent = True        
    def script_substitutions_2(self):        
        return dict( VERSION = self.package.__version__ )
                                               
class egg_PIL(InstalledPackageEggBuilder):
    __eggname__ = "PIL"
    __modulename__  = "Image"
    py_dependent   = True
    arch_dependent = True    
    def script_substitutions_2(self):
        return dict( VERSION = self.module.VERSION )
                 
class egg_pylsm(InstalledPackageEggBuilder):
    __eggname__ = "pylsm"
    py_dependent   = True
    arch_dependent = False
    
    @property 
    @with_original_sys_path
    def package(self):
        return __import__(self.packagename)
    
    def script_substitutions_2(self):
        pth = self.package.__path__[0]
        version = "UNKNOWN"
        for p in pth.split("\\"):
            if ".egg" in p:
                version = p.split("-")[1]+"_1" # we have a patched version
        return dict( VERSION = version )
                 
                 
                 
                 
                 
                 
                 
                 
                 
#################################
# -- MAIN LOOP AND RELATIVES -- #
#################################
def build_epilog():
    epilog = "PROJ_ACTIONS are a concatenation of flags specifying what actions will be done:\n"
    for proc, (funcname, skippable) in BaseProjectBuilder.all_procs.iteritems():
        if skippable:
            epilog += "\t%s : %s\n"%(proc, funcname.strip("_"))
    epilog += "\n"
    epilog += "EGG_ACTIONS are a concatenation of flags specifying what actions will be done:\n"
    for proc, (funcname, skippable) in BaseEggBuilder.all_procs.iteritems():
        if skippable:
            epilog += "\t%s : %s\n"%(proc, funcname.strip("_"))
    return epilog
    
def parse_arguments():
    parser = argparse.ArgumentParser(description="Build and package binary Openalea dependencies",
                                     epilog=build_epilog(),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,)
    parser.add_argument("--wdr", default=os.curdir, help="Under which directory we will create our working dir",
                        type=abspath)
            
    for proj in ProjectBuilders.builders.iterkeys():
        name = proj
        parser.add_argument("--"+name, default="", 
                            help="Force actions on %s"%name, dest=name,
                            metavar="PROJ_ACTIONS")

    for egg in EggBuilders.builders.iterkeys():
        name = "egg_"+egg
        parser.add_argument("--"+name, default="", 
                            help="Force actions on %s"%name, dest=name,
                            metavar="EGG_ACTIONS")
                            
    parser.add_argument("--login",  default=None, help="login to connect to GForge")
    parser.add_argument("--passwd", default=None, help="password to connect to GForge")
    parser.add_argument("--release", action="store_const", const=True, default=False, help="upload eggs to vplants repository for testing.")
    parser.add_argument("--verbose", action="store_const", const=True, default=False, help="upload eggs to vplants repository for testing.")
    return parser.parse_args()

def main():
    # set some env variables for subprocesses
    os.environ["MAKE_FLAGS"] = "-j2"

    args = parse_arguments()
    options = vars(args)

    env = BuildEnvironment()
    env.set_options(options)
    with env:
        env.build()
            
            

    
    
if __name__ ==  "__main__":
    main()