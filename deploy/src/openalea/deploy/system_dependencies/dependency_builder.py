# -*- python -*-
#
#       openalea.deploy.dependency_builder
#
#       Copyright 2006-2012 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau
#       File Contributors(s):
#                             - Yassin Refahi,
#                             - Frederic Boudon,
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
import threading
import pprint
import fnmatch
import re
import string
import argparse
import datetime
import zipfile
import tarfile
import ctypes
import patch
import ConfigParser #used by some project builders
from os.path import join as pj, splitext, getsize, exists, abspath, split, dirname, realpath
from collections import namedtuple, OrderedDict, defaultdict
from re import compile as re_compile

#################################
# Some Utilities - Path Joining #
#################################
# Native Path Joining function:
sj = os.pathsep.join

def uj(*args):
    """Unix-style path joining, useful when working with qmake."""
    return "/".join(args)


############################
# Some Utilities - Globals #
############################
exe_ext = ".exe" if "win32" in sys.platform else ""

# Major and Minor python version numbers:
pyver = sys.version_info[:2]

# A file object to redirect output to NULL:
NullOutput = open("NUL", "w")

# A variable that stores the absolute path to this file:
ModuleBaseDir = abspath(dirname(__file__))

class Later(object):
    """ Just a way to be able to check if a process should be done later,
    and not mark it as done or failed (the third guy in a tribool)"""
    pass

def rgetattr(c, attrs):
    """Like getattr, except that you can provide sub attributes:

    >>> rgetattr(obj, "attr.subattr")
    """
    attrs = attrs.split(".")
    value = c
    while len(attrs):
        value = getattr(value, attrs.pop(0))
    return value

################################
# Some Utilities - System Info #
################################
def is_64bits_host():
    # TODO : extend this to be multiplatform.
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

def get_python_scripts_dirs():
    dirs = []
    for pth in sorted(sys.path):
        pth = [part for part in pth.split(os.sep)]
        try:
            pth_low = [part.lower() for part in pth]
            idx = pth_low.index("lib")
        except:
            continue
        else:
            script_dir_name = "scripts" if sys.platform == "win32" else "bin"
            script_path = pj(*pth[:idx]+[script_dir_name])
            # sys.path contains absolute namesso the split operation above has to
            # be compensated:
            if sys.platform == "win32":
                # restore "driveletter:\\" on windows
                script_path = script_path.replace(":", ":"+os.sep)            
            else:
                # restore "/" on unixes
                script_path = "/"+script_path
            if script_path not in dirs:
                dirs.append(script_path)
    return dirs

###############################
# Some Utilities - Networking #
###############################
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

def into_subdir(base, pattern):
    if pattern is not None:
        pths = glob.glob(pj(base,pattern))
        if len(pths):
            return pths[0]
        else:
            return None
    else:
        return base

def download(url, easy_name, arch_path):
    def download_reporter(bk, bksize, bytes):
        if bytes == 0:
            raise urllib2.URLError("Url doesn't point to an existing resource.")
        progress= float(bk)/(bytes/bksize) * 100
        presentation_url = url[:]
        if len(presentation_url) >= 100:
            presentation_url = url[:25]+"[...]"+url[-25:]
        sys.stdout.write(("Dl %s to %s: %.1f %%"%(presentation_url, easy_name, progress))+"\r")
        sys.stdout.flush()

    # get the size of the ressource we're about to download
    remote_sz = float("inf")
    try:
        remote    = urllib.urlopen(url)
        # the content type shouldn' be text/*,
        # but application/*. text/* == error
        if remote.info().getheaders("Content-Type")[0].startswith("application"):
            c_len = remote.info().getheaders("Content-Length")
            if len(c_len):
                remote_sz = int(remote.info().getheaders("Content-Length")[0])
            else:
                print "Unknown content length, cannot determine if download can be skipped..."
                remote_sz = float("inf")
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

#####################
# Playing with eggs #  
#####################
try:
    from setuptools.package_index import PackageIndex
    from openalea.deploy.gforge_util import add_private_gforge_repositories
    from openalea.deploy.util import get_repo_list
    from distutils import log

    pi = PackageIndex(search_path=[])
    pi.add_find_links(get_repo_list())
    can_egg_download = True
except:
    can_egg_download = False
    
def download_egg(eggname, dir_):
    """Download an egg to a specific place"""
    if can_egg_download:
        print "Downloading %s"%eggname
        if BE.options.get("gforge"):
            add_private_gforge_repositories(BE.options.get("login"), BE.options.get("passwd"))
        log.set_verbosity(1)
        return pi.download(eggname, dir_)
    else:
        print "Oups: Egg download in not available cause setuptools (or distribute) is not installed"
        return False

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
    """Recursively globs files and returns a list of the globbed files.
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


def apply_patch(patchfile):
    p = patch.fromfile(patchfile)
    p.apply()


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

def create_metabuilder(mname):
    class innerclass(MSingleton):
        """A %s registry and MSingleton Metaclass."""%mname
        ez_name = mname.lower()
        bases   = []
        builders = OrderedDict()
        def __init__(cls, name, bases, dic):
            MSingleton.__init__(cls, name, bases, dic)
            if object in bases:
                innerclass.bases.append(cls)
            else:
                innerclass.builders[name] = cls
        @classmethod
        def get(cls, item):
            return innerclass.builders[item]
    innerclass.__name__ = "M%s"%mname
    return innerclass

MProject = create_metabuilder("Project")
MEgg     = create_metabuilder("Egg")

class MTool(MSingleton):
    def __init__(cls, name, bases, dic):
        MSingleton.__init__(cls, name, bases, dic)
        if object not in bases:
            cls.cmd_options = cls.cmd_options or []
            cls.cmd_options.insert(0, (name, None, "Path to "+ (cls.exe or name+".exe") ) )
            if cls.installable:
                cls.arch_name   = name+"."+cls.arch_name_ext

def memoize(attr):
    def deco_memoize(f):
        def wrapper(self, *args, **kwargs):
            if getattr(self, attr, None) is None:
                v = f(self, *args, **kwargs)
                setattr(self, attr, v)
            return getattr(self, attr)
        return wrapper
    return deco_memoize


#############################
# A micro build environment #
#############################
class Tool(object):
    __metaclass__ = MTool

    class PyExecPaths(object):
        """Include this symbol in the default_paths
        list to add the python "scripts" folder to
        the search list"""
        pass

    class OriginalSystemPaths(object):
        """Include this symbol in the paths listes in %PATH%
        to the search list"""
        pass

    # If this is not true, there will be no attempt
    # to install the tool if it hasn't been found
    installable = True

    # URL at which we can download
    # a release of the tool.
    url = None

    # extension of the downloaded archive.
    # the extension determines the unpacker to use.
    arch_name_ext = None

    # a glob pattern to move into subdirectories
    archive_subdir = None

    # Executable that can be called to test for availability
    exe = None

    # Places to look for the exe by default.
    default_paths = None

    # if not None, it is then a list of triplets specifying additionnal
    # command line options that are needed for this package.
    # the MTool metaclass will automatically add a self.name+"_path"
    # command line to this list.
    cmd_options = None

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def options(self):
        return BE.options

    @memoize("path")
    def get_path(self, no_install=False):
        verbose = BE.verbose
        if verbose:
            print "Looking for %s path"%self.name
        pth = self._get_path(no_install)
        if pth and verbose:
            print "\tGot it:", pth
        return pth

    def _get_path(self, no_install=False):
        #NOTE:
        #The BuildEnvironment class cleans the PATH.
        #no need to look into that variable.

        def pth_test(pth):
            exe_path = pj(pth, self.exe)
            if exists(exe_path):
                # see if we can actually call it
                try:
                    subprocess.call(exe_path, stdout=NullOutput, stderr=NullOutput)
                except OSError:
                    print "\tCalling", exe_path, "failed: bad path"
                    return False
                else:
                    return True
            return False

        # First look at the user provided command line option.
        pth = self.options[self.name]
        if pth is not None:
            if pth_test(pth):
                return pth

        # Look in default_paths:
        if self.default_paths is None or not len(self.default_paths):
            print "\tNo default paths given, skipping"
        else:
            # 1) - Expand PyExecPaths and OriginalSystemPaths placeholders
            if Tool.PyExecPaths in self.default_paths:
                self.default_paths.remove(Tool.PyExecPaths)
                self.default_paths.extend(get_python_scripts_dirs())
            if Tool.OriginalSystemPaths in self.default_paths:
                self.default_paths.remove(Tool.OriginalSystemPaths)
                self.default_paths.extend(BE.original_path.split(os.pathsep))
            # 2) - Do the lookup (might be possible to speed things up later on)
            for pth in self.default_paths:
                matches = glob.glob( pth )
                if len(matches):
                    matches.sort()
                    pth = matches[-1] # -1 is supposed toget highest version
                    if pth_test(pth):
                        return pth

        if not self.installable or no_install:
            return False

        # Is it installed locally?
        wp = BE.get_working_path()
        archpath = pj(wp, self.arch_name)
        toolpath = pj(wp, self.name)

        pth = into_subdir(toolpath, self.archive_subdir)
        if pth is not None:
            if pth_test(pth):
                return pth

        # Haven't found it yet, let's install it in wdr
        if self.url is None:
            print "\tNo url to download tool from, skipping"
            return None
        if not self.__prompt_user():
            print "\tUser refused download"
            return None

        print "\tWill now install %s to %s"%(self.name, wp)
        if not download(self.url, self.arch_name, archpath):
            print "\tCouldn't download", self.name
            return None
        if not unpack(archpath, toolpath):
            print "\tCouldn't unpack", self.name
            return None

        pth = into_subdir(toolpath, self.archive_subdir)
        return pth if pth_test(pth) else None

    def __prompt_user(self):
        """Prompt the user for download, wait 5 seconds and download if no input"""
        do_dl = None
        delay = 5000
        def ask_user_if_download():
            try:
                do_dl = raw_input().lower() == "y"
            except:
                do_dl = True

        prompt = "\tLocally install %s (%s seconds)? (y/n, default:y): \r"
        def print_prompt():
            sys.stdout.write(prompt%(self.name, delay))
            sys.stdout.flush()

        thInput = threading.Thread(target=ask_user_if_download)
        thInput.start()
        while delay > 0 and do_dl is None:
            if delay%1000==0:
                print_prompt()
            delay -= 1
            time.sleep(1/1000)
        thInput._Thread__stop()
        if do_dl is None:
            do_dl = True
        return do_dl



class Compiler_(object):
    __metaclass__ = MSingleton

    default_32_comp = "https://gforge.inria.fr/frs/download.php/29029/MinGW-5.1.4_2-win32.egg"

    def __init__(self):
        self.options={}
    
    def set_options(self, options):
        self.options = options.copy()

    # Obtaining Compiler Info - We only want MINGW-family compiler
    def ensure_has_mingw(self):
        try:
            compiler = os.path.join(self.get_bin_path(),"gcc.exe")

            subprocess.call(compiler+" --version", stdout=NullOutput)
        except OSError, e:
            print e
            print "No MingW compiler found, you can specify its path with -c"
            print "or install a default MingW compiler."
            if raw_input("Install a default MingW? (Y/N). :").lower() == "y":
                self.install()
            else:
                print "Cannot compile, continuing anyway..."

    def install(self):
        print "Will now install a default 32 bits MingW compiler to c:\mingw"
        print "Make sure you have to rights to do so and that the directory does NOT exist"
        if raw_input("Proceed? (Y/N):").lower() == "y":
            ez_name  = "mingw.zip"
            archpath = pj(BE.working_path, ez_name)
            if download(default_32_comp, ez_name, archpath):
                if not unpack(archpath, "c:\\mingw"):
                    print "Couldn't install MingW32, continuing anyway..."

    @memoize("comp_bin_path")
    def get_bin_path(self):
        # TODO : do smart things according to self.options
        if "win32" not in sys.platform:
            return "/usr/bin"
        if self.options.get("compiler"):
            v =  self.options["compiler"]
            if os.path.exists(v):
                return v

        # -- try to find it in eggs --
        try:
            from pkg_resources import Environment
            from distutils.sysconfig import get_python_lib
            env  = Environment()
            base = get_python_lib().lower()
            # this works in virtualenvs
            for f in env["mingw"]:
                if f.location.lower().startswith(base):
                    v = pj(f.location, "bin")
            raise Exception("Mingw not found")
        except Exception, e:
            v = r"c:\mingw\bin"

        if BE.verbose:
            print "Using MingW path:", v
        return v

    def version_gt(self, version):
        return self.get_version() >= version

    @memoize("is_tdm")
    def is_tdm(self):
        """Return True if we are using a compiler from tdm-gcc.tdragon.net/"""
        pop = subprocess.Popen( pj(self.get_bin_path(), "gcc --version"),
                                           stdout=subprocess.PIPE)
        time.sleep(1)
        output = pop.stdout.read()
        return "(tdm"  in output

    @memoize("version")
    def get_version(self):
        pop = subprocess.Popen( pj(self.get_bin_path(), "gcc --version"),
                                           stdout=subprocess.PIPE)
        time.sleep(1)
        output = pop.stdout.read()
        reg = re_compile(r"(\d\.\d.\d)")
        return reg.search(output).group(1)

    @memoize("default_target")
    def get_default_target(self):
        prog = "int main(){return sizeof(void*);}"
        src  =  pj(BE.working_path, "comp_target_test.cpp")
        exe  =  pj(BE.working_path, "comp_target_test.exe")
        cmd  = "gcc %s -o %s"%(src,exe)
        with open(src, "w") as f:
            f.write(prog)
        subprocess.call(cmd, stdout=NullOutput, stderr=NullOutput, shell=True)
        ret = subprocess.call(exe)
        return 64 if ret==8 else 32

    @memoize("is_cross_compiler")
    def can_cross_compile(self):
        flag = "-m"+("32" if self.get_default_target() == 64 else "64")
        prog = "int main(){return sizeof(void*);}"
        src  =  pj(BE.working_path, "comp_cross_test.cpp")
        exe  =  pj(BE.working_path, "comp_cross_test.exe")
        cmd  = "gcc %s %s -o %s"%(src,flag,exe)
        with open(src, "w") as f:
            f.write(prog)
        ret = subprocess.call(cmd, stdout=NullOutput, stderr=NullOutput) == 0
        return ret



# Shortcut:
Compiler = Compiler_()



class BuildEnvironment(object):
    __metaclass__ = MSingleton

    def __init__(self):
        self.options = {}
        # self.proj_builders = None
        # self.egg_builders  = None
        self.options = {}
        self.working_path    = None
        self.proc_file_path  = None
        self.original_path   = os.environ["PATH"]
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.null_stdout     = NullOutput
        self.tools = []
        self.metabuilders = []
        self.done_tasks = {}

    def set_options(self, options):
        self.options = options.copy()
        Compiler.set_options(options)        
        self.tools = options.get("tools",[])[:]
        self.init()
        
    @property
    def verbose(self):
        return self.options.get("verbose")

    def set_metabuilders(self, metabuilders):
        self.metabuilders = metabuilders[:]

    def init(self):
        self.working_path = pj( self.options.get("wdr","."), self.get_platform_string() )
        self.proc_file_path = pj(self.working_path,"proc_flags.pk")
        self.create_working_directories()
        recursive_copy( split(__file__)[0], self.working_path, "setup.py.in", levels=1)
        recursive_copy( split(__file__)[0], self.working_path, "qmake_main.cpp.sub", levels=1)
        self.__fix_environment()
        self.__fix_sys_path()

        if is_64bits_python():
            if self.verbose: print "Doing a 64 bits compilation because we are using a 64 bits Python."
            if not Compiler.get_default_target() == 64:
                print "Compiler is not a 64 bits compiler. Can it cross-compile?"
                if not Compiler.can_cross_compile():
                    print "Cannot cross compile."
                    raise Exception("No compiler found for Windows 64 bits")
        else:
            if self.verbose: print "Doing a 32 bits compilation because we are using a 32 bits Python."
            if not Compiler.get_default_target() == 32:
                print "Compiler is not a 32 bits compiler"
                raise Exception("No compiler found for Windows 64 bits")

    # -- context manager protocol --
    def __enter__(self):
        try:
            print self.proc_file_path
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
    # def __init_builders(self):
        # self.proj_builders = list(MProject.builders.itervalues())
        # self.egg_builders  = list(MEgg.builders.itervalues())

    def build(self):
        only = self.options.get("only")
        #self.__init_builders()
        # We do NOT restrict the loop to the builders in the "only"
        # list because we still want to process unskippable actions
        # of the other builders because they can extend os.env["PATH"]
        # or sys.path.
        for buildercls in ( cls for meta in self.metabuilders for cls in meta.builders.itervalues() ):
            builder = buildercls()
            if builder.has_pending and builder.enabled:

                if not builder.process_me(only):
                    if self.options["keep_going"]:
                        continue
                    else:
                        return False
                # however we do stop as soon as there are no more "only" builders
                # to process because we don't need to do the remaining unskippable
                # actions of the not "only" builders
                if only and builder.name in only:
                    only.remove(builder.name)
                    if not len(only):
                        return True
        return True

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
        self.__overwrite_path()
        self.ensure_python_lib()
        self.__overwrite_path()

    def __overwrite_path(self):        
        tool_paths = []
        for tool in self.tools:
            tool = tool()
            pth = tool.get_path()
            if pth:
                tool_paths.append(pth)
                
        path = sj(tool_paths + [Compiler.get_bin_path()])
        if self.options["pass_path"]:
            path = sj( [self.original_path, path] )

        if path.endswith("\""):
            print "Removing trailing PATH quotes as mingw32-make doesn't like them"
            path = path.replace("\"", "")
        os.environ["PATH"] = path

    def __fix_sys_path(self):
        """Clean sys.path for this process so that we don't import
        existing eggs or site-installed thingys."""
        our_egg_names = [name.strip("egg_") for name in MEgg.builders.iterkeys()]
        for pth in sys.path[:] :
            pth_p = pth.lower()
            for egg_name in our_egg_names:
                if egg_name in pth_p:
                    sys.path.remove(pth)
                    break

    def ensure_python_lib(self):
        """Checks that libpythonXY.a exists.
        On Win64 python only ships with pythonXY.lib (MSVC)"""
        if "win32" not in self.get_platform_string():
            return

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
            d_ = rgetattr(self, directory)
            print "changing to", d_, "for", f.__name__
            os.chdir(d_)
            ret = f(self, *args, **kwargs)
            os.chdir(self.env.get_working_path())
            return ret
        wrapper.__name__ = f.__name__
        return wrapper
    return dir_changer

def with_original_sys_path(f):
    """Calls the decorated function with the original PATH environment variable"""
    def func(*args,**kwargs):
        cursyspath = sys.path[:]
        sys.path = BaseEggBuilder.__oldsyspath__[:]
        ret = f(*args, **kwargs)
        sys.path = cursyspath
        return ret
    return func

def option_to_sys_path(option):
    """If optionnal argument "option" was provided on the command line
    it will be prepended to the PATH just for the call this function decorates.
    After the call, the original environment will be restored."""
    def func_decorator(f):
        def wrapper(self, *args, **kwargs):
            opt_pth = self.options.get(option)
            if opt_pth:
                prev_pth = os.environ["PATH"]
                os.environ["PATH"] = sj([opt_pth, prev_pth])
                ret = f(self, *args, **kwargs)
                os.environ["PATH"] = prev_pth
            else:
                print "option_to_sys_path:", option, "not provided"
                ret = f(self, *args, **kwargs)
            return ret
        return wrapper
    return func_decorator

def option_to_python_path(option):
    """If optionnal argument "option" was provided on the command line
    it will be appended to the PYTHONPATH and sys.path vars just for the
    call this function decorates. After the call, the original environment
    will be restored."""
    def func_decorator(f):
        def wrapper(self, *args, **kwargs):
            opt_pth = self.options.get(option)
            if opt_pth:
                # save original values
                prev_pth = sys.path[:]
                prev_py_pth = os.environ.get("PYTHONPATH", "")
                # modify environment
                sys.path += opt_pth.split(";")
                os.environ["PYTHONPATH"] = sj([opt_pth, prev_py_pth])
                # call the function
                ret = f(self, *args, **kwargs)
                # restore original values
                sys.path = prev_pth
                os.environ["PYTHONPATH"] = prev_py_pth
            else:
                print "option_to_python_path:", option, "not provided"
                ret = f(self, *args, **kwargs)
            return ret
        return wrapper
    return func_decorator

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
    #if not None, it is then a list of triplets specifying additionnal
    #command line options that are needed for this package.
    cmd_options = None
    # list of tools that are required by this builder
    required_tools = None

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

    def get_task_restriction(self):
        return None
        
    def __find_pending_tasks(self):
        tasks = []
        name  = self.name
        for task in self.supported_tasks:
            task_func, skippable = self.all_tasks.get(task, (None, None))
            if task_func == skippable == None:
            # This happens with the --no-upload option
            # that removes tasks from all_tasks
                continue
            done   = self.env.is_task_done(name, task)
            
            forced = False
            restriction = self.get_task_restriction()
            if restriction != None:
                forced = task in restriction
            else:
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

    def process_me(self, only):
        should_process = only is None or self.name in only
        self.env.make_silent( not self.__has_pending_verbose_tasks() or \
                              not should_process )

        # forced_tasks is a string containing self.all_tasks keys.
        # if a process is in forced_tasks it gets forced.
        forced_tasks = self.options.get(self.name, "")

        proc_str  = "Processing " + self.name
        print "\n",proc_str
        print "="*len(proc_str)
        print "forced tasks are:", forced_tasks        

        for task, task_func, skippable in self.pending:        
            if skippable and not should_process:
                continue
            # doing unskippable actions like extending python or env PATH.
            # or we should_process is True
            nice_func = task_func.strip("_")
            print "\t-->performing %s for %s"%(nice_func, self.name)
            success = getattr(self, task_func)()
            if success == Later:
                print "\t-->%s for %s we be done later"%(nice_func, self.name)
            elif success == False:
                print "\t-->%s for %s failed"%(nice_func, self.name)
                if not should_process:
                    print "-o %s was specified, ignoring error on package %s"% \
                         (self.options.get("only"), self.name)
                    continue
                return False
            else:
                self.env.task_is_done(self.name, task)

        self.env.make_silent(False)
        return True



class BaseProjectBuilder(BaseBuilder, object):
    __metaclass__ = MProject

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
                                    ("n",("_new_env_vars",False)),
                                    ("c",("_configure",True)),
                                    ("b",("_build",True)),
                                    ("i",("_install",True)),
                                    ("p",("_patch", True)), #where should you be?
                                    ("x",("_extend_sys_path",False)),
                                    ("y",("_extend_python_path",False)),
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

    def get_task_restriction(self):
        return self.options.get("only_action_projs")
        
    def download_source(self):
        # a proj with a none url implicitely means
        # the sources are already here because some
        # other proj installed it.
        if self.url is None:
            return True

        return download(self.url, self.download_name, self.archname)

    def unpack_source(self, arch=None):
        # a proj with a none url implicitely means
        # the sources are already here because some
        # other proj installed it.
        if self.url is None:
            print 'No url'
            return True
        if exists(self.sourcedir):
            print 'already unpacked in '+repr(self.sourcedir)
            return True
        arch = arch or self.archname
        return unpack(arch, self.sourcedir)

    def fix_source_dir(self):
        try:
            print "fixing sourcedir", self.sourcedir,
            self.sourcedir = into_subdir(self.sourcedir, self.archive_subdir)
            if self.sourcedir is None:
                raise Exception("Subdir should exist but doesn't, archive has probably not been unpacked")
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

class BaseEggBuilder(BaseBuilder, object):
    __metaclass__  = MEgg
    __oldsyspath__ = sys.path[:]
    # The egg depends on the Python version (allows correct egg naming)
    py_dependent   = True
    # The egg depends on the os and processor type (allows correct egg naming)
    arch_dependent = True
    # Task management:
    all_tasks      = OrderedDict([("c",("_configure_script",True)),
                                  ("e",("_eggify",True)),
                                  ("u",("_upload_egg",True)),
                                  ("g",("_copy_egg_in_dir",True)),
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

        self.default_substitutions = dict( NAME             = self.egg_name(),
                                       VERSION              = "1.0",
                                       THIS_YEAR            = datetime.date.today().year,
                                       SETUP_AUTHORS        = "Openalea Team",
                                       CODE_AUTHOR          = self.authors,
                                       DESCRIPTION          = self.description,
                                       URL                  = "",
                                       LICENSE              = self.license,

                                       ZIP_SAFE             = False,
                                       PYTHON_MODS          = None,
                                       PACKAGES             = None,
                                       PACKAGE_DIRS         = None,
                                       PACKAGE_DATA         = {},
                                       DATA_FILES           = None,

                                       INSTALL_REQUIRES     = None,

                                       BIN_DIRS = None,
                                       LIB_DIRS = None,
                                       INC_DIRS = None,
                                       )
    @classmethod
    def egg_name(cls):
        return cls.__name__.strip("egg_")

    def get_task_restriction(self):
        return self.options.get("only_action_eggs")
    
    def _glob_egg(self):
        eggs = glob.glob( pj(self.eggdir, "dist", "*.egg") )
        if len(eggs) == 0:
            raise Exception("No egg found for "+self.egg_name())
        elif len(eggs) > 1:
            raise Exception("Found multiple eggs for "+self.egg_name()+reduce(lambda x,y:x+"\t->%s\n"%y, eggs, "\n"))
        return eggs[0]    
        
    @try_except
    def _configure_script(self):
        with open( self.setup_in_name, "r") as input, \
             open( self.setup_out_name, "w") as output:
            conf = self.default_substitutions.copy()
            conf.update(self.script_substitutions())
            conf = dict( (k,repr(v)) for k,v in conf.iteritems() )
            template = TemplateStr(input.read())
            output.write(template.substitute(conf))
        return True

    @in_dir("eggdir")
    @try_except
    def _eggify(self):
        ret     = self.eggify()
        # -- fix file name --
        eggname = self._glob_egg()
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
        
    @in_dir("eggdir")
    @try_except
    def _copy_egg_in_dir(self):
        dest_dir = self.options.get("dest_egg_dir")
        if not dest_dir:
            print "Will not place egg in a directory"
            return True

        eggname  = self._glob_egg()
        destname = pj(dest_dir, split(eggname)[1])
        if exists(destname):
            print "removing", destname
            os.remove(destname)
        print "copying", eggname, "to", destname
        shutil.copyfile(eggname, destname)
        return True

    def script_substitutions(self):
        return {}

    def eggify(self):
        #ret0 = subprocess.call(sys.executable + " setup.py egg_info --egg-base=%s"%self.eggdir ) == 0
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
    qtsrc    = "*"#.pro,*.pri,*.rc,*.def,*.h,*.hxx"
    qtinc    = re_compile(r"^Q[0-9A-Z]\w|.*\.h|^Qt\w")
    qtmkspec = "*"
    qttransl = "*.qm"

############################################################
# The following egg builder requires that you have the     #
# corresponding library installed. This is because they    #
# are too difficult to compile and that we don't actually  #
# need to compile them (no linkage from us to them)        #
# or that they come as .exes and not eggs already          #
############################################################
class InstalledPackageEggBuilder(BaseEggBuilder, object):
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



##########################
# Some Tools definitions #
##########################
class cmake(Tool):
    url            = "http://www.cmake.org/files/v2.8/cmake-2.8.7-win32-x86.zip"
    arch_name_ext  = "zip"
    archive_subdir = r"cmake*\bin"
    exe            = "cmake.exe"
    default_paths  = [ "c:\\Program Files (x86)\\cmake*\\bin\\",
                       "c:\\Program Files\\cmake*\\bin\\",
                       "c:\\CMake*\\bin\\"]


class bisonflex(Tool):
    url            = "https://gforge.inria.fr/frs/download.php/27628/bisonflex-2.4.1_2.5.35-win32.egg"
    arch_name_ext  = "zip"
    archive_subdir = "bin"
    exe            = "bison.exe"


class setuptools(Tool):
    installable    = False
    exe            = "easy_install"+exe_ext
    default_paths  = [ Tool.PyExecPaths ]

    
class openalea_deploy(Tool):
    installable    = False
    exe            = "alea_install"+exe_ext
    default_paths  = [ Tool.PyExecPaths  ]


#################################
# -- MAIN LOOP AND RELATIVES -- #
#################################
def valid_builder(arg):
    if arg in MProject.builders.keys() or \
       arg in MEgg.builders.keys() :
        return arg
    else:
        raise argparse.ArgumentError()

def build_epilog(metabuilders, dep_build_end=True):
    epilog = ""
    for mbuilder in metabuilders:
        m_name = mbuilder.ez_name
        epilog += "%s_ACTIONS are a concatenation of flags specifying what actions will be done:\n"%m_name.upper()
        for proc, (funcname, skippable) in mbuilder.bases[0].all_tasks.iteritems():
            if skippable:
                epilog += "\t%s : %s\n"%(proc, funcname.strip("_"))
        epilog += "\n"

    # epilog += "EGG_ACTIONS are a concatenation of flags specifying what actions will be done:\n"
    # for proc, (funcname, skippable) in BaseEggBuilder.all_tasks.iteritems():
        # if skippable:
            # epilog += "\t%s : %s\n"%(proc, funcname.strip("_"))

    if dep_build_end:
        epilog += "\nBy default, building rules will be read from project_rules.py and egg_rules.py_dependent\n"
        epilog += "You can specify your own by using --prules <filename> and --erules <filename> .\n"

    return epilog

def options_common(parser):
    g = parser.add_argument_group("General options")
    g.add_argument("--keep-going", "-k", action="store_const", const=True, default=False,
                   help="Keep going on errors")
    g.add_argument("--verbose", action="store_const", const=True, default=False,
                   help="Well try to say more things.")
    g.add_argument("--pass-path", action="store_const", const=True, default=False,
                   help="Pass current PATH to the system instead of clearing it")
    return parser

def options_dep_build(parser):
    g = parser.add_argument_group("Dependency builder options")
    g.add_argument("--wdr", default=abspath(os.curdir), type=abspath,
                        help="Under which directory we will create our working dir")
    g.add_argument("--python", "-p", default=None,
                   help="Fully qualified python executable to use for the compilation")
    g.add_argument("--compiler", "-c", default=None,
                   help="Path to compiler binaries")
    g.add_argument("--only", "-o", default=None, action="append", type=valid_builder,
                   help="Only process these project/eggs")    
    g.add_argument("--only-action-projs", default=None, metavar="PROJECT_ACTIONS",
                   help="For all projects to be processed, only do these action")
    g.add_argument("--only-action-eggs", default=None, metavar="EGG_ACTIONS",
                   help="For all eggs to be processed, only do these action")
    g.add_argument("--jobs", "-j", default=1, type=int,
                   help="Number of jobs during compilation")
    g.add_argument("--no-upload", "-n", action="store_const", const=True, default=False,
                   help="Do not upload eggs to forge")
    g.add_argument("--release", action="store_const", const=True, default=False,
                   help="Upload eggs to openalea repository or vplants (if False - for testing).")    
    g.add_argument("--dest-egg-dir", default=None, type=abspath,
                   help="Put generated eggs in a directory.")
    return parser

def options_gforge(parser):
    g = parser.add_argument_group("GForge options")
    g.add_argument("--gforge",  action="store_const", const=True, default=False, help="Use the GForge")
    g.add_argument("--login",  default=None, help="Login to connect to GForge")
    g.add_argument("--passwd", default=None, help="Password to connect to GForge")
    return parser

def options_metabuilders(parser, metabuilders):
    pkg_options = {}
    tools = set()

    for mbuilder in metabuilders:
        m_name = mbuilder.ez_name
        g = parser.add_argument_group("Options controlling %s builder actions to force"%m_name)
        for name, builder in mbuilder.builders.iteritems():
            if not builder.enabled:
                continue
            g.add_argument("--"+name, default="",
                                help="Force actions on %s"%name, dest=name,
                                metavar="%s_ACTIONS"%m_name.upper())
            if builder.cmd_options:
                pkg_options.setdefault(name,list()).extend(builder.cmd_options)
            if builder.required_tools:
                tools |= set(builder.required_tools)


    for bname, opt_list in pkg_options.iteritems():
        g = parser.add_argument_group("Options for " + bname + " builder")
        for opt_name, default, help in opt_list:
            g.add_argument("--"+opt_name, default=default, help=help)

    tools = sorted(tools, cmp=lambda x,y: cmp(x.name, y.name))
    for tool in tools:
        g = parser.add_argument_group("Options for " + tool().name + " tool")
        if tool.cmd_options is not None:
            for opt_name, default, help in tool.cmd_options:
                g.add_argument("--"+opt_name, default=default, help=help)
    return parser, tools

def parse_arguments(metabuilders):
    parser = argparse.ArgumentParser(description="Build and package binary Openalea dependencies",
                                     epilog=build_epilog(metabuilders),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,)

    parser, tools = options_metabuilders(options_gforge(options_dep_build(options_common(parser))),
                                         metabuilders)

    return parser.parse_args(), tools

def main():
    #default building rules
    proj_rules_file = pj(split(__file__)[0],"project_rules.py")
    egg_rules_file  = pj(split(__file__)[0],"egg_rules.py")
    # if any rules are given as arguments, parse those first
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

    metabuilders=[MProject,MEgg]
    args, tools = parse_arguments( metabuilders )

    # set some env variables for subprocesses
    os.environ["MAKE_FLAGS"] = "-j"+str(args.jobs)
    if args.no_upload:
        del BaseEggBuilder.all_tasks["u"]
        
    if args.python is not None: #use another Python to compile, this is weird, maybe useless.
        python = args.python
        del args.python #or else we will nevert start!
        arg_str = reduce( lambda x,y: x + (" --"+y[0]+"="+str(y[1]) if y[1] else ""), args._get_kwargs(), pj(os.getcwd(), __file__) )
        # cannot use subprocess, spawn or exec : if we run a 32 python on a 64 bits machine
        # and ask to use a 64 bits python, WoW (which is executing the 32 bits process)
        # will fail to run the 64 bits Python as a subprocess
        return os.system(python + " " + arg_str)
    else:
        options = vars(args)
        options["tools"] = tools
        env = BuildEnvironment()
        env.set_options(options)
        env.set_metabuilders(metabuilders)
        ret = False
        with env:
            ret = env.build()
        return ret




if __name__ ==  "__main__":
    sys.exit( main() == False )
