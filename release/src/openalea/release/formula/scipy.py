from openalea.release import Formula

class scipy(Formula):
    license = "Scipy License"
    authors = "(c) Enthought"
    description = "Scipy packaged as an egg"  
    py_dependent   = True
    arch_dependent = True 
    version = "0.12.0"       
    download_url = "http://freefr.dl.sourceforge.net/project/scipy/scipy/0.12.0/scipy-0.12.0-win32-superpack-python2.7.exe"
    download_name  = "scipy.exe"
    DOWNLOAD = COPY_INSTALLER = True
    # Here we can download, install and eggify the package for install it after like an egg
    # with DOWNLOAD = INSTALL = EGGIFY = True
    
    # But we can use DOWNLOAD = COPY_INSTALLER = True
    # So, we download the installer and copy it.
    
    def setup(self):
        return dict( VERSION = self.package.version.full_version )
      