from openalea.release import Formula
from openalea.release.utils import sh, apply_patch
from os.path import join as pj, abspath, dirname

PATCH_DIR = abspath(dirname(__file__))

class ann(Formula):
    version = '1.1.2'
    homepage = "http://www.cs.umd.edu/~mount/ANN/"
    download_url = "http://www.cs.umd.edu/~mount/ANN/Files/"+version+"/ann_"+version+".zip"
    license = "GNU Lesser Public License"
    authors = "Copyright (c) 1997-2010 University of Maryland and Sunil Arya and David Mount"
    description = "Windows gcc libs and headers of ANN"
    download_name  = "ann_src.zip"
    py_dependent   = False
    arch_dependent = True
    patch_filename = pj(PATCH_DIR,"ann_mgw.patch")
    def setup(self):
        return dict(DATA_FILES = [('doc' , [pj(self.sourcedir,'doc','ANNmanual.pdf')] )],
                    LIB_DIRS         = {'lib' : pj(self.sourcedir,'lib') },
                    INC_DIRS         = {'include' : pj(self.sourcedir,'include') },
                    BIN_DIRS         = {'bin' : pj(self.sourcedir,'bin') },
                    )
    def patch(self):
        return apply_patch(self.patch_filename)
    def configure(self):
        return True
    def make(self):
        return sh("mingw32-make win32-g++") == 0
    def install(self):
        return True
        