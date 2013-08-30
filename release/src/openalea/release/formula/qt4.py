from openalea.release import Formula
from openalea.release.formula.mingw import mingw
from openalea.release.formula.mingw_rt import mingw_rt
from openalea.release.utils import uj, recursive_glob, recursive_glob_as_dict, \
 recursive_copy, apply_patch, makedirs, Pattern
from os.path import join as pj, abspath, dirname
import subprocess
import ConfigParser
import time
import os
from setuptools import find_packages
# Warnings : other imports in the setup

PATCH_DIR = abspath(dirname(__file__))

# Warning: really long compiling...
class qt4(Formula):
    #version = "4.7.4"
    version = "4.8.5"
    #download_url = "http://get.qt.nokia.com/qt/source/qt-everywhere-opensource-src-"+version+".zip"
    download_url = "http://download.qt-project.org/official_releases/qt/4.8/4.8.5/qt-everywhere-opensource-src-"+version+".zip"
    download_name  = "qt4_src.zip"

    license = "General Public License V3"
    authors = "Riverbank Computing (Sip+PyQt4+QSCintilla) & Nokia (Qt4)"
    description = "Sip+PyQt4+QScintilla Runtime packaged as an egg for windows-gcc"
    py_dependent   = True
    arch_dependent = True
    
    def __init__(self, *args, **kwargs):
        super(qt4, self).__init__(*args, **kwargs)
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
        self.inst_paths = [getattr(self, attr) for attr in dir(self) if attr.startswith("install_") and attr.endswith("_dir")]

    def new_env_vars(self):
        if mingw().version_gt("4.6.0"):
            return [ ("QMAKESPEC","win32-g++-4.6") ]
        else:
            return [ ("QMAKESPEC","win32-g++") ]

    def configure(self):
        # we must rename syncqt[.bat] files in the bin directory if they exist.
        syncqtfiles = recursive_glob( "bin", "syncqt*")
        for sqt in syncqtfiles:
            os.rename(sqt, sqt+"_no_use")
            
        # we must patch the sources in some cases
        if self.version == "4.8.0" :#and mingw().version_gt("4.7.0"):
            apply_patch(  pj(PATCH_DIR,"qt-4.8.0.patch") )
            
        # build the configure command line
        # more details on options:
        # http://qt-project.org/doc/qt-4.8/configure-options.html
        common = " -platform win32-g++"
        common += " -release -opensource -shared -nomake demos -nomake examples -mmx -sse2 -3dnow"
        common += " -declarative -webkit -no-cetest -qt-zlib"        
        cmd = "configure.exe" + common
        if mingw().version_gt("4.6.0"):
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
 
    def setup(self):  
        from openalea.release.formula.pyqt4 import pyqt4
        from openalea.release.formula.pyqscintilla import pyqscintilla
        from openalea.release.formula.sip import sip    
        
        pyqt4_ = pyqt4()
        pysci_ = pyqscintilla()
        sip_   = sip()
        # dlls are the union of qt dlls and plugins directories (which is actually the same!)
        # qscis apis are recursive from qt4 (need to list all files)        
        qscis    = recursive_glob_as_dict(pysci_.qsci_dir, Pattern.sciapi, strip_keys=True, prefix_key="qsci").items()
        extra_pyqt4_mods = recursive_glob_as_dict(pj(pyqt4_.install_site_dir,"PyQt4"), Pattern.pyall, strip_keys=True, prefix_key="PyQt4").items()
        # print extra_pyqt4_mods
        sip_mods = recursive_glob_as_dict(sip_.install_site_dir, Pattern.pyall, strip_keys=True, levels=1).items()

        lib_dirs    = {"PyQt4": self.install_dll_dir}
        package_dir = {"PyQt4": pj(pyqt4_.install_site_dir, "PyQt4")}
        
        d  = dict( 
                    VERSION  = self.version,
                    PACKAGES = find_packages(pyqt4_.install_site_dir, "PyQt4"),
                    PACKAGE_DIRS = package_dir,
                    PACKAGE_DATA = {'' : [Pattern.pyext]},
                    
                    LIB_DIRS         = lib_dirs,
                    DATA_FILES       = qscis+sip_mods+extra_pyqt4_mods,
                    INSTALL_REQUIRES = [mingw_rt().egg_name()]
                    )   
        return d