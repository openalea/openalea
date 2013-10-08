"""
HOW TO CREATE MINGW EGG
=======================

1. Download mingw-get-setup.exe at https://sourceforge.net/projects/mingw/files/latest/download

2. Install this packages thanks to the GUI:
    a. mingw32-gcc-fortran (bin)
    b. mingw32-gcc-g++ (bin)
    
    c. mingw32-gmp (dev)
    d. mingw32-mpfr (dev)
    e. mingw32-libz (dev)
    
    f. msys-bison (bin)
    g. msys-flex (bin)
    
OR with the CLI:
    a. mingw-get install gcc-fortran
    b. mingw-get install gcc-g++
    c. mingw-get install gmp
    d. mingw-get install mpfr
    e. mingw-get install libz
    f. mingw-get install msys-bison
    g. mingw-get install msys-flex
    
Here, we install Bison-Flex too.
"""

from openalea.release import Formula
from openalea.release.utils import recursive_glob_as_dict, memoize, sh, makedirs, install, safe_rmdir
import os, sys
import glob
from os.path import join as pj
from re import compile as re_compile
from path import path
import subprocess
import time
import warnings

class mingw(Formula):
    download_url = "http://downloads.sourceforge.net/project/mingw/Installer/mingw-get-setup.exe?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fmingw%2F%3Fsource%3Ddirectory&ts=1380884282&use_mirror=freefr"
    download_name = "mingw-get-setup.exe"
    license = "PublicDomain for MingW runtime. GLP or LGPL for some libraries."
    authors = "The Mingw Project"
    description = "Mingw Runtime"
    py_dependent   = False
    arch_dependent = True
    version        = "5.2"
    DOWNLOAD = INSTALL = CONFIGURE = EGGIFY = True
    
    def configure(self):
        """
        Will install mingw with gcc and other dependencies.
        More informations:
        http://www.mingw.org/wiki/InstallationHOWTOforMinGW
        
        :warning: will install much more than needed! And will be really heavy!
        Try to remove what is not necessary.
        For example, when installing gcc, it installs binutils. A big part of binutils is useless.
        """
    
        cmd_prefix = "mingw-get install "
        libs = ["gcc-fortran", "gcc-g++", "gmp", "mpfr", "libz", "msys-bison", "msys-flex", "gcc", "mingw32-make"]
        libs += ["binutils", "mingw-runtime", "pthreads", "iconv", "gcc-core"]
        for lib in libs:
            cmd = cmd_prefix + lib
            sh(cmd)
        
        '''
        # Remove useless packages:
        cmd_prefix = "mingw-get remove "
        libs = ["binutils"]
        for lib in libs:
            cmd = cmd_prefix + lib
            sh(cmd)
            
        # mingw-get install --reinstall g++ 
        # avoid error?
        # gcc: fatal error: -fuse-linker-plugin, but liblto_plugin-0.dll not found
        '''
        
        return True 

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
        from pkg_resources import get_distribution
        location = "c:\\MinGW"
        try:
            result = get_distribution('mingw')
            location = result.location
        except:
            location = "c:\\MinGW"
        
        return path(location)
    
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