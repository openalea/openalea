from openalea.release import Formula
from openalea.release.utils import recursive_glob_as_dict, memoize, sh
import os, sys
from os.path import join as pj
from re import compile as re_compile
import subprocess
import time

class mingw(Formula):
    download_url = "https://gforge.inria.fr/frs/download.php/29029/MinGW-5.1.4_2-win32.egg"
    download_name = "mingw.zip"
    license = "PublicDomain for MingW runtime. GLP or LGPL for some libraries."
    authors = "The Mingw Project"
    description = "Mingw Runtime"
    py_dependent   = False
    arch_dependent = True
    version        = "5.1.4_4b"

    def setup(self):
        cpath = self.get_bin_path()
        mingwbase = pj(cpath,"..")
        subd  = os.listdir( mingwbase )
        safe_rmdir("EGG-INFO", subd)
        safe_rmdir("bin", subd)
        safe_rmdir("include", subd)
        data = []
        for dir in subd:
            dat = recursive_glob_as_dict(pj(mingwbase,dir), "*", strip_keys=True, prefix_key=dir).items()         
            data += [ (d, [f for f in t if not f.endswith(".dll")]) for d,t in dat]
        bindirs = {"bin": cpath}
        incdirs = {"include": pj(mingwbase, "include")}   
        return dict( 
                    VERSION  = self.version,
                    BIN_DIRS = bindirs,
                    INC_DIRS = incdirs,
                    DATA_FILES   = data,
                    )
                    
    def configure(self):
        # Doesn't need installation : download and unpack is enought
        return True
        
    def make(self):
        # Doesn't need installation : download and unpack is enought
        return True  
        
    def install(self):
        # Doesn't need installation : download and unpack is enought
        return True
 
    def get_bin_path(self):
        # works well ?
        if "win32" not in sys.platform:
            return "/usr/bin"
        if self.options.get("compiler"):
            v =  self.options["compiler"]
            if os.path.exists(v):
                return v
        else:
            return r"c:\mingw\bin"    
            
    def is_installed(self):
        compiler = os.path.join(self.get_bin_path(),"gcc.exe")
        try:
            sh(compiler+" --version")
            return True
        except OSError:
            return False  
          
    def version_gt(self, version):
        return self.get_version() >= version
        
    @memoize("version")
    def get_version(self):
        pop = subprocess.Popen( pj(self.get_bin_path(), "gcc --version"),
                                           stdout=subprocess.PIPE)
        time.sleep(1)
        output = pop.stdout.read()
        reg = re_compile(r"(\d\.\d.\d)")
        return reg.search(output).group(1)
        
def safe_rmdir(dirname, listdir):
    """ Remove dirname only if exists in listdir
    """
    if dirname in listdir:
        listdir.remove(dirname)