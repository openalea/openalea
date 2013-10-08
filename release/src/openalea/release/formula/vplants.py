from openalea.release import Formula
from openalea.release.utils import sh, checkout

class vplants(Formula):
    version = '1.0'
    homepage = "http://openalea.gforge.inria.fr/dokuwiki/doku.php"
    download_url = "https://scm.gforge.inria.fr/svn/vplants/vplants/branches/release_1_0"
    license = "Cecill-C License"
    authors = "Virtual Plants team (Inria)"
    description = "Set of packages to analyse, model and simulate plant architecture and its development at different scales (tissue, organ, axis and plant)"
    download_name  = "VPlants"
    dependencies = [  "ann-dev",
                    "bison-dev",
                    "boostmath",
                    "boostmath-dev",
                    "boostpython",
                    "boostpython-dev",
                    "cgal",
                    "cgal-dev",
                    "compilers-dev",
                    "flex-dev",
                    "glut",
                    "glut-dev",
                    "gnuplot",
                    "nose-dev",
                    "networkx",
                    "openalea_formula",
                    "pyopengl",
                    "pyqt4",
                    "pyqt4-dev",
                    "qhull",
                    "qhull-dev",
                    "readline",
                    "readline-dev",
                    "rpy2",
                    "scons-dev",
                    "sip4-dev",
                    "svn-dev",
                    ]           
    DOWNLOAD = INSTALL = True
                    
    def _download(self):
        checkout(self.download_url, self.sourcedir)
    def install(self):
        return sh("python multisetup.py install")
        