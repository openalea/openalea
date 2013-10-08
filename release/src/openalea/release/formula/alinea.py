from openalea.release import Formula
from openalea.release.utils import sh, checkout

class alinea(Formula):
    version = '1.0'
    homepage = "http://openalea.gforge.inria.fr/dokuwiki/doku.php"
    download_url = "https://scm.gforge.inria.fr/svn/openaleapkg/branches/release_1_0"
    license = "Cecill-C License"
    authors = "INRA teams and Virtual Plants team (Inria)"
    description = "Set of packages to simulate ecophysiological and agronomical processes (crop 3D development, light distribution, interactions with diseases…)"
    download_name  = "Alinea"
    dependencies = ["vplants", "openalea_formula"]
    DOWNLOAD = INSTALL = True
    
    def _download(self):
        checkout(self.download_url, self.sourcedir)
    def install(self):
        return sh("python multisetup.py install")