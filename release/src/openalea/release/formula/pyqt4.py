from openalea.release import Formula
from openalea.release.utils import option_to_python_path, option_to_sys_path, \
sh, pj
from openalea.release.formula.qt4 import qt4
import sys

class pyqt4(Formula):
    download_url = "http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.10.2/PyQt-win-gpl-4.10.2.zip"
    '''
    download_url = "http://pypi.python.jp/PyQt/PyQt-win-gpl-4.8.6.zip#md5=734bb1b8e6016866f4450211fc4770d9"
    url = "http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-win-gpl-4.9.1.zip"
    '''
    download_name  = "pyqt4_src.zip"
    
    cmd_options = [ ("siphome", None, "Path to sip.exe"),
                    ("sipsite", None, "Path(s) to sip modules (';' seperated)") ]

    def __init__(self, *args, **kwargs):
        super(pyqt4, self).__init__(*args, **kwargs)
        # we install pyqt4 binaries in the qt bin installation directory to easily recover it
        # for the egg. The eggs are built in the historical layout used by openalea packagers.
        # This doesn't mean it's good. It doesn't mean it's bad though it does look a bit messy.
        qt4_ = qt4()
        self.install_bin_dir  = qt4_.install_bin_dir
        self.install_site_dir = pj(self.installdir,"site")
        self.install_sip_dir  = pj(self.installdir,"sip")
        self.inst_paths       = self.install_bin_dir, self.install_site_dir, self.install_sip_dir

    @option_to_python_path("sipsite")
    @option_to_sys_path("siphome")
    def configure(self):
        return sh(sys.executable + \
                      " -S configure.py --confirm-license -w -b %s -d %s -v %s"%self.inst_paths) == 0
        
    def make(self):
        return True
        
    def install(self):
        return True
        
    def extra_paths(self):
        return self.install_bin_dir

    def extra_python_paths(self):
        return self.install_site_dir

    def patch(self):
        return True
        
        '''
        header = """
import sipconfig
from sipconfig import pj as pj
from sipconfig import qtdev as qtdev
from sipconfig import qt as qt"""

        txt = ""
        with open("pyqtconfig.py") as f:
            txt = f.read()

        txt = txt.replace("import sipconfig", header)
        txt = re.sub(r"(\s*'pyqt_bin_dir':\s*)'[A-Z]:(\\\\|/).*'", r"\1pj(qtdev,'bin')", txt)
        txt = re.sub(r"(\s*'pyqt_mod_dir':\s*)'[A-Z]:(\\\\|/).*'", r"\1pj(qt,'PyQt4')", txt)
        txt = re.sub(r"(\s*'pyqt_sip_dir':\s*)'[A-Z]:(\\\\|/).*'", r"\1pj(qtdev,'sip')", txt)
        txt = re.sub(r"(\s*'qt_data_dir':\s*)'[A-Z]:(\\\\|/).*'",  r"\1qtdev.replace('\\','/')", txt)
        txt = re.sub(r"(\s*'qt_dir':\s*)'[A-Z]:(\\\\|/).*'",       r"\1qt", txt)
        txt = re.sub(r"(\s*'qt_inc_dir':\s*)'[A-Z]:(\\\\|/).*'",   r"\1pj(qtdev, 'include')", txt)
        txt = re.sub(r"(\s*'qt_lib_dir':\s*)'[A-Z]:(\\\\|/).*'",   r"\1pj(qtdev, 'lib')", txt)

        txt = re.sub(r"(\s*'INCDIR_QT':\s*)'[A-Z]:(\\\\|/).*'",    r"\1pj(qtdev, 'include')", txt)
        txt = re.sub(r"(\s*'LIBDIR_QT':\s*)'[A-Z]:(\\\\|/).*'",    r"\1pj(qtdev, 'lib')", txt)
        txt = re.sub(r"(\s*'MOC':\s*)'[A-Z]:(\\\\|/).*'",          r"\1pj(qtdev, 'bin', 'moc.exe')", txt)

        shutil.copyfile( "pyqtconfig.py", "pyqtconfig.py.old" )
        with open("pyqtconfig.py", "w") as f:
            f.write(txt)
        prefix = sys.prefix'''