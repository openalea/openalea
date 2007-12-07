import os
import time
import string
from openalea.core.path import path

class MCSail(object):
    """  Compute mean fluxes on layered canopy  """ 
    cpt = 0

    def __init__(self):
        self.out="MCSail%i.env"%(MCSail.cpt)
        MCSail.cpt += 1


    def __call__(self, s2v_dir, light_file):

        log = "\nMCSail :Last call => " + time.asctime() + "\n"

        if s2v_dir is None:
            log += " No diffusion => no file generated\n"
            return None, log

        curdir= path('.').abspath()
        d=path(s2v_dir).abspath()
        d=eval('r"%s"'%d)
        os.chdir(d)

        effargs = ['"%s"'%light_file]
        cmd = "mcsail19 " + ' '.join(effargs)
        print cmd    
        fin, fout = os.popen2(cmd)
        log +=  cmd + "\n" +''.join(fout.readlines())
        fin.close(); fout.close()

        os.chdir(curdir)
        
        return (path(self.out).abspath(),log)
