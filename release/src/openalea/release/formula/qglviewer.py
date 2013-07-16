from openalea.release import Formula
from openalea.release.utils import recursive_copy, pj, sh, Pattern

class qglviewer(Formula):
    download_url = "https://gforge.inria.fr/frs/download.php/28138/libQGLViewer-2.3.9-py.tgz"
    download_name  = "qglviewer_src.tgz"

    def __init__(self, *args, **kwargs):
        super(qglviewer, self).__init__(*args, **kwargs)
        self.install_inc_dir = pj(self.installdir, "include", "QGLViewer")
        self.install_dll_dir = pj(self.installdir, "dll")
        self.install_lib_dir = pj(self.installdir, "lib")

    def configure(self):
        return sh("qmake QGLViewer*.pro") == 0

    def make(self):
        # by default, and since we do not use self.options yet, we build in release mode
        return sh("mingw32-make release") == 0

    def install(self):
        # The install procedure will install qscintilla in qt's directories
        recursive_copy( self.sourcedir               , self.install_inc_dir, Pattern.include)
        recursive_copy( pj(self.sourcedir, "release"), self.install_lib_dir, Pattern.qtstalib)
        recursive_copy( pj(self.sourcedir, "release"), self.install_dll_dir, Pattern.dynlib)
        return True

    def extra_paths(self):
        return self.install_dll_dir