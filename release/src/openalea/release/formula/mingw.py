from openalea.release import Formula
from openalea.release.utils import recursive_glob_as_dict, memoize, sh, makedirs, install
import os, sys
import glob
from os.path import join as pj
from re import compile as re_compile
from path import path
import subprocess
import time
import warnings

class mingw(Formula):
    download_url = "https://gforge.inria.fr/frs/download.php/29029/MinGW-5.1.4_2-win32.egg"
    download_name = "mingw.zip"
    license = "PublicDomain for MingW runtime. GLP or LGPL for some libraries."
    authors = "The Mingw Project"
    description = "Mingw Runtime"
    py_dependent   = False
    arch_dependent = True
    version        = "5.1.4_4b"
    
    def _unpack(self, arch=None):
        arch = arch or self.archname
        ret = self.unpack(arch, self.get_path())
        return ret 

    def setup(self):
        mingwbase = self.get_path()
        if not path(mingwbase).exists():
            makedirs(path(mingwbase))
        subd  = os.listdir( mingwbase )
        safe_rmdir("EGG-INFO", subd)
        safe_rmdir("bin", subd)
        safe_rmdir("include", subd)
        data = []
        for dir in subd:
            dat = recursive_glob_as_dict(pj(mingwbase,dir), "*", strip_keys=True, prefix_key=dir).items()         
            data += [ (d, [str(f) for f in t if not f.endswith(".dll")]) for d,t in dat]
        bindirs = {"bin": str(self.get_bin_path())}
        incdirs = {"include": str(pj(mingwbase, "include"))}   
        #libdirs = {"lib": str(pj(mingwbase, "lib"))}  
        return dict( 
                    VERSION  = self.version,
                    BIN_DIRS = bindirs,
                    INC_DIRS = incdirs,
                    LIB_DIRS = None,
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
        
    def post_install(self):
        eggd = str(path(self.eggdir)/"dist")
        egg = glob.glob( pj(eggd, "*.egg") )[0]
        cmd = "alea_install -H None -f . %s" %egg
        return sh(cmd)
 
    def get_bin_path(self):
        # works well ?
        if "win32" not in sys.platform:
            return "/usr/bin"
        if self.options.get("compiler"):
            v =  self.options["compiler"]
            if os.path.exists(v):
                return v
        else:
            return self.get_path()/"bin"  
            
    def get_path(self):
        return path("c:\\MinGW")
    
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
        
        
        
        
        
        

#############TO DO###################
## Download MinGW-get-installer
    ## http://sourceforge.net/projects/mingw/files/latest/download?source=files
    ## or http://sourceforge.net/projects/mingw/files/Installer/mingw-get-setup.exe/download?use_mirror=switch&r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fmingw%2Ffiles%2F&use_mirror=switch
## Install MinGW thx to installer
## Get dependencies:
    ## mingw-get install zlib
    ## mingw-get install gmp
    ## mingw-get install mpfr
## Bdist egg
#####################################

class mingw_new(Formula):
    """
    New formula to create egg MinGW with 3rd party packages:
        - zlib
        - gmp
        - mpfr
    
    Work in progress.
    """
    download_url = "http://sourceforge.net/projects/mingw/files/latest/download?source=files"
    download_name = "mingw.exe"
    
    license = "PublicDomain for MingW runtime. GLP or LGPL for some libraries."
    authors = "The Mingw Project"
    description = "Mingw Runtime"
    py_dependent   = False
    arch_dependent = True
    version        = "5.1.4_4b"
    
    def __init__(self, *args, **kwargs):
        super(mingw, self).__init__(*args, **kwargs)
        self.sourcedir = self.get_path()
    
    def _unpack(self, arch=None):
        """ 
        Install MinGW thx to installer
        and Get dependencies:
            mingw-get install zlib
            mingw-get install gmp
            mingw-get install mpfr
        """
        mingw_get_installer = path(self._get_dl_path())/self.download_name
        print mingw_get_installer
        ret = install(mingw_get_installer) 
        print ret
        ret = ret & sh("mingw-get install zlib")
        print ret
        ret = ret & sh("mingw-get install gmp")
        print ret
        ret = ret & sh("mingw-get install mpfr")
        print ret       
        return ret

    def setup(self):
        mingwbase = self.get_path()
        if not path(mingwbase).exists():
            message = ""+ mingwbase + " doesn't exists! Please be sure that Mingw is well installed at " + self.get_path() +""
            warnings.warn(message)
            makedirs(path(mingwbase))
        subd  = os.listdir( mingwbase )
        safe_rmdir("EGG-INFO", subd)
        safe_rmdir("bin", subd)
        safe_rmdir("include", subd)
        data = []
        for dir in subd:
            dat = recursive_glob_as_dict(pj(mingwbase,dir), "*", strip_keys=True, prefix_key=dir).items()         
            data += [ (d, [str(f) for f in t if not f.endswith(".dll")]) for d,t in dat]
        bindirs = {"bin": str(self.get_bin_path())}
        incdirs = {"include": str(pj(mingwbase, "include"))}   
        #libdirs = {"lib": str(pj(mingwbase, "lib"))}  
        return dict( 
                    VERSION  = self.version,
                    BIN_DIRS = bindirs,
                    INC_DIRS = incdirs,
                    LIB_DIRS = None,
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
        
    def post_install(self):
        eggd = str(path(self.eggdir)/"dist")
        egg = glob.glob( pj(eggd, "*.egg") )[0]
        cmd = "alea_install -H None -f . %s" %egg
        return sh(cmd)
 
    def get_bin_path(self):
        # works well ?
        if "win32" not in sys.platform:
            return "/usr/bin"
        if self.options.get("compiler"):
            v =  self.options["compiler"]
            if os.path.exists(v):
                return v
        else:
            return self.get_path()/"bin"  
            
    def get_path(self):
        return path("c:\\MinGW")
    
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