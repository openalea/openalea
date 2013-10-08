from openalea.release import Formula
from os.path import join as pj

class gnuplot(Formula):
    version = "4.6.3"
    download_url = "http://downloads.sourceforge.net/project/gnuplot/gnuplot/4.6.3/gp463-win32-setup.exe"
    download_name = "gnuplot.exe"
    DOWNLOAD = COPY_INSTALLER = True 