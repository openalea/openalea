from openalea.release import Formula

class setuptools_formula(Formula):
    license = ""
    authors = "Python Software Foundation"
    description = "Download, build, install, upgrade, and uninstall Python packages -- easily!"  
    py_dependent   = True
    arch_dependent = True 
    version = "0.6c11"       
    download_url = "http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe"
    download_name  = "setuptools.exe"
    
    DOWNLOAD = INSTALL = True      