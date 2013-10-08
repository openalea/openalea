from openalea.release import Formula
from openalea.release.utils import pj
from path import path

class cmake(Formula):
    version        = '2.8.11.2'
    homepage       = "http://www.cmake.org/"
    download_url   = "http://www.cmake.org/files/v2.8/cmake-2.8.11.2-win32-x86.zip"
    download_name  = "cmake_src.zip"
    py_dependent   = False
    arch_dependent = True
    DOWNLOAD = UNPACK = EGGIFY = True
    
    def setup(self):
        return dict(BIN_DIRS = {'bin' : pj(self.sourcedir,'bin') },
                    LIB_DIRS = None,
                    INC_DIRS = {'share' : pj(self.sourcedir,'share') },
                    )
    def extra_paths(self):
        return path(self.sourcedir)