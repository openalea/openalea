from openalea.release import Formula
from os.path import join as pj

class gnuplot(Formula):
    download_url = "http://heanet.dl.sourceforge.net/project/gnuplot/gnuplot/4.4.4/gp444win32.zip"
    download_name  = "gnuplot_src.zip"

    def configure(self):
        return True
    def make(self):
        return True
    def install(self):
        return True 
    def setup(self):
        print "=========================================================="
        print "Check in Formula\gnuplot.py if the setup is the good one"
        print "And test the egg"
        print "=========================================================="
        return dict(
                    LIB_DIRS         = None,
                    INC_DIRS         = None,
                    BIN_DIRS         = {'bin' : pj(self.sourcedir,'binary') },
                    )