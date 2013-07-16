from openalea.release import Formula
from openalea.release.utils import sh, option_to_sys_path, apply_patch, Pattern
from os.path import join as pj, abspath, dirname
import sys

PATCH_DIR = abspath(dirname(__file__))

class rpy2(Formula):
    version = "2.3"
    # revision = "f075a4291e9c"
    # revision = "436e3f9"
    revision = "RELEASE_2_3_6"
    download_url = "https://bitbucket.org/lgautier/rpy2/get/"+revision+".zip"
    download_name  = "rpy2_src.zip"
    archive_subdir = "lgautier-rpy2*"
    homepage = "http://rpy.sourceforge.net"
    
    cmd_options = [ ("R", None, "Path to R.exe") ]

    license = "AGPLv3.0 (except rpy2.rinterface: LGPL)"
    authors = "Laurent Gautier"
    description = "Unofficial Windows gcc libs and includes of rpy2"
    py_dependent   = True
    arch_dependent = True
    
    def setup(self):
        from setuptools import find_packages
        return dict(URL          = self.homepage,
                    PACKAGES     = find_packages(self.installdir,"rpy2"),
                    PACKAGE_DIRS = { "rpy2": pj(self.installdir, "rpy2") },
                    VERSION      = self.version+".rev"+self.revision,
                    PACKAGE_DATA = {'' : [Pattern.pyext]},
                    LIB_DIRS         = None,
                    INC_DIRS         = None,
                    BIN_DIRS         = None,
                    )

    @option_to_sys_path("R")
    def patch(self):
        apply_patch( pj(PATCH_DIR,"rpy2.patch") )
        return True
        
    def configure(self):
        return True
        
    @option_to_sys_path("R")
    def make(self):
        cmd = sys.executable + " setup.py build_ext --compiler=mingw32"
        return sh(cmd) == 0
        
    @option_to_sys_path("R")
    def install(self):
        cmd = sys.executable + " setup.py install --install-lib=" + self.installdir
        return sh(cmd) == 0          