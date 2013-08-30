from os.path import join as pj
import os
from openalea.release import Formula
from openalea.release.utils import recursive_copy, Pattern, makedirs
from openalea.release.formula.mingw import mingw

class mingw_rt(Formula):
    license = "PublicDomain for MingW runtime. GLP or LGPL for some libraries."
    authors = "The Mingw Project"
    description = "Mingw Development (compiler, linker, libs, includes)"
    py_dependent   = False
    arch_dependent = True
    version        = mingw.version
    download_url = None
    supported_tasks = "i"
    download_name  = "mingw"
    
    dependencies = ["mingw"]
    
    def __init__(self, *args, **kwargs):
        super(mingw_rt, self).__init__(*args, **kwargs)
        makedirs(self.eggdir)
        self.sourcedir = mingw().get_path()
        self.install_dll_dir = pj(self.installdir, "dll")
        
    def _unpack(self, arch=None):
        if not (os.path.isfile(self.sourcedir) or os.path.isdir(self.sourcedir)):
            mingw()._download()
            return mingw()._unpack()
        return True

    def make(self):
        return True
        
    def install(self):
        recursive_copy( pj(self.sourcedir, "bin"), self.install_dll_dir, Pattern.dynlib, levels=1)
        return True
        
    def setup(self):
        return dict( 
                    VERSION  = self.version,
                    LIB_DIRS = {"lib":self.install_dll_dir},
                    INC_DIRS = None,
                    BIN_DIRS = None,
                    )             
