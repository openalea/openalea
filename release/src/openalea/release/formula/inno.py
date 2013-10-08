from openalea.release import Formula

class inno(Formula):
    license = "Free of charge but not public domain : http://www.jrsoftware.org/files/is/license.txt"
    authors = "(C) 1997-2013 Jordan Russell"
    description = "Inno Setup is a free installer for Windows programs"  
    py_dependent   = True
    arch_dependent = True 
    version = "5.5.3"       
    download_url = "http://mlaan2.home.xs4all.nl/ispack/isetup-5.5.3.exe"
    homepage = "http://www.jrsoftware.org/"
    download_name  = "innosetup.exe"
    DOWNLOAD = INSTALL = True 