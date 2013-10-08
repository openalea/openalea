from openalea.release import Formula

class matplotlib(Formula):
    license = "Python Software Foundation License Derivative - BSD Compatible."
    authors = "Matplotlib developers"
    version = "1.3.0"
    download_url = "https://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-"+version+"/matplotlib-1.3.0.win32-py2.7.exe"
    download_name  = "matplotlib.exe"
    description = "Matplotlib packaged as an egg"  
    py_dependent   = True
    arch_dependent = True   
    DOWNLOAD = COPY_INSTALLER = True
    # Here we can download, install and eggify the package for install it after like an egg
    # with DOWNLOAD = INSTALL = EGGIFY = True
    
    # But we can use DOWNLOAD = COPY_INSTALLER = True
    # So, we download the installer and copy it.
    
    def setup(self):        
        return dict( VERSION = self.package.__version__ )   