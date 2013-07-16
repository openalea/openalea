from openalea.release import Formula
from openalea.release.utils import sh, pj
from path import path
import glob

class cmake(Formula):
    version        = '2.8.11.2'
    homepage       = "http://www.cmake.org/"
    download_url   = "http://www.cmake.org/files/v2.8/cmake-2.8.11.2-win32-x86.zip"
    download_name  = "cmake_src.zip"
    py_dependent   = False
    arch_dependent = True
    def configure(self):
        return True
    def make(self):
        return True
    def install(self):
        return True
    def setup(self):
        return dict(BIN_DIRS = {'bin' : pj(self.sourcedir,'bin') },
                    LIB_DIRS = None,
                    INC_DIRS = {'share' : pj(self.sourcedir,'share') },
                    )
    def post_install(self):
        egg = glob.glob( pj(self._get_dl_path(), "*.egg") )[0]
        cmd = "alea_install -H None -f . %s" %egg
        return sh(cmd)
    def extra_paths(self):
        return path(self.sourcedir)