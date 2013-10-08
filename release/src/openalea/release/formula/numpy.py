from openalea.release import Formula

class numpy(Formula):
    license = "Numpy License"
    authors = "(c) Numpy Developers"
    description = "Numpy packaged as an egg"    
    version = "1.7.1"    
    py_dependent   = True
    arch_dependent = True      
    download_url = "http://freefr.dl.sourceforge.net/project/numpy/NumPy/1.7.1/numpy-1.7.1-win32-superpack-python2.7.exe"
    download_name  = "numpy.exe"
    DOWNLOAD = COPY_INSTALLER = True
    # Here we can download, install and eggify the package for install it after like an egg
    # with DOWNLOAD = INSTALL = EGGIFY = True
    
    # But we can use DOWNLOAD = COPY_INSTALLER = True
    # So, we download the installer and copy it.
    
    def setup(self):
        return dict( VERSION = self.package.version.full_version, )