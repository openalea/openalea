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
__revision__ = " $Id$ "

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
import ctypes
import ConfigParser #used by project builders
from os.path import join as pj, splitext, getsize, exists, abspath, split
from collections import namedtuple, OrderedDict, defaultdict
from re import compile as re_compile

sj = os.pathsep.join

def uj(*args):
    return "/".join(args)

verbose = False



# Some utilities
pyver = sys.version_info[:2]

def is_64bits_host():
    # extend this to be multiplatform.
    # This is a hack to clearly identify if we are running
    # Python is a 64 bits Windows host. We don't use
    # platform.architecture because it returns "32" for
    # a 32 bits Python running in a 64 bits windows.
    # and "64" for a full 64 environment.
    # We don't use platform.machine() as it returns the processor
    # type and a 64 bits processor can run a 32 bits OS.
    return "PROGRAMFILES'(x86)" not in os.environ

def is_64bits_python():
    """Return True if the python that is running is 64 bits"""
    return "64" in platform.architecture()[0]

def get_python_dll():
    """ On windows, returns the location of the Python DLL.
    This should be
        C:\Windows\SysWOW64 for a 32 bits Python running in a 64 bits host
        C:\Windows\System32 for a NN bits Python running in a NN bits host
    However, we do NOT use hardcoded paths and rely on some CType power to
    retreive this information.

    Hum, WOW64 is complicated, as it redirects accesses to dlls. In both cases
    above, this function will return the same file *name*. But in the WOW case, on read,
    it will actually read the correct file.
    """
    nsize = 2048
    path = ctypes.create_unicode_buffer(nsize)
    py_path = ""
    if ctypes.windll.kernel32.GetSystemWow64DirectoryW(ctypes.pointer(path), nsize):
        py_path = ctypes.wstring_at(path)
    elif ctypes.windll.kernel32.GetSystemWindowsDirectoryW(ctypes.pointer(path), nsize):
        py_path = ctypes.wstring_at(path)
    else:
        raise OSError("Couldn't determine python%d%d.dll path"%pyver)
    return pj(py_path, u"python%d%d.dll"%pyver)

class Later(object):
    """ Just a way to be able to check if a process should be done later,
    and not mark it as done or failed (the third guy in a tribool)"""
    pass

class NullOutput(object):
    """A class that replace sys.stdout and that prints nothing"""
    def write(self, s):
        pass

# Some functions to strip away html tags from html documents.
# from http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
from HTMLParser import HTMLParser
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def download(url, easy_name, arch_path):
    def download_reporter(bk, bksize, bytes):
        if bytes == 0:
            raise urllib2.URLError("Url doesn't point to an existing resource.")
        progress= float(bk)/(bytes/bksize) * 100
        sys.stdout.write(("Dl %s to %s: %.1f %%"%(url, easy_name, progress))+"\r")
        sys.stdout.flush()

    # get the size of the ressource we're about to download
    remote_sz = float("inf")
    try:
        remote    = urllib.urlopen(url)
        # the content type shouldn' be text/*,
        # but application/*. text/* == error
        if remote.info().getheaders("Content-Type")[0].startswith("application"):
            remote_sz = int(remote.info().getheaders("Content-Length")[0])
        elif remote.info().getheaders("Content-Type")[0].startswith("text/html"):
            raise IOError( strip_tags(remote.read()) )
        else:
            raise IOError( remote.read() )
    except IOError:
        traceback.print_exc()
        return False
    finally:
        remote.close()

    ret = True
    try:
        #raises os.error if arch_path doesn't exist
        local_sz = getsize(arch_path)
        # download is incomplete, raise error to download
        if local_sz<remote_sz :
            raise os.error
    except os.error:
        try:
            urllib.urlretrieve(url, arch_path, download_reporter)
        except:
            traceback.print_exc()
            ret = False
    return ret

def unpack(arch, where):
    arch = arch
    base, ext = splitext( arch )
    print "unpacking", arch
    # TODO : verify that there is no absolute path inside zip.
    if ext == ".zip":
        zipf = zipfile.ZipFile( arch, "r" )
        zipf.extractall( path=where )
    elif ext == ".tgz":
        tarf = tarfile.open( arch, "r:gz")
        tarf.extractall( path=where )
    elif ext == ".tar":
        tarf = tarfile.open( arch, "r")
        tarf.extractall( path=where )
    print "done"
    return True

##################################
# File list digging and mangling #
##################################
def merge_list_dict(li):
    """ Converts li which is a list of (key,value) into
    a dictionnary where items with the same keys get appended
    to a list instead of overwriting the key."""
    d = defaultdict(list)
    for k, v in li:
        d[k].extend(v)
    return dict( (k, sj(v)) for k,v in d.iteritems() )

CompiledRe = type(re_compile(""))
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


###############
# METACLASSES #
###############

# Every class further on is a MSingleton. Hum, maybe this is bad-design.
 # - The base MSingleton metaclass is just that: a metaclass that converts
   # the classes that use it into Singletons
 # - The (MProject|MEgg)Builders metaclasses are also singleton metaclasses
   # but they act as registries for the classes that use them.
   # The classes are stored in the M(Project|Egg)Builders.builders dicts.
   # These dicts are referred to in the build_proj function

class MSingleton(type):
    """ Singleton Metaclass."""
    def __init__(cls, name, bases, dic):
        type.__init__(cls, name, bases, dic)
        cls.instance=None
    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance=type.__call__(cls, *args, **kw)
        return cls.instance

class MProjectBuilders(MSingleton):
    """ A Project Builder registry and MSingleton Metaclass."""
    builders = OrderedDict()
    def __init__(cls, name, bases, dic):
        MSingleton.__init__(cls, name, bases, dic)
        if name != "BaseProjectBuilder":
            MProjectBuilders.builders[name] = cls
    @classmethod
    def get(cls, item):
        return MProjectBuilders.builders[item]

class MEggBuilders(MSingleton):
    """ An Egg Builder registry and MSingleton Metaclass."""
    builders = OrderedDict()
    def __init__(cls, name, bases, dic):
        MSingleton.__init__(cls, name, bases, dic)
        if name not in ["BaseEggBuilder", "InstalledPackageEggBuilder"]:
            MEggBuilders.builders[name] = cls
    @classmethod
    def get(cls, item):
        return MEggBuilders.builders[item]




#############################
# A micro build environment #
#############################
class Compiler(object):
    __metaclass__ = MSingleton

    def set_options(self, options):
        self.options = options.copy()
    
    # Obtaining Compiler Info - We only want MINGW-family compiler
    def ensure_has_mingw_compiler(self):
        try:
            subprocess.call("gcc --version")
        except WindowsError:
            print "No MingW compiler found, you can specify its path with -c"
            print "or install a default MingW compiler."
            install = raw_input("Install a default MingW? (Y/N). :")
            if install.lower() == "y":
                self.install_compiler()
            else:
                print "Cannot compile, continuing anyway..."
                    
    def install_compiler(self):
        print "Will now install a default 32 bits MingW compiler to c:\mingw"
        print "Make sure you have to rights to do so and that the directory does NOT exist"
        if raw_input("Proceed? (Y/N):").lower() == "y":
            archpath = pj(BE.working_path, "mingw.zip")
            if download("https://gforge.inria.fr/frs/download.php/29029/MinGW-5.1.4_2-win32.egg",
                     "mingw.zip",
                     archpath):
                if not unpack(archpath, "c:\mingw"):
                    print "Couldn't install MingW32, continuing anyway..."
            
                     

    def get_compiler_bin_path(self):
        # TODO : do smart things according to self.options
        if self.options["compiler"]:
            return self.options["compiler"]

        # -- try to find it in eggs --
        try:
            from pkg_resources import Environment
            from distutils.sysconfig import get_python_lib
            env  = Environment()
            base = get_python_lib().lower()
            # this works in virtualenvs
            for f in env["mingw"]:
                if f.location.lower().startswith(base):
                    return pj(f.location, "bin")
            raise Exception("Mingw not found")
        except Exception, e:
            print e
            return r"c:\mingw\bin"

    def is_tdm_compiler(self):
        """Return True if we are using a compiler from tdm-gcc.tdragon.net/"""
        pop = subprocess.Popen( pj(self.get_compiler_bin_path(), "gcc --version"),
                                           stdout=subprocess.PIPE)
        time.sleep(1) #give enough time for executable to load before it asks for license agreement.
        output = pop.stdout.read()
        return "(tdm"  in output
# Shortcut:
Comp = Compiler()
    
    
    
class BuildEnvironment(object):
    __metaclass__ = MSingleton

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
        Comp.set_options(options)
        self.init()

    def init(self):
        self.working_path = pj( self.options.get("wdr"), self.get_platform_string() )
        self.proc_file_path = pj(self.working_path,"proc_flags.pk")
        self.create_working_directories()
        recursive_copy( split(__file__)[0], self.working_path, "setup.py.in", levels=1)
        recursive_copy( split(__file__)[0], self.working_path, "qmake_main.cpp.sub", levels=1)
        self.__fix_environment()
        self.__fix_sys_path()

        if self.options["bits"] == 64:
            if not is_64bits_host():
                print "Building for Win64 can only be done on a 64 bits host."
                print "Indeed, we cannot cross compile from 32bits host as "
                print "generated 64bits executables are used during compilation."
                raise Exception("Could not continue compilation for 64 bits release")
            if not is_64bits_python():
                print "Building for Win64 can only be done using 64 bits Python."
                print "Indeed, some linking is done with the Python in use."
                raise Exception("Could not continue compilation for 64 bits release")
            # if not Comp.is_tdm_compiler():
                # print "Building for Win64 can currently only be done using TDM-GCC compilers."
                # raise Exception("Could not continue compilation for 64 bits release")

    # -- context manager protocol --
    def __enter__(self):
        try:
            with open(self.proc_file_path, "rb") as f:
                txt  = f.read()
                self.done_tasks = eval(txt)
        except:
            print "%s not found, let's start from the very beginning"%self.proc_file_path
            self.done_tasks = {}

    def __exit__(self, exc_type, exc_value, traceback):
        with open(self.proc_file_path, "wb") as f:
            pprint.pprint(self.done_tasks, f)

    # -- Project building --
    def __init_builders(self):
        self.proj_builders = list(MProjectBuilders.builders.itervalues())
        self.egg_builders  = list(MEggBuilders.builders.itervalues())

    def build(self):
        only = self.options.get("only")
        self.__init_builders()
        for buildercls in self.proj_builders + self.egg_builders:            
            builder = buildercls()
            if builder.has_pending and builder.enabled:
                if (only is None) or (builder.name == only):
                    builder.process_me()

    def task_is_done(self, name, task):
        """ Marks that the `task` step has been accomplished for `proj`.
         - name is a key from M(Project|Egg)Builders.builders
         - task is a task identifier
        """
        if task not in self.done_tasks.setdefault(name, ""):
            self.done_tasks[name] += task

    def is_task_done(self, name, task):
        """ Tells is a task is finished. """
        return task in self.done_tasks.setdefault(name, "")

    def is_task_forced(self, name, task):
        """ Tells is the user forced this task. """
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

    def __fix_environment(self):
        # TODO : Clean env so that we do not propagate preexisting installations in subprocesses
        # give priority to OUR compiler!
        os.environ["PATH"] = sj([Comp.get_compiler_bin_path(), os.environ["PATH"]])
        self.ensure_python_lib()

    def __fix_sys_path(self):
        """Clean sys.path for this process so that we don't import
        existing eggs or site-installed thingys."""
        our_egg_names = [name.strip("egg_") for name in MEggBuilders.builders.iterkeys()]
        for pth in sys.path[:] :
            pth_p = pth.lower()
            for egg_name in our_egg_names:
                if egg_name in pth_p:
                    sys.path.remove(pth)
                    break

    def ensure_python_lib(self):
        """Checks that libpythonXY.a exists.
        On Win64 python only ships with pythonXY.lib (MSVC)"""
        dst = pj(sys.prefix, "libs", "libpython%d%d.a"%pyver)
        dstdef = pj(sys.prefix, "python%d%d.def"%pyver)
        src = get_python_dll()

        if not exists( dst ):
            if exists( src ):
                print "Using PExports to create %s"%dst
                if not os.system( "pexports.exe %s > %s"%(src, dstdef) ):
                    if not os.system("dlltool -U -d %s -l %s"%(dstdef, dst) ):
                        print "Created %s"%dst
                    else:
                        raise Exception("Can't create %s, dlltool error: Python link will fail"%dst)
                else:
                    raise Exception("Can't create %s, pexports error: Python link will fail"%dst)
            else:
                raise Exception("Can't create %s, %s not found: Python link will fail"%(dst,src))
        else:
            print "Python lib is ok"
#a shorthand:
BE=BuildEnvironment()



############################################
# A few decorators to factor out some code #
############################################
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
    wrapper.__name__ = f.__name__
    return wrapper

def in_dir(directory):
    def dir_changer( f ) :
        """Encapsulate f in a structure that changes to getattr(self,directory),
        calls f and moves back to BuildEnvironment.get_working_path()"""
        def wrapper(self, *args, **kwargs):
            d_ = getattr(self, directory)
            print "changing to", d_, "for", f.__name__
            os.chdir(d_)
            ret = f(self, *args, **kwargs)
            os.chdir(self.env.get_working_path())
            return ret
        wrapper.__name__ = f.__name__
        return wrapper
    return dir_changer

def with_original_sys_path(f):
    def func(*args,**kwargs):
        cursyspath = sys.path[:]
        sys.path = BaseEggBuilder.__oldsyspath__[:]
        ret = f(*args, **kwargs)
        sys.path = cursyspath
        return ret
    return func




########################
# Builder Base classes #
########################
class BaseBuilder(object):
    #string of task ids that this particular builder supports (eg. "duf")
    supported_tasks = ""
    #OrderedDict mapping of
    # task id and (the name of the method to call, task can be skipped boolean)
    all_tasks       = None
    #string of tasks for which stdout can be decently swallowed
    silent_tasks    = ""
    #if is false, won't be processed.
    enabled         = True

    def __init__(self):
        self.env = BE
        self.pending = None
    @property
    def name(self):
        return self.__class__.__name__
    @property
    def options(self):
        return self.env.options
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
        for task in self.supported_tasks:
            task_func, skippable = self.all_tasks[task]
            done   = self.env.is_task_done(name, task)
            forced = self.env.is_task_forced(name, task)
            skip = done and not forced and skippable
            if not skip:
                tasks.append((task, task_func, skippable))
        self.pending = tasks

    def __has_pending_verbose_tasks(self):
        for task, func, skippable in self.pending:
            if task not in self.silent_tasks:
                return True
        return False

    def process_me(self):
        self.env.make_silent( not self.__has_pending_verbose_tasks() )

        proc_str  = "PROCESSING " + self.name
        print "\n",proc_str
        print "="*len(proc_str)
        # forced_tasks is a string containing self.all_tasks keys.
        # if a process is in forced_tasks it gets forced.
        forced_tasks = self.options.get(self.name, "")
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
    __metaclass__ = MProjectBuilders

    # The URL to fetch the sources from
    # A None url implies the download has already done by someone else
    url = None
    # Name of the  local archive
    download_name  = None
    # If the unpacked archive has subdirectories to go through
    # before we reach the source, use a glob here:
    archive_subdir = None
    # Task management:
    all_tasks       = OrderedDict([ ("d",("download_source",True)),
                                    ("u",("unpack_source",True)),
                                    ("f",("fix_source_dir",False)),
                                    ("c",("_configure",True)),
                                    ("b",("_build",True)),
                                    ("i",("_install",True)),
                                    ("p",("_patch", True)), #where should you be?
                                    ("x",("_extend_sys_path",False)),
                                    ("y",("_extend_python_path",False)),
                                    ("n",("_new_env_vars",False)),
                                    ])
    # swallow stdout for these tasks:
    silent_tasks    = "fxy"
    # Only execute these tasks:
    supported_tasks = "".join(all_tasks.keys())

    def __init__(self):
        BaseBuilder.__init__(self)
        self.archname  = pj( self.env.get_dl_path() , self.download_name)
        self.sourcedir = pj( self.env.get_src_path(), splitext(self.download_name)[0] )
        self.installdir = pj( self.env.get_install_path(), splitext(self.download_name)[0] )

    def download_source(self):
        def download_reporter(bk, bksize, bytes):
            if bytes == 0:
                raise urllib2.URLError("Url doesn't point to an existing resource.")
            progress= float(bk)/(bytes/bksize) * 100
            sys.stdout.write(("Dl %s to %s: %.1f %%"%(self.url, self.download_name, progress))+"\r")
            sys.stdout.flush()

        # a proj with a none url implicitely means
        # the sources are already here because some
        # other proj installed it.
        if self.url is None:
            return True
        
        return download(self.url, self.download_name, self.archname)
        
        # get the size of the ressource we're about to download
        remote_sz = float("inf")
        try:
            remote    = urllib.urlopen(self.url)
            # the content type shouldn' be text/*,
            # but application/*. text/* == error
            if remote.info().getheaders("Content-Type")[0].startswith("application"):
                remote_sz = int(remote.info().getheaders("Content-Length")[0])
            elif remote.info().getheaders("Content-Type")[0].startswith("text/html"):
                raise IOError( strip_tags(remote.read()) )
            else:
                raise IOError( remote.read() )
        except IOError:
            traceback.print_exc()
            return False
        finally:
            remote.close()

        ret = True
        try:
            #raises os.error if self.archname doesn't exist
            local_sz = getsize(self.archname)
            # download is incomplete, raise error to download
            if local_sz<remote_sz :
                raise os.error
        except os.error:
            try:
                urllib.urlretrieve(self.url, self.archname, download_reporter)
            except:
                traceback.print_exc()
                ret = False
        return ret

    def unpack_source(self, arch=None):
        # a proj with a none url implicitely means
        # the sources are already here because some
        # other proj installed it.
        if self.url is None:
            return True
        if exists(self.sourcedir):
            return True
        arch = arch or self.archname
        return unpack(arch, self.sourcedir)
        
        base, ext = splitext( arch )
        print "unpacking", arch
        # TODO : verify that there is no absolute path inside zip.
        if ext == ".zip":
            zipf = zipfile.ZipFile( arch, "r" )
            zipf.extractall( path=self.sourcedir )
        elif ext == ".tgz":
            tarf = tarfile.open( arch, "r:gz")
            tarf.extractall( path=self.sourcedir )
        elif ext == ".tar":
            tarf = tarfile.open( arch, "r")
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

    def _new_env_vars(self):
        exp = self.new_env_vars()
        if exp is not None:
            os.environ.update(exp)
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
    def new_env_vars(self):
        return None
    def configure(self):
        raise NotImplementedError
    def build(self):
        cmd = "mingw32-make -j " + str(self.options["jobs"])
        print cmd
        return subprocess.call( cmd ) == 0
    def patch(self):
        return True
    def install(self):
        return subprocess.call("mingw32-make install") == 0



class TemplateStr(string.Template):
    delimiter = "@"

class BaseEggBuilder(BaseBuilder):
    __metaclass__  = MEggBuilders
    __oldsyspath__ = sys.path[:]
    # The egg depends on the Python version (allows correct egg naming)
    py_dependent   = True
    # The egg depends on the os and processor type (allows correct egg naming)
    arch_dependent = True
    # Task management:
    all_tasks       = OrderedDict([("c",("_configure_script",True)),
                                   ("e",("_eggify",True)),
                                   ("u",("_upload_egg",True))
                                  ])
    # Only execute these tasks:
    supported_tasks = "".join(all_tasks.keys())

    def __init__(self,**kwargs):
        BaseBuilder.__init__(self, **kwargs)
        if "no_env" in kwargs:
            self.eggdir         = ""
            self.setup_in_name  = ""
        else:
            self.eggdir         = pj(self.env.get_egg_path(), self.egg_name())
            self.setup_in_name  = pj(self.env.get_working_path(), "setup.py.in")
        self.setup_out_name = pj(self.eggdir, "setup.py")
        self.use_cfg_login  = False
        makedirs(self.eggdir)

        self.default_substitutions = dict( NAME      = self.egg_name(),
                                           VERSION   = "1.0",
                                           THIS_YEAR = datetime.date.today().year,
                                           SETUP_AUTHORS = "Openalea Team",
                                           CODE_AUTHOR   = self.authors,
                                           DESCRIPTION   = self.description,
                                           URL           = "",
                                           LICENSE       = self.license,

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
    @classmethod
    def egg_name(cls):
        return cls.__name__.strip("egg_")

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
                    self.egg_name(), "\"ThirdPartyLibraries\"", "vplants" if not self.options["release"] else "openalea"
            return subprocess.call(sys.executable + " setup.py egg_upload --yes-to-all --login %s --password %s --release %s --package %s --project %s"%opts) == 0
        else:
            opts = self.egg_name(), "\"ThirdPartyLibraries\"", "vplants" if not self.options["release"] else "openalea"
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
    qtinc    = re_compile(r"^Q[0-9A-Z]\w|.*\.h")
    qtmkspec = "*"
    qttransl = "*.qm"

############################################################
# The following egg builder requires that you have the     #
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
            print self.name, "disabled:", e
            self.enabled = False
        else:
            self.enabled = True
    @property
    def package(self):
        return __import__(self.packagename)
    @property
    def module(self):
        if self.__modulename__:
            return __import__(".".join([self.packagename,self.__modulename__]), 
                              fromlist=[self.__modulename__])
    @property
    def packagename(self):
        return self.__packagename__ or self.egg_name()
    @property
    def install_dir(self):
        return os.path.dirname(self.package.__file__)

    def _filter_packages(self, pkgs):
        parpkg = self.packagename + "."
        return [ p for p in pkgs if (p == self.packagename or p.startswith(parpkg))]

    def find_packages(self):
        from setuptools import find_packages
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











#################################
# -- MAIN LOOP AND RELATIVES -- #
#################################
def build_epilog():
    epilog = "PROJ_ACTIONS are a concatenation of flags specifying what actions will be done:\n"
    for proc, (funcname, skippable) in BaseProjectBuilder.all_tasks.iteritems():
        if skippable:
            epilog += "\t%s : %s\n"%(proc, funcname.strip("_"))
    epilog += "\n"
    epilog += "EGG_ACTIONS are a concatenation of flags specifying what actions will be done:\n"
    for proc, (funcname, skippable) in BaseEggBuilder.all_tasks.iteritems():
        if skippable:
            epilog += "\t%s : %s\n"%(proc, funcname.strip("_"))

    epilog += "\nBy default, building rules will be read from project_rules.py and egg_rules.py_dependent\n"
    epilog += "You can specify your own by using --prules <filename> and --erules <filename> .\n"

    return epilog

def parse_arguments():
    parser = argparse.ArgumentParser(description="Build and package binary Openalea dependencies",
                                     epilog=build_epilog(),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,)
    parser.add_argument("--wdr", default=abspath(os.curdir), help="Under which directory we will create our working dir",
                        type=abspath)

    for proj in MProjectBuilders.builders.iterkeys():
        name = proj
        parser.add_argument("--"+name, default="",
                            help="Force actions on %s"%name, dest=name,
                            metavar="PROJ_ACTIONS")

    for egg in MEggBuilders.builders.iterkeys():
        name = egg
        parser.add_argument("--"+name, default="",
                            help="Force actions on %s"%name, dest=name,
                            metavar="EGG_ACTIONS")

    parser.add_argument("--python", "-p", default=None, help="fully qualified python executable to use for the compilation")
    parser.add_argument("--compiler", "-c", default=None, help="path to compiler binaries")
    parser.add_argument("--only", "-o", default=None, help="Only process this project/egg")
    parser.add_argument("--jobs", "-j", default=1, type=int, help="number of jobs during compilation")
    parser.add_argument("--bits", default=64 if is_64bits_python() else 32, type=int, choices=[32, 64], help="32 or 64 bits build")
    parser.add_argument("--login",  default=None, help="login to connect to GForge")
    parser.add_argument("--passwd", default=None, help="password to connect to GForge")
    parser.add_argument("--release", action="store_const", const=True, default=False, help="upload eggs to openalea repository or vplants (if False - for testing).")
    parser.add_argument("--verbose", action="store_const", const=True, default=False, help="Well try to say more things.")
    return parser.parse_args()

def main():
    #default building rules
    proj_rules_file = pj(split(__file__)[0],"project_rules.py")
    egg_rules_file  = pj(split(__file__)[0],"egg_rules.py")
    # if any rules are given as arguments parse those first
    # or else the parse_arguments function won't build the
    # parser correctly
    if "--prules" in sys.argv:
        proj_rules_file = sys.argv[ sys.argv.index("--prules") + 1 ]
        if not exists(proj_rules_file):
            raise Exception("No such project rule file : %s"%proj_rules_file)
        sys.argv.remove("--prules")
        sys.argv.remove(proj_rules_file)
    if "--erules" in sys.argv:
        egg_rules_file = sys.argv[ sys.argv.index("--erules") + 1 ]
        if not exists(egg_rules_file):
            raise Exception("No such egg rule file : %s"%egg_rules_file)
        sys.argv.remove("--erules")
        sys.argv.remove(egg_rules_file)

    with open(proj_rules_file) as f:
        proj_rules = eval(compile(f.read(), proj_rules_file, "exec"), globals())
    with open(egg_rules_file) as f:
        egg_rules  = eval(compile(f.read(), egg_rules_file, "exec"), globals())

    args = parse_arguments()
    # set some env variables for subprocesses
    os.environ["MAKE_FLAGS"] = "-j"+str(args.jobs)

    if args.python is not None:
        python = args.python
        del args.python #or else we will nevert start!
        arg_str = reduce( lambda x,y: x + (" --"+y[0]+"="+str(y[1]) if y[1] else ""), args._get_kwargs(), pj(os.getcwd(), __file__) )
        # cannot use subprocess, spawn or exec : if we run a 32 python on a 64 bits machine
        # and ask to use a 64 bits python, WoW (which is executing the 32 bits process)
        # will fail to run the 64 bits Python as a subprocess
        os.system(python + " " + arg_str)
    else:
        options = vars(args)
        env = BuildEnvironment()
        env.set_options(options)
        Comp.ensure_has_mingw_compiler()
        with env:
            env.build()





if __name__ ==  "__main__":
    main()