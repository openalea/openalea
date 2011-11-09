
import traceback
import platform
import os, sys
from os.path import join as pj, splitext, getsize, exists, abspath
import shutil
from collections import namedtuple, OrderedDict
import urllib
import subprocess
import glob
import time
import pprint
import fnmatch
import re

Project = namedtuple("Project", "name url dlname arch_subdir")
sj = os.pathsep.join

# TODO! This can be merged with the utility that makes windows installers
# and the system_dependecies utility.


# a Project with a None url implicitely means the sources are already here because some other proj installed it.

projs_dict = OrderedDict ( (p.name,p) for p in  [Project("qt4"         , "http://download.qt.nokia.com/qt/source/qt-everywhere-opensource-src-4.7.4.zip", "qt4_src.zip", "qt-every*"),
                                                 Project("sip"         , "http://www.riverbankcomputing.co.uk/static/Downloads/sip4/sip-4.13.zip", "sip_src.zip", "sip*"),
                                                 Project("pyqt4"       , "http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-win-gpl-4.8.6.zip", "pyqt4_src.zip", "PyQt*"),
                                                 Project("qscintilla"  , "http://www.riverbankcomputing.co.uk/static/Downloads/QScintilla2/QScintilla-gpl-2.5.1.zip", "qscintilla_src.zip", "QScint*/Qt4"),
                                                 Project("pyqscintilla", None, "qscintilla_src.zip", "QScint*/Python"), # shares the same as qscintilla
                                                 Project("qglviewer"   , "https://gforge.inria.fr/frs/download.php/28138/libQGLViewer-2.3.9-py.tgz", "qglviewer_src.tgz", "libQGLV*/QGLViewer"),
                                                 Project("pyqglviewer" , "https://gforge.inria.fr/frs/download.php/28212/PyQGLViewer-0.9.1.zip", "pyqglviewer_src.zip", "PyQGLV*"),
                                                ]
                        )
                        
eggs = ["qt4", "qt4_dev", "pyqglviewer"]

# Some utilities
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

def recursive_glob(dir_, filepatterns=None, regexp=None):
    """ Goes down a file hierarchy and returns files paths
    that match filepatterns or regexp."""
    files = []
    if filepatterns:
        filepatterns = filepatterns.split(",")
    elif regexp:
        regexp = re.compile(regexp)
    for dir_path, sub_dirs, subfiles in os.walk(dir_):
        if filepatterns:
            for pat in filepatterns:
                for fn in fnmatch.filter(subfiles, pat):
                    files.append( os.path.join(dir_path, fn) )
        elif regexp:
            for fn in subfiles:
                if regexp.match(fn): files.append(os.path.join(dir_path, fn))
    return files

def copy(source, dest, patterns):
    patterns = patterns.split(",")
    files = []
    for pat in patterns:
        files += glob.glob( pj(source, pat) )
    for f in files: shutil.copy(f, dest)

def recursive_copy(sourcedir, destdir, filepatterns=None, regexp=None):
    src = recursive_glob( sourcedir, filepatterns, regexp )
    src_r = [ pj(destdir, f[len(sourcedir)+1:]) for f in src]
    bases = set([ os.path.split(f)[0] for f in src_r])
    for pth in bases:
        makedirs(pth)
    for src, dst in zip(src, src_r):
        shutil.copy(src, dst)

# -- we define a micro build environment --
class Singleton(type):
    """ Singleton Metaclass """

    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance=None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance=super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

class BuildEnvironment(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.options = {}
        self.working_path = pj( os.getcwd(), self.get_platform_string() )
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

    def mark_proc_as_done(self, proj, proc):
        if proc not in self.proc_flags.setdefault(proj.name, ""):
            self.proc_flags[proj.name] += proc

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
        super(ProjectBuilders, cls).__init__(name, bases, dic)
        ProjectBuilders.builders[name] = cls

class EggBuilders(Singleton):
    """ An Egg Builder registry and Singleton Metaclass """
    builders = {}
    def __init__(cls, name, bases, dic):
        super(EggBuilders, cls).__init__(name, bases, dic)
        EggBuilders.builders[name] = cls

class BaseProjectBuilder(object):
    __metaclass__ = ProjectBuilders

    def __init__(self, options):
        self.options = options.copy()
        self.proj = None
        proj_name = self.__class__.__name__
        self.proj = projs_dict.get(proj_name)
        if self.proj is None:
            raise Exception("cannot find", proj_name, "in projs_dict")

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
        exp = self.extra_path()
        if exp is not None:
            os.environ["PATH"] = sj([os.environ["PATH"],exp])
        return True

    def _extend_python_path(self):
        exp = self.extra_python_path()
        if exp is not None:
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

    def extra_path(self):
        return None
    def extra_python_path(self):
        return None
    def configure(self):
        raise NotImplementedError
    def build(self):
        return subprocess.call("mingw32-make") == 0
    def patch(self):
        return True
    def install(self):
        return subprocess.call("mingw32-make install") == 0


class BaseEggBuilder(object):
    __metaclass__ = EggBuilders
    def __init__(self, options):
        pass

    @try_except
    @sourcedir
    def _eggify(self):
        return self.eggify()

    def eggify(self):
        return True

####################################################################################################
# - PROJECT BUILDERS - PROJECT BUILDERS - PROJECT BUILDERS - PROJECT BUILDERS - PROJECT BUILDERS - #
####################################################################################################
class qt4(BaseProjectBuilder):
    def __init__(self, *args, **kwargs):
        super(qt4, self).__init__(*args, **kwargs)
        # define installation paths
        self.inst_paths = pj(self.installdir, "bin"), pj(self.installdir, "dll"), pj(self.installdir, "lib"), pj(self.installdir, "src"), \
                          pj(self.installdir, "include"), pj(self.installdir, "plugins"), pj(self.installdir, "mkspecs")
        self.install_exe_dir, self.install_dll_dir, self.install_lib_dir, self.install_src_dir, self.install_inc_dir, self.install_plu_dir, self.install_mks_dir = self.inst_paths
    def configure(self):
        pop = subprocess.Popen("configure.exe -platform win32-g++ -release -opensource -shared -nomake demos -nomake examples -mmx -sse2 -3dnow -declarative -webkit -no-s60 -no-cetest",
                               stdin=subprocess.PIPE) # PIPE is required or else pop.comminicate won't do anything!
        time.sleep(2) #give enough time for executable to load before it asks for license agreement.
        pop.communicate("y\r") #accepts license agreement, also waits for configure to finish
        return pop.returncode
    def install(self):
        # create the installation directories
        for pth in self.inst_paths:
            makedirs(pth)
        # copy binaries
        copy( pj(self.sourcedir, "bin"), self.install_exe_dir, "*.exe" )
        # copy dlls
        copy( pj(self.sourcedir, "bin"), self.install_dll_dir, "*.dll" )
        # copy libs
        copy( pj(self.sourcedir, "lib"), self.install_lib_dir, "*.a,*.prl" )
        recursive_copy( pj(self.sourcedir, "lib", "fonts"), self.install_lib_dir, "*" )
        # copy src -- actually only header files in src --
        recursive_copy( pj(self.sourcedir, "src"), self.install_src_dir, "*.pro,*.rc,*.def,*.h,*.hxx" )
        # copy include
        recursive_copy( pj(self.sourcedir, "include"), self.install_inc_dir, regexp=r"^Q[A-Z]\w|.*\.h" )
        # copy plugins
        recursive_copy( pj(self.sourcedir, "plugins"), self.install_plu_dir, "*.dll,*.a" )
        # copy plugins
        recursive_copy( pj(self.sourcedir, "mkspecs"), self.install_mks_dir, "*" )
        return True
    def extra_path(self):
        return sj([ self.install_exe_dir, self.install_dll_dir])
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
    def configure(self):
        paths = (pj(self.installdir,"bin"), pj(self.installdir,"site"), pj(self.installdir,"include"), pj(self.installdir,"sip"))
        return subprocess.call(sys.executable + " configure.py --platform=win32-g++ -b %s -d %s -e %s -v %s"%paths) == 0
    def extra_path(self):
        return pj(self.installdir, "bin")
    def extra_python_path(self):
        return pj(self.installdir, "site")
    # def patch(self):
        # txt = None
        # with open("sipconfig.py") as f:
            # txt = f.read()
        # shutil.copyfile( "sipconfig.py", "sipconfig.py.old" )
        # prefix = sys.prefix

class pyqt4(BaseProjectBuilder) :
    def configure(self):
        paths = ( pj(self.installdir,"bin"), pj(self.installdir,"site"), pj(self.installdir,"sip"))
        return subprocess.call(sys.executable + " configure.py --confirm-license -b %s -d %s -v %s"%paths) == 0
    def extra_path(self):
        return pj(self.installdir, "bin")
    def extra_python_path(self):
        return pj(self.installdir, "site")
    # def patch(self):
        # txt = None
        # with open("sipconfig.py") as f:
            # txt = f.read()
        # shutil.copyfile( "sipconfig.py", "sipconfig.py.old" )
        # prefix = sys.prefix


class qscintilla(BaseProjectBuilder):
    def configure(self):
        # The install procedure will install qscintilla in qt's directories
        return subprocess.call("qmake qscintilla.pro") == 0

class pyqscintilla(BaseProjectBuilder):
    def configure(self):
        """pyqscintilla installs itself in PyQt4's installation directory"""
        qsci = qscintilla.instance
        #qsci.fix_source_dir()
        pyqt = pyqt4.instance
        # we want pyqscintilla to install itself where pyqt4 installed itself.
        install_paths = (pj(pyqt.installdir,"site", "PyQt4"), pj(pyqt.installdir,"sip"))
        return subprocess.call(sys.executable + " configure.py -o " + pj(qsci.sourcedir,"release") +
                        " -n " + qsci.sourcedir + " -d %s -v %s"%install_paths) == 0 #make this smarter

class qglviewer(BaseProjectBuilder):
    def __init__(self, *args, **kwargs):
        super(qglviewer, self).__init__(*args, **kwargs)
        # qmake is annoying with backslashes
        self.includedir        = pj(self.installdir, "include").replace("\\", "/")
        self.includedirVRender = pj(self.installdir, "include", "VRender").replace("\\", "/")
        self.libdir            = pj(self.installdir, "lib").replace("\\", "/")
    def configure(self):
        # The install procedure will install qscintilla in qt's directories
        paths = self.includedir, self.libdir
        return subprocess.call("qmake include.path=%s target.path=%s QGLViewer*.pro"%paths) == 0
    def build(self):
        # by default, and since we do not use self.options yet, we build in release mode
        return subprocess.call("mingw32-make release") == 0
    def install(self):
        dirs = self.includedirVRender, self.libdir
        for d in dirs:
            makedirs(d)
        # copy headers
        copy(self.sourcedir, self.includedir, "*.h")
        # copy vrender headers
        copy( pj(self.sourcedir, "VRender"), self.includedirVRender, "*.h")
        # copy libs
        copy( pj(self.sourcedir, "release"), self.libdir, "*.dll,*.a")
    def extra_path(self):
        return self.libdir

class pyqglviewer(BaseProjectBuilder):
    def configure(self):
        qglbuilder = qglviewer.instance
        paths = pj(qglbuilder.sourcedir, os.path.pardir),
        return subprocess.call(sys.executable + " configure.py -Q %s "%paths) == 0
    def install(self):
        """ pyqglviewer installs itself into the same directory as qglviewer """
        qglbuilder = qglviewer.instance
        shutil.copy( pj(self.sourcedir, "build", "PyQGLViewer.pyd"), qglbuilder.installdir)
        shutil.copytree( pj(self.sourcedir, "src", "sip"), pj(qglbuilder.installdir, "sip"))
    def extra_python_path(self):
        qglbuilder = qglviewer.instance
        return qglbuilder.installdir



################################################################################
# - EGG BUILDERS - EGG BUILDERS - EGG BUILDERS - EGG BUILDERS - EGG BUILDERS - #
################################################################################
class qt4(BaseEggBuilder):
    def get_meta_info(self):
        import sip
        import PyQt4
        return {name:"qt4",
                version:PyQt4.QT_VERSION_STR,
                description:"PyQt Runtime packaged as an egg for windows-gcc",
                author:"Riverbank Computing is the author of PyQt4. This egg was prepared by the Openalea Team.",
                }

class qt4_dev(BaseEggBuilder):
    pass

class pyqglviewer(BaseEggBuilder):
    pass
    
# MAIN LOOP AND RELATIVES
def parse_process_flags(sysargv, options):
    proc_flags = {}
    for argv in sysargv:
        try:
            pk, flags = argv.split("_")
            proc_flags[pk] = flags
        except:
            continue
    options["PROC_FLAGS"] = proc_flags


proj_process_map = OrderedDict([("d",("download_source",True)),
                                ("u",("unpack_source",True)),
                                ("f",("fix_source_dir",False)),
                                ("c",("_configure",True)),
                                ("b",("_build",True)),
                                ("p",("_patch", True)), #where should you be?
                                ("i",("_install",True)),
                                ("x",("_extend_sys_path",False)),
                                ("y",("_extend_python_path",False)),
                                ("e",("_eggify",True))
                                ])

egg_process_map = OrderedDict([("e",("_eggify",True)),
                                #("g",("_upload_egg",True))
                                ])
                                
                                
def main():

    # set some env variables for subprocesses
    os.environ["MAKE_FLAGS"] = "-j2"

    options = {}
    parse_process_flags(sys.argv, options)

    env = BuildEnvironment()
    env.set_options(options)
    with env:
        for proj in projs_dict.itervalues():
            proc_str = "PROCESSING " + proj.name
            print "\n",proc_str
            print "="*len(proc_str)
            # proc_flags is a string containing proj_process_map keys.
            # if a process is in proc_flags it gets forced.
            proc_flags = options["PROC_FLAGS"].get(proj.name, "")
            print "process flags are:", proc_flags

            builder = ProjectBuilders.builders[proj.name](options)
            for proc, (proc_func, skippable) in proj_process_map.iteritems():
                if proc in env.proc_flags[proj.name] and proc not in proc_flags and skippable:
                    print "\t-->ignoring %s for %s"%(proc_func, proj.name)
                    continue
                else:
                    print "\t-->performing %s for %s"%(proc_func, proj.name)
                    success = getattr(builder, proc_func)()
                    if not success :
                        print "\t-->%s for %s failed"%(proc_func, proj.name)
                        # break
                    else:
                        env.mark_proc_as_done(proj, proc)

        for egg in eggs:
            proc_str = "PROCESSING " + egg
            print "\n",proc_str
            print "="*len(proc_str)
            # proc_flags is a string containing process_map keys.
            # if a process is in proc_flags it gets forced.
            proc_flags = options["PROC_FLAGS"].get(egg, "")
            print "process flags are:", proc_flags

            builder = EggBuilders.builders[egg](options)            
            for proc, (proc_func, skippable) in egg_process_map.iteritems():
                if proc in env.proc_flags[proj.name] and proc not in proc_flags and skippable:
                    print "\t-->ignoring %s for %s"%(proc_func, proj.name)
                    continue
                else:
                    print "\t-->performing %s for %s"%(proc_func, proj.name)
                    success = getattr(builder, proc_func)()
                    if not success :
                        print "\t-->%s for %s failed"%(proc_func, proj.name)
                        # break
                    else:
                        env.mark_proc_as_done(proj, proc)


if __name__ ==  "__main__":
            main()