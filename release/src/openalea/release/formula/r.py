from openalea.release import Formula

class r(Formula):
    license = "GNU General Public License"
    authors = "(c) 1998-2013 by Kurt Hornik"
    description = "The R Project for Statistical Computing"  
    py_dependent   = True
    arch_dependent = True 
    version = "2.15.3"       
    download_url = "http://mirror.ibcp.fr/pub/CRAN/bin/windows/base/old/2.15.3/R-2.15.3-win.exe"
    homepage = "http://www.r-project.org/"
    download_name  = "r.exe"
    
    DOWNLOAD = INSTALL = True        

    def extra_paths(self):
        # TODO :  add R's home to the path
        
        # return pj("C:/Program Files/R","")
        return None 