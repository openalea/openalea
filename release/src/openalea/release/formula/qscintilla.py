from openalea.release import Formula
from openalea.release.utils import recursive_copy
from openalea.release.compiler import Compiler
import os

MINGW_PATH = ''

class mingw_rt(Formula):
    license = "PublicDomain for MingW runtime. GLP or LGPL for some libraries."
    authors = "The Mingw Project"
    description = "Mingw Development (compiler, linker, libs, includes)"
    py_dependent   = False
    arch_dependent = True
    version        = "5.1.4_4b"
    download_url = None
    supported_tasks = "i"
    download_name  = "mingw"
    archive_subdir = None
    def __init__(self, *args, **kwargs):
        super(mingw_rt, self).__init__(*args, **kwargs)
        self.sourcedir = MINGW_PATH if MINGW_PATH else pj(Compiler.get_bin_path(), '..')
        self.install_dll_dir = pj(self.installdir, "dll")

    def install(self):
        recursive_copy( pj(self.sourcedir, "bin"), self.install_dll_dir, Pattern.dynlib, levels=1)
        return True
        
    def configure_init_py(self):
        return dict( 
                    VERSION  = self.version,
                    LIB_DIRS = {"bin":self.install_dll_dir},
                    )             