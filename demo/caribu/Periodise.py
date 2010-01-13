__license__ = "Cecill-C"
__revision__ = " $Id$ "

import os
import time
import string

from openalea.core.path import path

def dQuote(fn):
    return '"%s"'%fn

class Periodise(object):
    """  Retail a scene along a pattern for use as a periodic motif  """ 
    cpt = 0


    def __init__(self):
        self.outfile="PeriodiseOut%i.can"%(Periodise.cpt)
        Periodise.cpt += 1


    def __call__(self, scene_file, pattern_file):

        log = "\nPeriodise :Last call => " + time.asctime() + "\n"

        if pattern_file is None:
            log += " No pattern file => pass can file unchanged\n"
            return scene_file, log
        
        effargs = ["-m", dQuote(scene_file), "-8", dQuote(pattern_file),"-o", self.outfile]
        cmd = "periodise "
        for opt in effargs:
            cmd += opt + " "
        print cmd    
        fin, fout = os.popen2(cmd)
        log +=  cmd + "\n" +''.join(fout.readlines())
        fin.close(); fout.close()
        
        return (path(self.outfile).abspath(),log)
