from openalea.release import Formula
from os.path import join as pj

class qhull(Formula):
    download_url = "http://www.qhull.org/download/qhull-2011.2.zip"
    download_name  = "qhull_src.zip"
    archive_subdir = "qhull-2011.2"
    enabled = False
    def configure(self):
        return True
    def make(self):
        return True
    def install(self):
        return True 
    # def bdist_egg(self):
        # print "Can't bdist_egg! Please implement it in Formula\qhull.py"
        # return False
    def setup(self):
        print "=========================================================="
        print "Check in Formula\qhull.py if the setup is the good one"
        print "And test the egg"
        print "=========================================================="
        return dict(
                    LIB_DIRS         = {'lib' : pj(self.sourcedir,'build') },
                    INC_DIRS         = {'include' : pj(self.sourcedir,'eg') },
                    BIN_DIRS         = {'bin' : pj(self.sourcedir,'bin') },
                    )