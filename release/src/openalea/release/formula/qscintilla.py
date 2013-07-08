from openalea.release import Formula
from openalea.release.utils import sh, pj
from openalea.release.formula.qt4 import qt4
import shutil

class qscintilla(Formula):
    download_url = "http://www.riverbankcomputing.co.uk/static/Downloads/QScintilla2/QScintilla-gpl-2.6.1.zip"
    download_name  = "qscintilla_src.zip"
    archive_subdir = "QScint*/Qt4"

    def configure(self):
        # The install procedure will install qscintilla in qt's installation directories
        qt4_ = qt4()
        paths = qt4_.install_inc_dir, qt4_.install_tra_dir, qt4_.installdir, qt4_.install_dll_dir,
        return sh( ("qmake -after header.path=%s trans.path=%s qsci.path=%s " + \
                                 "target.path=%s -spec win32-g++ qscintilla.pro")%paths) == 0
    
    def install(self):
        ret = super(qscintilla, self).install()
        qt4_ = qt4()
        try:
            shutil.move( pj(qt4_.install_dll_dir, "libqscintilla2.a"), qt4_.install_lib_dir)
        except Exception, e :
            print e
        return ret