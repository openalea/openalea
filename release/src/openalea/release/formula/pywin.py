from openalea.release import Formula

class pywin(Formula):
    license = "Python Software Foundation License"
    authors = "Mark Hammond"
    description = "Python for Windows Extensions"  
    py_dependent   = True
    arch_dependent = True 
    version = "218"       
    download_url = "http://freefr.dl.sourceforge.net/project/pywin32/pywin32/Build%20218/pywin32-218.win32-py2.7.exe"
    homepage = "http://pywin32.sourceforge.net/"
    download_name  = "pywin.exe"
    DOWNLOAD = INSTALL = True   