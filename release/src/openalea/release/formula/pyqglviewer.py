from openalea.release import Formula
from openalea.release.utils import recursive_copy, pj, sh, recursive_glob_as_dict, \
merge_list_dict, Pattern

from openalea.release.formula.qglviewer import qglviewer
from openalea.release.formula.qt4 import qt4

import sys
import os

class pyqglviewer(Formula):
    license = "General Public License"
    authors = "libQGLViewer developers for libQGLViewer, PyQGLViewer (INRIA) developers for PyQGLViewer"
    description = "Win-GCC version of PyQGLViewer"
    py_dependent   = True
    arch_dependent = True
    download_url = "https://gforge.inria.fr/frs/download.php/28212/PyQGLViewer-0.9.1.zip"
    download_name  = "pyqglviewer_src.zip"
    DOWNLOAD = UNPACK = CONFIGURE = MAKE = MAKE_INSTALL = EGGIFY = True

    def __init__(self, *args, **kwargs):
        super(pyqglviewer, self).__init__(*args, **kwargs)
        qglbuilder = qglviewer()
        self.qglbuilderbase = pj(qglbuilder.sourcedir, os.path.pardir),
        self.install_sip_dir  = pj(qglbuilder.installdir, "sip")
        self.install_site_dir = qglbuilder.installdir
        self.install_exa_dir  = pj(qglbuilder.installdir, "examples")

    def configure(self):
        # The -S flag is needed or else configure.py
        # sees any existing sip installation and can fail.
        return sh(sys.executable + " -S configure.py -Q %s "%self.qglbuilderbase) == 0

    def make_install(self):
        """ pyqglviewer installs itself into the same directory as qglviewer """
        recursive_copy( pj(self.sourcedir, "build"), self.install_site_dir, Pattern.pyext, levels=1)
        recursive_copy( pj(self.sourcedir, "src", "sip"), self.install_sip_dir, Pattern.sipfiles, levels=1)
        recursive_copy( pj(self.sourcedir, "examples"), self.install_exa_dir, Pattern.any)
        return True

    def extra_python_paths(self):
        qglbuilder = qglviewer()
        return qglbuilder.installdir
        
    def script_substitutions(self):
        qt4_   = qt4()
        qglv_   = qglviewer()
        
        pyqgl_mods = recursive_glob_as_dict(self.install_site_dir, Pattern.pyall, strip_keys=True, levels=1).items()
        # includes are recursive subdirectories of qglviewer           
        incs = recursive_glob_as_dict( qglv_.install_inc_dir, Pattern.include, strip_keys=True, prefix_key="include", dirs=True).items()
        inc_dirs = merge_list_dict( incs )
        # libs are recursive subdirectories of qt libs          
        libs = recursive_glob_as_dict(qglv_.install_lib_dir, Pattern.qtstalib, strip_keys=True, prefix_key="lib").items()
        # sip files are recursive subdirectories of pyqglviewer sip installation directory
        sips = recursive_glob_as_dict(self.install_sip_dir, Pattern.sipfiles, strip_keys=True, prefix_key="sip").items()
        # examples are recursive subdirectories of pyqglviewer examples installation directory contains various types of files
        exas = recursive_glob_as_dict(self.install_exa_dir, Pattern.any, strip_keys=True, prefix_key="examples").items()        
        
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
                    INSTALL_REQUIRES = [qt4_.egg_name()]
                    )  


