from openalea.release import Formula
from openalea.release.utils import sh, ascii_file_replace, recursive_glob_as_dict, merge_list_dict, Pattern
from openalea.release.formula.mingw_rt import mingw_rt
from os.path import join as pj, exists
import os, sys
from re import compile as re_compile
import re

class boost(Formula):
    download_url = "http://switch.dl.sourceforge.net/project/boost/boost/1.48.0/boost_1_48_0.zip"
    download_name  = "boost_src.zip"
    archive_subdir = "boost*"
    license = "Boost Software License 1.0"
    authors = "Boost contributors"
    description = "Windows gcc libs and includes of Boost"
    homepage = "http://www.boost.org/"
    py_dependent   = True
    arch_dependent = True    
    def configure(self):
        return True #bjam configures, builds and installs so nothing to do here
    def make(self):
        # it is possible to bootstrap boost if no bjam.exe is found:
        if not exists( pj(self.sourcedir, "bjam.exe") ):
            print "Call bootstrap.bat"
            if sh("bootstrap.bat mingw") != 0:
                return False
            else:
                # The Bootstrapper top-level script ignores that gcc
                # was used and by default says it's msvc, even though
                # the lower level scripts used gcc.
                ascii_file_replace( "project-config.jam",
                                    "using msvc",
                                    "using gcc")
        # try to fix a bug in python discovery which prevents
        # bjam from finding python on Windows NT and old versions.
        pyjam_pth = pj("tools","build","v2","tools","python.jam")
        ascii_file_replace(pyjam_pth,
                           "[ version.check-jam-version 3 1 17 ] || ( [ os.name ] != NT )",
                           "[ version.check-jam-version 3 1 17 ] && ( [ os.name ] != NT )")
        paths = self.installdir, pj(sys.prefix, "include"), pj(sys.prefix,"libs")
        cmd = "bjam --debug-configuration --prefix=%s --without-test --layout=system"
        cmd += " variant=release link=shared threading=multi runtime-link=shared toolset=gcc"
        cmd += " include=%s library-path=%s install"
        cmd %= paths
        print cmd
        return sh(cmd) == 0
    def install(self):
        """ bjam configures, builds and installs so nothing to do here"""
        return True
    def setup(self):
        version_re  = re_compile("^.*BOOST_VERSION\s:\s([\d\.]{4,8}).*$", re.MULTILINE|re.DOTALL)
        incs = recursive_glob_as_dict( self.install_inc_dir, Pattern.qtinc, strip_keys=True, prefix_key="include", dirs=True).items()
        inc_dirs = merge_list_dict( incs )
        # get the version from Jamroot file
        version = "UNKNOWN"        
        with open( pj(self.sourcedir, "Jamroot") ) as f:
            txt = f.read()
            se = version_re.search(txt)
            if se:
                version = se.groups()[0]
        lib_dirs    = {"lib": self.install_lib_dir}
        return dict( 
                    VERSION          = version,                 
                    LIB_DIRS         = lib_dirs,
                    INC_DIRS         = inc_dirs,
                    BIN_DIRS         = None,                
                    INSTALL_REQUIRES = [mingw_rt.egg_name()]
                    )  