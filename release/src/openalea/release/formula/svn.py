from openalea.release import Formula

class svn(Formula):
    license = ""
    authors = ""
    description = ""  
    py_dependent   = True
    arch_dependent = True 
    version = "1.8.0-1"       
    download_url = "http://sourceforge.net/projects/win32svn/files/1.8.0/apache22/Setup-Subversion-1.8.0-1.msi"
    homepage = "http://subversion.apache.org/"
    download_name  = "svn.msi"
    
    DOWNLOAD = INSTALL = True 