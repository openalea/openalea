from openalea.release import Formula
from openalea.release.utils import sh, pj
import glob

class bisonflex(Formula):
    download_url = "https://gforge.inria.fr/frs/download.php/27628/bisonflex-2.4.1_2.5.35-win32.egg"
    download_name  = "bisonflex.egg"
    def _unpack(self):
        return True
    def _configure(self):
        return True
    def _make(self):
        return True
    def _install(self):
        egg = glob.glob( pj(self._get_dl_path(), "bisonflex*.egg") )[0]
        cmd = "alea_install -H None -f . %s" %egg
        return sh(cmd)
    def _bdist_egg(self):
        return True
