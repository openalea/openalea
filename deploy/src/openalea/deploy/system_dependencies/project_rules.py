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

####################################################################################################
# - PROJECT BUILDERS - PROJECT BUILDERS - PROJECT BUILDERS - PROJECT BUILDERS - PROJECT BUILDERS - #
# !!!!          THE ORDER OF CLASS DEFINITIONS IS THE ORDER OF PROJECT COMPILATION             !!!!#
####################################################################################################
class mingwrt(BaseProjectBuilder):
    url = None
    supported_tasks = "i"
    download_name  = "mingw"
    archive_subdir = None
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        self.sourcedir = pj(Compiler.get_bin_path(), os.pardir)
        self.install_dll_dir = pj(self.installdir, "dll")

    def install(self):
        recursive_copy( pj(self.sourcedir, "bin"), self.install_dll_dir, Pattern.dynlib, levels=1)
        return True



class qt4(BaseProjectBuilder):
    version = "4.7.4"
    #version = "4.8.0"
    url = "http://get.qt.nokia.com/qt/source/qt-everywhere-opensource-src-"+version+".zip"
    download_name  = "qt4_src.zip"
    archive_subdir = "qt-every*"

    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        # define installation paths
        self.install_bin_dir = pj(self.installdir, "bin")
        self.install_dll_dir = pj(self.installdir, "dll")
        self.install_lib_dir = pj(self.installdir, "lib")
        self.install_src_dir = pj(self.installdir, "src")
        self.install_inc_dir = pj(self.installdir, "include")
        self.install_plu_dir = pj(self.installdir, "dll")
        self.install_plu_lib_dir = pj(self.installdir, "plugins_lib")
        self.install_mks_dir = pj(self.installdir, "mkspecs")
        self.install_tra_dir = pj(self.installdir, "translations")
        self.inst_paths = [getattr(self, attr) for attr in dir(self) if attr.startswith("install_")\
                           and attr.endswith("_dir")]

    def new_env_vars(self):
        if Compiler.version_gt("4.6.0"):
            return [ ("QMAKESPEC","win32-g++-4.6") ]
        else:
            return [ ("QMAKESPEC","win32-g++") ]

    def configure(self):
        # we must rename syncqt[.bat] files in the bin directory if they exist.
        syncqtfiles = recursive_glob( "bin", "syncqt*")
        for sqt in syncqtfiles:
            os.rename(sqt, sqt+"_no_use")
            
        # we must patch the sources in some cases
        if self.version == "4.8.0" :#and Compiler.version_gt("4.7.0"):
            apply_patch(  pj(ModuleBaseDir,"qt-4.8.0.patch") )
            
        # build the configure command line
        common = " -release -opensource -shared -nomake demos -nomake examples -mmx -sse2 -3dnow"
        common += " -declarative -webkit -no-s60 -no-cetest"        
        cmd = "configure.exe" + common
        if Compiler.version_gt("4.6.0"):
            # TDM doesn't ship with DirectX headers. Cannot use Phonon
            # Actually this is useless as configure.exe will check himself.
            cmd += " -no-phonon" #  + " -no-declarative"
        # PIPE is required or else pop.communicate won't do anything!
        pop = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        # give enough time for executable to load before it asks for license agreement.
        time.sleep(2)
        # accepts license agreement, also waits for configure to finish
        pop.communicate("y\r")
        return pop.returncode == 0

    def install(self):
        # create the installation directories
        for pth in self.inst_paths:
            makedirs(pth)
        # copy binaries
        recursive_copy( pj(self.sourcedir, "bin"), self.install_bin_dir, Pattern.exe )
        # add a qt.conf file that tells qmake to look into
        # directories that are relative to the executable.
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
        self.make_qt_conf()
        return True

    def extra_paths(self):
        return pj(self.sourcedir, "bin")

    def make_qt_conf(self, where=None):
        """ Patch qt *.exes and *.dlls so that they do not contain hard coded paths anymore. """
        config = ConfigParser.RawConfigParser()
        sec = "Paths"
        config.add_section(sec)
        if where == None:
            config.set(sec, "Headers",	 "../include")
            config.set(sec, "Libraries", "../lib")
            config.set(sec, "Binaries",  "../bin")
            config.set(sec, "Plugins",   "../dll")
            #config.set(sec, "Imports"	"no idea")
            config.set(sec, "Data",      "..")
            config.set(sec, "Translations", "../translations")
        else:
            unix_installdir = self.installdir.replace("\\", "/")
            config.set(sec, "Headers",	 uj(unix_installdir, "include"))
            config.set(sec, "Libraries", uj(unix_installdir, "lib"))
            config.set(sec, "Binaries",  uj(unix_installdir, "bin"))
            config.set(sec, "Plugins",   uj(unix_installdir, "dll"))
            #config.set(sec, "Imports"	"no idea")
            config.set(sec, "Data",      unix_installdir )
            config.set(sec, "Translations", uj(unix_installdir, "translations")  )      
        # Writing our configuration file
        if where is None:
            where = self.install_bin_dir
        with open(pj(where, 'qt.conf'), 'w') as configfile:
            config.write(configfile)
        return True



class sip(BaseProjectBuilder):
    url = "http://www.riverbankcomputing.com/hg/sip/archive/0869eb93c773.zip" #downloading from the mercurial tag
    #url = "http://www.riverbankcomputing.co.uk/static/Downloads/sip4/sip-4.13.2.zip"
    download_name  = "sip_src.zip"
    archive_subdir = "sip*"
    
    required_tools = [bisonflex]

    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        # we install pyqt4 binaries in the qt bin installation directory to easily recover it
        # for the egg. The eggs are built in the historical layout used by openalea packagers.
        # This doesn't mean it's good. It doesn't mean it's bad though it does look a bit messy.
        qt4_ = qt4()
        self.install_bin_dir  = qt4_.install_bin_dir
        self.install_site_dir = pj(self.installdir, "site")
        self.install_inc_dir  = pj(self.installdir, "include")
        self.install_sip_dir  = pj(self.installdir, "sip")

        self.inst_paths = self.install_bin_dir, self.install_site_dir, self.install_inc_dir, \
                          self.install_sip_dir

    @option_to_sys_path("bisonflex_path")
    def configure(self):
        if exists(pj(self.sourcedir,"configure.py") ):
            print "it's alive!"
            # The -S flag is needed or else configure.py
            # sees any existing sip installation and can fail.
            return subprocess.call(sys.executable + \
                   " -S configure.py --platform=win32-g++ -b %s -d %s -e %s -v %s"%self.inst_paths) == 0
        else:
            #if configure.py doesn't exist then we might
            #be using a zipball retreived directly from
            #sip's mercurial repository. This type of source
            #needs a step before actually calling configure.py
            if exists("build.py"):
                print "Will try to build sip from mercurial source zipball"
                try:
                    #We neeeed bison and flex
                    subprocess.call("bison.exe")
                except:
                    print "Could not find bison flex, use --bisonflex"
                    return False
                apply_patch( pj(ModuleBaseDir,"sip_build.patch") )
                subprocess.call(sys.executable + " -S build.py prepare")
                return self.configure()
            else:
                #we don't have a clue of what type of source we're in
                #so dying cleanly can seem like a good option:
                return False

    def extra_paths(self):
        return self.sourcedir, pj(self.sourcedir, "sipgen")

    def extra_python_paths(self):
        return self.sourcedir, pj(self.sourcedir, "siplib")

    def patch(self):
        return True
        # Patching sipconfig.py so that its
        # paths point to the qt4 egg path we are building.
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

        # inject our new header
        txt = txt.replace("import re", header)

        prefix = sys.prefix.replace("\\", r"\\\\")
        # Evil massive regexp substitutions. RegExp are self-explanatory! Just kidding...
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
        with open( pj(self.install_site_dir,"sipconfig.py"), "w") as f:
            f.write(txt)

        return True



class pyqt4(BaseProjectBuilder) :
    url = "http://pypi.python.jp/PyQt/PyQt-win-gpl-4.8.6.zip#md5=734bb1b8e6016866f4450211fc4770d9"
    #url = "http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-win-gpl-4.9.1.zip"
    download_name  = "pyqt4_src.zip"
    archive_subdir = "PyQt*"
    
    cmd_options = [ ("siphome", None, "Path to sip.exe"),
                    ("sipsite", None, "Path(s) to sip modules (';' seperated)") ]

    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        # we install pyqt4 binaries in the qt bin installation directory to easily recover it
        # for the egg. The eggs are built in the historical layout used by openalea packagers.
        # This doesn't mean it's good. It doesn't mean it's bad though it does look a bit messy.
        qt4_ = qt4()
        self.install_bin_dir  = qt4_.install_bin_dir
        self.install_site_dir = pj(self.installdir,"site")
        self.install_sip_dir  = pj(self.installdir,"sip")
        self.inst_paths       = self.install_bin_dir, self.install_site_dir, self.install_sip_dir

    @option_to_python_path("sipsite")
    @option_to_sys_path("siphome")
    def configure(self):
        # The -S flag is needed or else configure.py
        # sees any existing sip installation and can fail.
        # subprocess.call(sys.executable + \
                      # " -S configure.py --help")
        # return False
        qt4_ = qt4()
        #qtconf_dir = pj(self.sourcedir.replace("\\", "/"),"release")
        #makedirs( qtconf_dir )
        #qt4_.make_qt_conf(where=qtconf_dir)
        return subprocess.call(sys.executable + \
                      " -S configure.py --confirm-license -w -b %s -d %s -v %s"%self.inst_paths) == 0

    def extra_paths(self):
        return self.install_bin_dir

    def extra_python_paths(self):
        return self.install_site_dir

    def patch(self):
        return True
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
    url = "http://www.riverbankcomputing.co.uk/static/Downloads/QScintilla2/QScintilla-gpl-2.6.1.zip"
    download_name  = "qscintilla_src.zip"
    archive_subdir = "QScint*/Qt4"

    def configure(self):
        # The install procedure will install qscintilla in qt's installation directories
        qt4_ = qt4()
        paths = qt4_.install_inc_dir, qt4_.install_tra_dir, qt4_.installdir, qt4_.install_dll_dir,
        return subprocess.call( ("qmake -after header.path=%s trans.path=%s qsci.path=%s " + \
                                 "target.path=%s -spec win32-g++ qscintilla.pro")%paths) == 0
    def install(self):
        ret = BaseProjectBuilder.install(self)
        qt4_ = qt4()
        try:
            shutil.move( pj(qt4_.install_dll_dir, "libqscintilla2.a"), qt4_.install_lib_dir)
        except Exception, epyqt :
            print e
        return ret



class pyqscintilla(BaseProjectBuilder):
    url = None # shares the same as qscintilla
    download_name  = "qscintilla_src.zip"
    archive_subdir = "QScint*/Python"

    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        # define installation paths
        qsci = qscintilla()
        qt4_ = qt4()
        pyqt = pyqt4()
        self.install_paths = pj(qsci.sourcedir,"release"), pj(qt4_.installdir, "qsci"), \
                             qsci.sourcedir, pj(pyqt.install_site_dir, "PyQt4"), \
                             pyqt.install_sip_dir
        self.qsci_dir = self.install_paths[1]

    def configure(self):
        # we want pyqscintilla to install itself where pyqt4 installed itself.
        # -- The -S flag is needed or else configure.py
        # sees any existing sip installation and can fail. --
        return subprocess.call(sys.executable + \
               " -S configure.py -o %s -a %s -n %s -d %s -v %s"%self.install_paths ) == 0



class qglviewer(BaseProjectBuilder):
    url = "https://gforge.inria.fr/frs/download.php/28138/libQGLViewer-2.3.9-py.tgz"
    download_name  = "qglviewer_src.tgz"
    archive_subdir = "libQGLV*/QGLViewer"

    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
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
    url = "https://gforge.inria.fr/frs/download.php/28212/PyQGLViewer-0.9.1.zip"
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
        # The -S flag is needed or else configure.py
        # sees any existing sip installation and can fail.
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
    url = "http://switch.dl.sourceforge.net/project/boost/boost/1.48.0/boost_1_48_0.zip"
    download_name  = "boost_src.zip"
    archive_subdir = "boost*"

    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        self.install_inc_dir = pj(self.installdir, "include")
        self.install_lib_dir = pj(self.installdir, "lib")

    def configure(self):
        return True #bjam configures, builds and installs so nothing to do here

    def build(self):
        # it is possible to bootstrap boost if no bjam.exe is found:
        if not exists( pj(self.sourcedir, "bjam.exe") ):
            print "Call bootstrap.bat"
            if subprocess.call("bootstrap.bat mingw") != 0:
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
        cmd = "bjam --debug-configuration --prefix=%s --without-test --layout=system"
        cmd += " variant=release link=shared threading=multi runtime-link=shared toolset=gcc"
        cmd += " include=%s library-path=%s install"
        cmd %= paths
        print cmd
        return subprocess.call(cmd) == 0

    def install(self):
        """ bjam configures, builds and installs so nothing to do here"""
        return self.build()

        
        
class ann(BaseProjectBuilder):
    version = '1.1.2'
    url = "http://www.cs.umd.edu/~mount/ANN/Files/"+version+"/ann_"+version+".zip"
    download_name  = "ann_src.zip"
    archive_subdir = "ann*"
    enabled = True

    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        self.patchfile = pj(ModuleBaseDir,"ann_mgw.patch")
        self.install_inc_dir = pj(self.sourcedir, "include")
        self.install_lib_dir = pj(self.sourcedir, "lib")
        
    def configure(self):
        apply_patch(self.patchfile)
        return True

    def build(self):
        return subprocess.call("mingw32-make win32-g++") == 0

    def install(self):
        return True



class gnuplot(BaseProjectBuilder):
    url = "http://heanet.dl.sourceforge.net/project/gnuplot/gnuplot/4.4.4/gp444win32.zip"
    download_name  = "gnuplot_src.zip"
    archive_subdir = "gnuplot*"
    enabled = False

    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        self.install_inc_dir = pj(self.installdir, "include")
        self.install_lib_dir = pj(self.installdir, "lib")
    def configure(self):
        return True

    def build(self):
        return True

    def install(self):
        return True



class qhull(BaseProjectBuilder):
    url = "http://www.qhull.org/download/qhull-2011.2.zip"
    download_name  = "qhull_src.zip"
    archive_subdir = "qhull*"
    enabled = False

    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        self.install_inc_dir = pj(self.installdir, "include")
        self.install_lib_dir = pj(self.installdir, "lib")
    
    def configure(self):
        return True

    def build(self):
        return True
    
    def install(self):
        return True

        
        
class cgal(BaseProjectBuilder):
    url = "https://gforge.inria.fr/frs/download.php/30390/CGAL-4.0.zip"
    download_name  = "cgal_src.zip"
    archive_subdir = "cgal*"
    required_tools = [cmake]
    enabled = True
    version = "4.0"
    def __init__(self, *args, **kwargs):
        BaseProjectBuilder.__init__(self, *args, **kwargs)
        self.install_inc_dir = pj(self.installdir, "include")
        self.install_lib_dir = pj(self.installdir, "lib")
    
    def configure(self):
        compiler = Compiler.get_bin_path()
        boost_ = boost()
        
        db_quote = lambda x: '"'+x+'"'
        
        options = " ".join(['-DCMAKE_INSTALL_PREFIX='+db_quote(self.installdir),
                            '-DCMAKE_CXX_COMPILER:FILEPATH='+db_quote(pj(compiler,'g++.exe')),
                            '-DBOOST_ROOT='+db_quote(boost_.installdir),
                            '-DGMP_INCLUDE_DIR='+db_quote( pj(compiler, "..", "include") ),
                            '-DMPFR_INCLUDE_DIR='+db_quote( pj(compiler, "..", "include") ),
                            '-DZLIB_INCLUDE_DIR='+db_quote(pj(compiler, "..", "include")),
                            '-DZLIB_LIBRARY='+db_quote(pj(compiler,"..", "lib", "libz.a")),
                            #'-DOPENGL_LIBRARIES='+db_quote(pj(compiler,"..", "lib", "libglu32.a")),
                            ])
        options=options.replace("\\", "/") #avoid "escape sequence" errors with cmake
        cmd = 'cmake.exe -G"MinGW Makefiles" '+options+' . '
        print cmd
        return subprocess.call(cmd) == 0
                            
        
    
class rpy2(BaseProjectBuilder):
    version = "2.3"
    revision = "f075a4291e9c"
    url = "https://bitbucket.org/lgautier/rpy2/get/"+revision+".zip"
    download_name  = "rpy2_src.zip"
    archive_subdir = "lgautier-rpy2*"
    
    cmd_options = [ ("rhome", None, "Path to R.exe") ]

    @option_to_sys_path("rhome")
    def configure(self):
        apply_patch( pj(ModuleBaseDir,"rpy2.patch") )
        return True
        
    @option_to_sys_path("rhome")
    def build(self):
        cmd = sys.executable + " setup.py build --compiler=mingw32"
        return subprocess.call(cmd) == 0
        
    @option_to_sys_path("rhome")
    def install(self):
        cmd = sys.executable + " setup.py install --install-lib=" + self.installdir
        return subprocess.call(cmd) == 0