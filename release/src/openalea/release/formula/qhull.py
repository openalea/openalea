from openalea.release import Formula
from os.path import join as pj

class qhull(Formula):
    version = "2012.1"
    download_url = "http://www.qhull.org/download/qhull-2012.1.zip"
    download_name  = "qhull.zip"
    DOWNLOAD = UNPACK = EGGIFY = True
    
    def setup(self):
        return dict(
                    LIB_DIRS         = {'lib' : pj(self.sourcedir,'build') },
                    INC_DIRS         = {'include' : pj(self.sourcedir,'eg') },
                    BIN_DIRS         = {'bin' : pj(self.sourcedir,'bin') },
                    )