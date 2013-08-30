from openalea.release import Formula
from openalea.release.utils import sh, apply_patch, checkout
from os.path import join as pj, abspath, dirname


## Name is openalea_formula and not openalea to avoid namespace conflict!
class openalea_formula(Formula):
    version = '1.0'
    homepage = "http://openalea.gforge.inria.fr/dokuwiki/doku.php"
    download_url = "https://scm.gforge.inria.fr/svn/openalea/branches/release_1_0"
    license = "Cecill-C License"
    authors = "Inria, INRA, CIRAD"
    description = "OpenAlea is an open source project primarily aimed at the plant research community."
    download_name  = "OpenAlea"
    dependencies = ["mingw", "mingw_rt", "pyqt4", "numpy", "scipy", "matplotlib", 
                  "pyqscintilla", "setuptools", "pillow", "pylsm", "pylibtiff", "pywin32"]
                  ## And what about "soappy" ???
                  ## pywin32 only WINDOWS
                  ## old: "pyqt4", "numpy", "scipy", "matplotlib", 
                  ## "pyqscintilla", "setuptools", "pillow", "pylsm", "pylibtiff","soappy" , "pywin32"
    
    def _download(self):
        checkout(self.download_url, self.sourcedir)
    def setup(self):
        return dict()
    def configure(self):
        return True
    def make(self):
        return True
    def install(self):
        return sh("python multisetup.py install")