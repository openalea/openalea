
import traceback
import platform
import os, sys
from os.path import join as pj, splitext, getsize, exists, abspath, split
import shutil
from collections import namedtuple, OrderedDict, defaultdict
import urllib
import subprocess
import glob
import time
import pprint
import fnmatch
import re
import string

Project = namedtuple("Project", "name url dlname arch_subdir")
Egg = namedtuple("Egg", "name")
sj = os.pathsep.join

# TODO! This can be merged with the utility that makes windows installers
# and the system_dependecies utility.


# a Project with a None url implicitely means the sources are already here because some other proj installed it.

projs = OrderedDict ( (p.name,p) for p in  [Project("qt4"         , "http://download.qt.nokia.com/qt/source/qt-everywhere-opensource-src-4.7.4.zip", "qt4_src.zip", "qt-every*"),
                                             Project("sip"         , "http://www.riverbankcomputing.co.uk/static/Downloads/sip4/sip-4.13.zip", "sip_src.zip", "sip*"),
                                             Project("pyqt4"       , "http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-win-gpl-4.8.6.zip", "pyqt4_src.zip", "PyQt*"),
                                             Project("qscintilla"  , "http://www.riverbankcomputing.co.uk/static/Downloads/QScintilla2/QScintilla-gpl-2.5.1.zip", "qscintilla_src.zip", "QScint*/Qt4"),
                                             Project("pyqscintilla", None, "qscintilla_src.zip", "QScint*/Python"), # shares the same as qscintilla
                                             Project("qglviewer"   , "https://gforge.inria.fr/frs/download.php/28138/libQGLViewer-2.3.9-py.tgz", "qglviewer_src.tgz", "libQGLV*/QGLViewer"),
                                             Project("pyqglviewer" , "https://gforge.inria.fr/frs/download.php/28212/PyQGLViewer-0.9.1.zip", "pyqglviewer_src.zip", "PyQGLV*"),
                                                ]
                        )
                        
eggs = OrderedDict ( (p.name,p) for p in  [Egg("qt4"), 
                                           Egg("qt4_dev"), 
                                           Egg("pyqglviewer")]
                   )

# Some utilities
def recursive_glob(dir_, filepatterns=None, regexp=None, strip_dir_=False, levels=-1):
    """ Goes down a file hierarchy and returns files paths
    that match filepatterns or regexp."""
    files = []
    if filepatterns:
        filepatterns = filepatterns.split(",")
    elif regexp:
        regexp = re.compile(regexp)
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
    return files if not strip_dir_ else [ f[len(dir_)+1:] for f in files]
    
def recursive_glob_as_dict(dir_, filepatterns=None, regexp=None, strip_dir_=False, strip_keys=False, prefix_key=None, dirs=False):
    files     = recursive_glob(dir_, filepatterns, regexp, strip_dir_)
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
    """ A wrapper around os.makedirs that prints what itt's doing and catches harmless errors. """
    print "creating", pth, "...",
    try:
        os.makedirs( pth )
        print "ok"
    except os.error, e:
        print "already exists or access denied"
        if verbose:
            traceback.print_exc()    
    
def copy(source, dest, patterns):
    patterns = patterns.split(",")
    files = []
    for pat in patterns:
        files += glob.glob( pj(source, pat) )
    for f in files: shutil.copy(f, dest)

def recursive_copy(sourcedir, destdir, filepatterns=None, regexp=None, levels=-1, flat=False):
    print "recursive_copy", sourcedir, destdir, filepatterns, regexp
    src = recursive_glob( sourcedir, filepatterns, regexp, levels=levels )
    src_r = [destdir]*len(src) if flat else [ pj(destdir, f[len(sourcedir)+1:]) for f in src]
    bases = set([ split(f)[0] for f in src_r])
    for pth in bases:
        makedirs(pth)
    for src, dst in zip(src, src_r):
        print src, dst
        shutil.copy(src, dst)               

# -- we define a micro build environment --
class Singleton(type):
    """ Singleton Metaclass """

    def __init__(cls, name, bases, dic):
        type.__init__(cls, name, bases, dic)
        cls.instance=None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance=type.__call__(cls, *args, **kw)
        return cls.instance

        
proj_process_map = OrderedDict([("d",("download_source",True)),
                                ("u",("unpack_source",True)),
                                ("f",("fix_source_dir",False)),
                                ("c",("_configure",True)),
                                ("b",("_build",True)),
                                ("i",("_install",True)),
                                ("p",("_patch", True)), #where should you be?
                                ("x",("_extend_sys_path",False)),
                                ("y",("_extend_python_path",False)),
                                ])

egg_process_map = OrderedDict([("c",("_configure_script",True)),
                               ("e",("_eggify",True)),
                               #("u",("_upload_egg",True))
                              ])        
        
        
        
class BuildEnvironment(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.options = {}
        self.working_path = pj( os.getcwd(), self.get_platform_string() )
        recursive_copy( split(abspath(sys.argv[0]))[0], self.working_path, "setup*.py.in", levels=1)
        self.proc_file_path = pj(self.working_path,"proc_flags.pk")
        self.create_working_directories()
        os.environ["PATH"] = sj([os.environ["PATH"],self.get_compiler_bin_path()])

    def set_options(self, options):
        self.options = options.copy()

    # context manager protocol
    def __enter__(self):
        try:
            with open(self.proc_file_path, "rb") as f:
                txt  = f.read()
                self.proc_flags = eval(txt)
        except:
            traceback.print_exc()
            self.proc_flags = {}
            
    def skippable_proc(self, proj, proc):               
        if not isinstance(proj, Egg):            
            name = proj.name
            d    = proj_process_map
        else:
            name = proj.name+'_egg'
            d    =  egg_process_map
        
        skippable = d[proc][1]
        forced_proc_flags = self.options.setdefault("PROC_FLAGS",{}).setdefault(name, "")
        skip = proc in self.proc_flags.setdefault(name, "") and proc not in forced_proc_flags and skippable
        return skip
            
    def mark_proc_as_done(self, proj, proc):
        name = proj.name if not isinstance(proj, Egg) else proj.name+'_egg'
        if proc not in self.proc_flags.setdefault(name, ""):
            self.proc_flags[name] += proc

    def __exit__(self, exc_type, exc_value, traceback):
        with open(self.proc_file_path, "wb") as f:
            pprint.pprint(self.proc_flags, f)

    # Some info to tell us where to build
    def get_platform_string(self):
        # TODO : do smart things according to self.options
        return "_".join([platform.python_version(),
                        "Win"+platform.win32_ver()[0],
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

def sourcedir( f ) :
    """Encapsulate f in a structure that changes to self.sourcedir,
    calls f and moves back to BuildEnvironment.get_working_path()"""
    def wrapper(self, *args, **kwargs):
        os.chdir(self.sourcedir)
        ret = f(self, *args, **kwargs)
        os.chdir(self.env.get_working_path())
        return ret
    return wrapper

# -- we define a micro build environment --
class ProjectBuilders(Singleton):
    """ A Project Builder registry and Singleton Metaclass """
    builders = {}
    def __init__(cls, name, bases, dic):
        Singleton.__init__(cls, name, bases, dic)
        ProjectBuilders.builders[name] = cls        

class BaseProjectBuilder(object):
    __metaclass__ = ProjectBuilders

    def __init__(self, options):
        self.options = options.copy()
        self.proj = None
        proj_name = self.__class__.__name__
        self.proj = projs.get(proj_name)
        if self.proj is None:
            raise Exception("cannot find", proj_name, "in projs")

        self.env = BE()
        self.archname  = pj( self.env.get_dl_path() , self.proj.dlname)
        self.sourcedir = pj( self.env.get_src_path(), splitext(self.proj.dlname)[0] )
        self.installdir = pj( self.env.get_install_path(), splitext(self.proj.dlname)[0] )

    def download_source(self):
        def download_reporter(bk, bksize, bytes):
            progress= float(bk)/(bytes/bksize) * 100
            sys.stdout.write(("Dl %s from %.20s to %s: %.1f"%(self.proj[:3]+(progress,)))+"\r")
            sys.stdout.flush()

        # a proj with a none url implicitely means the sources are already here because some
        # other proj installed it.
        if self.proj.url is None:
            return True

        remote_sz = float("inf")
        try:
            remote    = urllib.urlopen(self.proj.url)
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
                urllib.urlretrieve(self.proj.url, self.archname, download_reporter)
            except:
                traceback.print_exc()
                ret = False
        return ret

    def unpack_source(self):
        # a proj with a none url implicitely means the sources are already here because some
        # other proj installed it.
        if self.proj.url is None:
            return True
        if exists(self.sourcedir):
            return True

        import zipfile, tarfile
        base, ext = splitext( self.proj.dlname )
        print "unpacking", self.proj.dlname
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
            if self.proj.arch_subdir is not None:
                self.sourcedir = glob.glob(pj(self.sourcedir,self.proj.arch_subdir))[0]
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
            os.environ["PATH"] = sj([os.environ["PATH"],exp])
        return True

    def _extend_python_path(self):
        exp = self.extra_python_paths()
        if exp is not None:
            if isinstance(exp, tuple):
                exp = sj(exp)        
            #sys.path += exp
            os.environ["PYTHONPATH"] = sj([os.environ.get("PYTHONPATH",""),exp])
        return True

    @try_except
    @sourcedir
    def _configure(self):
        return self.configure()

    @try_except
    @sourcedir
    def _build(self):
        return self.build()

    @try_except
    @sourcedir
    def _patch(self):
        return self.patch()

    @try_except
    @sourcedir
    def _install(self):
        return self.install()

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


        
class EggBuilders(Singleton):
    """ An Egg Builder registry and Singleton Metaclass """
    builders = {}
    def __init__(cls, name, bases, dic):
        Singleton.__init__(cls, name, bases, dic)
        if "egg_" in name: #dunno why "EggBuilder" gets passed here.
            EggBuilders.builders[name[4:]] = cls

def eggdir( f ) :
    """Encapsulate f in a structure that changes to self.eggdir,
    calls f and moves back to BuildEnvironment.get_working_path()"""
    def wrapper(self, *args, **kwargs):
        os.chdir(self.eggdir)
        ret = f(self, *args, **kwargs)
        os.chdir(self.env.get_working_path())
        return ret
    return wrapper
    
class BaseEggBuilder(object):
    __metaclass__ = EggBuilders
    def __init__(self, options):
        self.name           = self.__class__.__eggname__
        self.env            = BE()
        self.eggdir         = pj(self.env.get_egg_path(), self.name)
        self.setup_in_name  = pj(self.env.get_working_path(), "setup_" + self.name + ".py"+'.in')
        self.setup_out_name = pj(self.eggdir, "setup.py")
        makedirs(self.eggdir)

    def _configure_script(self):
        try:
            with open( self.setup_in_name, "r") as input, open( self.setup_out_name, "w") as output:
                conf = self.script_substitutions()
                template = string.Template(input.read())
                output.write(template.substitute(conf))
        except Exception, e:
            traceback.print_exc()
            return False
        else:
            return True
        
    @try_except
    @eggdir
    def _eggify(self):
        return self.eggify()

    @try_except
    @eggdir
    def _upload_egg(self):
        return self.upload_egg()

    def script_substitutions(self):
        return {}
        
    def eggify(self):
        return subprocess.call(sys.executable + " setup.py bdist_egg") == 0
        
    def upload_egg(self):
        return True

####################################################################################################
# - PROJECT BUILDERS - PROJECT BUILDERS - PROJECT BUILDERS - PROJECT BUILDERS - PROJECT BUILDERS - #
####################################################################################################
class qt4(BaseProjectBuilder):
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        # define installation paths
        self.inst_paths = pj(self.installdir, "bin"), pj(self.installdir, "dll"), pj(self.installdir, "lib"), pj(self.installdir, "src"), \
                          pj(self.installdir, "include"), pj(self.installdir, "dll"), pj(self.installdir, "plugins_lib"), pj(self.installdir, "mkspecs"), pj(self.installdir, "translations")
        self.install_bin_dir, self.install_dll_dir, self.install_lib_dir, self.install_src_dir, self.install_inc_dir, self.install_plu_dir, self.install_plu_lib_dir, self.install_mks_dir, self.install_tra_dir = self.inst_paths
        self.bin_pattern = "*.exe"
        self.dll_pattern = "*.dll"
        self.lib_pattern = "*.a,*.prl,*.pri,*.pfa,*.pfb,*.qpf,*.ttf,README"
        self.src_pattern = "*.pro,*.pri,*.rc,*.def,*.h,*.hxx"
        self.inc_pattern = r"^Q[A-Z]\w|.*\.h"        
        self.mks_pattern = "*"
        self.tra_pattern = "*.qm"
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
        copy( pj(self.sourcedir, "bin"), self.install_bin_dir, self.bin_pattern )
        # copy dlls
        copy( pj(self.sourcedir, "bin"), self.install_dll_dir, self.dll_pattern )
        # copy libs
        recursive_copy( pj(self.sourcedir, "lib"), self.install_lib_dir, self.lib_pattern )
        # copy src -- actually only header files in src --
        recursive_copy( pj(self.sourcedir, "src"), self.install_src_dir, self.src_pattern )
        # copy include
        recursive_copy( pj(self.sourcedir, "include"), self.install_inc_dir, regexp=self.inc_pattern )
        # copy plugins
        recursive_copy( pj(self.sourcedir, "plugins"), self.install_plu_dir, self.dll_pattern, flat=True )
        # copy plugins
        recursive_copy( pj(self.sourcedir, "plugins"), self.install_plu_lib_dir, self.lib_pattern )
        # copy plugins
        recursive_copy( pj(self.sourcedir, "mkspecs"), self.install_mks_dir, self.mks_pattern )
        # copy translations
        recursive_copy( pj(self.sourcedir, "translations"), self.install_tra_dir, self.tra_pattern )        
        return True
    def extra_paths(self):
        return pj(self.sourcedir, "bin"), self.install_dll_dir
    def patch(self):
        """ Patch qt *.exes and *.dlls so that they do not contain hard coded paths anymore. """
        import qtpatch
        try:
            qtpatch.patch("*.dll,*.exe", qtDirPath=self.sourcedir, where=self.installdir)
        except:
            traceback.print_exc()
            return False
        else:
            return True

class sip(BaseProjectBuilder):
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        # define installation paths
        # we install sip binaries in the qt bin installation directory to easily recover it
        # for the egg. 
        qt4_ = qt4.instance
        self.inst_paths = qt4_.install_bin_dir, pj(self.installdir, "site"), pj(self.installdir, "include"), pj(self.installdir, "sip")
        self.install_bin_dir, self.install_site_dir, self.install_inc_dir, self.install_sip_dir = self.inst_paths    
    def configure(self):
        return subprocess.call(sys.executable + " configure.py --platform=win32-g++ -b %s -d %s -e %s -v %s"%self.inst_paths) == 0
    def extra_paths(self):
        return self.install_bin_dir
    def extra_python_paths(self):
        return self.install_site_dir
    # def patch(self):
        # txt = None
        # with open("sipconfig.py") as f:
            # txt = f.read()
        # shutil.copyfile( "sipconfig.py", "sipconfig.py.old" )
        # prefix = sys.prefix

class pyqt4(BaseProjectBuilder) :
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        # define installation paths
        # we install pyqt4 binaries in the qt bin installation directory to easily recover it
        # for the egg.
        qt4_ = qt4.instance
        self.inst_paths = qt4_.install_bin_dir, pj(self.installdir,"site"), pj(self.installdir,"sip")
        self.install_bin_dir, self.install_site_dir, self.install_sip_dir = self.inst_paths    
    def configure(self):
        return subprocess.call(sys.executable + " configure.py --confirm-license -b %s -d %s -v %s"%self.inst_paths) == 0
    def extra_paths(self):
        return self.install_bin_dir
    def extra_python_paths(self):
        return self.install_site_dir
    # def patch(self):
        # txt = None
        # with open("sipconfig.py") as f:
            # txt = f.read()
        # shutil.copyfile( "sipconfig.py", "sipconfig.py.old" )
        # prefix = sys.prefix

class qscintilla(BaseProjectBuilder):
    def configure(self):
        # The install procedure will install qscintilla in qt's installation directories
        qt4_ = qt4.instance
        paths = qt4_.install_inc_dir, qt4_.install_tra_dir, qt4_.installdir, qt4_.install_dll_dir, 
        return subprocess.call("qmake -after header.path=%s trans.path=%s qsci.path=%s target.path=%s -spec win32-g++ qscintilla.pro"%paths) == 0
    def install(self):
        ret = BaseProjectBuilder.install(self)
        qt4_ = qt4.instance
        try:
            shutil.move( pj(qt4_.install_dll_dir, "libqscintilla2.a"), qt4_.install_lib_dir)
        except Exception, epyqt :
            print e
        return ret
        
class pyqscintilla(BaseProjectBuilder):
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        # define installation paths
        qsci = qscintilla.instance
        qt4_ = qt4.instance
        pyqt = pyqt4.instance        
        self.install_paths = pj(qsci.sourcedir,"release"), pj(qt4_.installdir, "qsci"), qsci.sourcedir, pj(pyqt.install_site_dir, "PyQt4"), pyqt.install_sip_dir
        self.qsci_dir = self.install_paths[1]
    def configure(self):
        """pyqscintilla installs itself in PyQt4's installation directory"""
        # we want pyqscintilla to install itself where pyqt4 installed itself.
        return subprocess.call(sys.executable + " configure.py -o %s -a %s -n %s -d %s -v %s"%self.install_paths ) == 0 #make this smarter

class qglviewer(BaseProjectBuilder):
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
        recursive_copy( self.sourcedir, self.install_inc_dir, "*.h")
        recursive_copy( pj(self.sourcedir, "release"), self.install_lib_dir, "*.a,*.prl")
        recursive_copy( pj(self.sourcedir, "release"), self.install_dll_dir, "*.dll")
        return True
    def extra_paths(self):
        return self.install_dll_dir

class pyqglviewer(BaseProjectBuilder):
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        qglbuilder = qglviewer.instance
        self.qglbuilderbase = pj(qglbuilder.sourcedir, os.path.pardir),        
        self.install_sip_dir  =  pj(qglbuilder.installdir, "sip")
        self.install_site_dir = qglbuilder.installdir
        self.install_exa_dir =  pj(qglbuilder.installdir, "examples")        
    def configure(self):
        return subprocess.call(sys.executable + " configure.py -Q %s "%self.qglbuilderbase) == 0
    def install(self):
        """ pyqglviewer installs itself into the same directory as qglviewer """
        recursive_copy( pj(self.sourcedir, "build"), self.install_site_dir, "*.pyd", levels=1)
        recursive_copy( pj(self.sourcedir, "src", "sip"), self.install_sip_dir, "*.sip", levels=1)
        recursive_copy( pj(self.sourcedir, "examples"), self.install_exa_dir, "*")
        return True
    def extra_python_paths(self):
        qglbuilder = qglviewer.instance
        return qglbuilder.installdir



################################################################################
# - EGG BUILDERS - EGG BUILDERS - EGG BUILDERS - EGG BUILDERS - EGG BUILDERS - #
################################################################################
def merge_list_dict(l):
    d = defaultdict(list)
    for k, v in l:
        d[k].extend(v)
        
    return dict( (k, sj(v)) for k,v in d.iteritems() )
    
class egg_qt4(BaseEggBuilder):
    __eggname__ = "qt4"
    def script_substitutions(self):
        qt4_   = qt4.instance
        pyqt4_ = pyqt4.instance
        pysci_ = pyqscintilla.instance
        sip_   = sip.instance
        # dlls are the union of qt dlls and plugins directories (which is actually the same!)
        # qscis apis are recursive from qt4 (need to list all files)        
        qscis   = recursive_glob_as_dict(pysci_.qsci_dir, "*.api", strip_keys=True, prefix_key="qsci").items()
        
        return { "DLLS": repr(qt4_.install_dll_dir),
                 "PYQT4DIR" : repr(pyqt4_.install_site_dir), 
                 "SIPDIR": repr(sip_.install_site_dir),
                 "QSCI": repr(qscis) ,
                 }
                 
class egg_qt4_dev(BaseEggBuilder):
    __eggname__ = "qt4_dev"
    def script_substitutions(self):
        qt4_   = qt4.instance
        pyqt4_ = pyqt4.instance
        sip_   = sip.instance
        # binaries are the union of qt, pyqt and sip binaries 
        bin_dirs = {"bin":qt4_.install_bin_dir}
        # includes are recursive subdirectories and the union of qt and sip includes               
        incs = recursive_glob_as_dict( qt4_.install_inc_dir, regexp=qt4_.inc_pattern, strip_keys=True, prefix_key="include", dirs=True).items() + \
               recursive_glob_as_dict( sip_.install_inc_dir, regexp=qt4_.inc_pattern, strip_keys=True, prefix_key="include", dirs=True).items()
        inc_dirs = merge_list_dict( incs )
        # libs are recursive subdirectories of qt libs          
        libs = recursive_glob_as_dict(qt4_.install_lib_dir, qt4_.lib_pattern, strip_keys=True, prefix_key="lib").items()
        # sip files are recursive subdirectories and the union of pyqt4 and...
        sips = recursive_glob_as_dict(pyqt4_.install_sip_dir, "*.sip", strip_keys=True, prefix_key="sip").items()
        # sources are recursive subdirectories and the union of qt4 and that all (CPP have been removed)...
        srcs = recursive_glob_as_dict(qt4_.install_src_dir, qt4_.src_pattern, strip_keys=True, prefix_key="src").items()
        # tra files are recursive subdirectories in qt4
        tra = recursive_glob_as_dict(qt4_.install_tra_dir, qt4_.tra_pattern, strip_keys=True, prefix_key="translations").items()
        # mks files are recursive subdirectories in qt4
        mks = recursive_glob_as_dict(qt4_.install_mks_dir, qt4_.mks_pattern, strip_keys=True, prefix_key="mkspecs").items()        
        # plugins files are recursive subdirectories in qt4
        plu = recursive_glob_as_dict(qt4_.install_plu_lib_dir, qt4_.lib_pattern, strip_keys=True, prefix_key="plugins").items()        

        return { "BINDIRS": repr(bin_dirs),
                 "INCLUDEDIRS": repr(inc_dirs),
                 "LIBS": repr(libs)[1:-1]    ,
                 "SIP": repr(sips)[1:-1]     ,
                 "SRC": repr(srcs)[1:-1],
                 "TRA": repr(tra)[1:-1],
                 "MKS": repr(mks)[1:-1],
                 "PLU": repr(plu)[1:-1],
                 }

class egg_pyqglviewer(BaseEggBuilder):
    __eggname__ = "pyqglviewer"
    def script_substitutions(self):
        qt4_   = qt4.instance
        qglv_   = qglviewer.instance
        pyqglv_   = pyqglviewer.instance
        # binaries are the union of qt, pyqt and sip binaries 
        bin_dirs = {"bin":qt4_.install_bin_dir}
        # includes are recursive subdirectories of qglviewer           
        incs = recursive_glob_as_dict( qglv_.install_inc_dir, "*.h", strip_keys=True, prefix_key="include", dirs=True).items()
        inc_dirs = merge_list_dict( incs )
        # libs are recursive subdirectories of qt libs          
        libs = recursive_glob_as_dict(qglv_.install_lib_dir, qt4_.lib_pattern, strip_keys=True, prefix_key="lib").items()
        # sip files are recursive subdirectories of pyqglviewer sip installation directory
        sips = recursive_glob_as_dict(pyqglv_.install_sip_dir, "*.sip", strip_keys=True, prefix_key="sip").items()
        # examples are recursive subdirectories of pyqglviewer examples installation directory contains various types of files
        exas = recursive_glob_as_dict(pyqglv_.install_exa_dir, "*", strip_keys=True, prefix_key="examples").items()        
        
        return { "PYQGLDIR": repr(pyqglv_.install_site_dir),
                 "INCLUDEDIRS": repr(inc_dirs),
                 "QGLVDLLDIR": repr(qglv_.install_dll_dir),
                 "LIBS": repr(libs)[1:-1]    ,
                 "SIP": repr(sips)[1:-1]     ,
                 "EXA": repr(exas)[1:-1],
                 }
    
# MAIN LOOP AND RELATIVES
def parse_process_flags(sysargv, options):
    proc_flags = {}
    for argv in sysargv[1:]:
        try:
            if argv.count("_") == 1:
                pk, flags = argv.split("_")
            elif argv.count("_") > 1:
                spl = argv.split("_")
                pk = "_".join(spl[:-1])
                flags = spl[-1]
            else:
                continue
            proc_flags[pk] = flags
        except:
            continue
    options["PROC_FLAGS"] = proc_flags

                                
                                
def main():
    # set some env variables for subprocesses
    os.environ["MAKE_FLAGS"] = "-j2"

    options = {}
    parse_process_flags(sys.argv, options)
    print options
    
    env = BuildEnvironment()
    env.set_options(options)
    # give priority to OUR compiler!
    os.environ["PATH"] = os.pathsep.join([env.get_compiler_bin_path(), os.environ["PATH"]])
    
    with env:
        for proj in projs.itervalues():
            proc_str = "PROCESSING " + proj.name
            print "\n",proc_str
            print "="*len(proc_str)
            # proc_flags is a string containing proj_process_map keys.
            # if a process is in proc_flags it gets forced.
            proc_flags = options["PROC_FLAGS"].get(proj.name, "")
            print "process flags are:", proc_flags

            builder = ProjectBuilders.builders[proj.name](options)
            for proc, (proc_func, skippable) in proj_process_map.iteritems():
                if env.skippable_proc(proj, proc):
                    print "\t-->ignoring %s for %s"%(proc_func, proj.name)
                    continue
                else:
                    print "\t-->performing %s for %s"%(proc_func, proj.name)
                    success = getattr(builder, proc_func)()
                    if not success :
                        print "\t-->%s for %s failed"%(proc_func, proj.name)
                        sys.exit(-1)
                    else:
                        env.mark_proc_as_done(proj, proc)

        
        for egg in eggs.itervalues():
            proc_str = "PROCESSING EGG " + egg.name
            print "\n",proc_str
            print "="*len(proc_str)
            # proc_flags is a string containing process_map keys.
            # if a process is in proc_flags it gets forced.
            proc_flags = options["PROC_FLAGS"].get(egg.name, "")
            print "process flags are:", proc_flags

            builder = EggBuilders.builders[egg.name](options)            
            for proc, (proc_func, skippable) in egg_process_map.iteritems():
                if env.skippable_proc(egg, proc):
                    print "\t-->ignoring %s for %s"%(proc_func, egg.name)
                    continue
                else:
                    print "\t-->performing %s for %s"%(proc_func, egg.name)
                    success = getattr(builder, proc_func)()
                    if not success :
                        print "\t-->%s for %s failed"%(proc_func, egg.name)
                        # break
                    else:
                        env.mark_proc_as_done(egg, proc)

    
    
if __name__ ==  "__main__":
            main()