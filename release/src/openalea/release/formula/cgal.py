from openalea.release import Formula
from openalea.release.utils import sh
from openalea.release.formula.boost import boost
from openalea.release.formula.mingw import mingw
from os.path import join as pj
import os
from openalea.release.tools.cmake import cmake

class cgal(Formula):
    license = "GNU Lesser Public License"
    authors = "CGAL, Computational Geometry Algorithms Library"
    description = "Windows gcc libs and includes of CGAL"
    py_dependent   = False
    arch_dependent = True  
    homepage = "http://www.cgal.org/"
    download_url = "https://gforge.inria.fr/frs/download.php/30390/CGAL-4.0.zip"
    download_name  = "cgal_src.zip"
    archive_subdir = "cgal*"
    required_tools = [cmake]
    version = "4.0"
    def setup(self):
        return dict( 
                    VERSION          = self.version,
                    LIB_DIRS         = {'lib' : pj(self.sourcedir,'lib') },
                    INC_DIRS         = {'include' : pj(self.sourcedir,'include') },
                    BIN_DIRS         = {'bin' : pj(self.sourcedir,'bin') },
                    ) 
    def configure(self):
        compiler = mingw().get_bin_path()
        boost_ = boost()
        boost_._fix_source_dir()
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
        return sh(cmd) == 0   
'''    def make(self):
        return True
    def install(self):
        return True'''