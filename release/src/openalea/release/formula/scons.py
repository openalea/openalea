"""
OLD Way to create SCONS egg:

SCONS=scons-1.2.0.d20100117
wget http://sourceforge.net/projects/scons/files/scons/1.2.0.d20100117/${SCONS}.tar.gz/download
tar xvfz ${SCONS}.tar.gz
cp setup_scons.py ${SCONS}/setup.py
cd ${SCONS}
python setup.py build;
python setup.py bdist_egg

"""

import sys, os
from openalea.release.utils import sh, in_dir, try_except
from openalea.release import Formula
from setuptools import find_packages
from path import path

class scons(Formula):
    license = "MIT license"
    authors = "Steven Knight and The SCons Foundation"
    description = ""    
    version = "2.3.0"      
    #http://downloads.sourceforge.net/project/scons/scons/2.3.0/scons-2.3.0.zip?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fscons%2Ffiles%2F&ts=1381144282&use_mirror=garr
    
    download_url = "http://downloads.sourceforge.net/project/scons/scons/2.3.0/scons-2.3.0.zip"
    download_name  = "scons.zip"
    DOWNLOAD = UNPACK = MAKE = EGGIFY = True   

    _packages = dict()
    _packages_dir = dict()
    _bin_dir = dict()
       
    def make(self):
        ret = sh(sys.executable + " setup.py build") == 0
        os.chdir("engine")
        self._packages=[pkg.replace('.','/') for pkg in find_packages('.')]
        self._package_dir = dict([(pkg, str(path(pkg).abspath())) for pkg in self._packages])
        os.chdir("..")
        self._bin_dir = {'EGG-INFO/scripts': str(path('script').abspath())}
        return ret

    def setup(self):
        print self._package_dir
        print "-----------------"
        print self._packages
        print "================="
        return dict( 
                    PACKAGES = self._packages,
                    PACKAGE_DIRS = self._package_dir,
                    BIN_DIRS = self._bin_dir,
                    ZIP_SAFE = False,
                    setup_requires = ['openalea.deploy'],
                    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
                    ) 