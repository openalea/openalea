import os
import time
import string
from openalea.core.path import path

class S2v(object):
    """  Produce volumetric statistics from CanFile  """ 
    cpt = 0

    def __init__(self):
        self.outDir="S2vOutDir%i"%(S2v.cpt)
        S2v.cpt += 1


    def __call__(self, scene_file, pattern_file,layer_nz,layer_Dz,optical_file):

        log = "\nS2v :Last call => " + time.asctime() + "\n"

        if layer_nz is None or layer_Dz is None:
            log += " No layer described => no file generated\n"
            return None, log

        curdir= path('.').abspath()
        d=curdir/self.outDir
        if not d.exists():
            d.mkdir(mode=755)
        os.chdir(d)

        
        effargs = ['"%s"'%scene_file, str(layer_nz), str(layer_Dz), '"%s"'%pattern_file]
        # delete the .opt
        optical_name = optical_file[0:-4]
        effargs.append(optical_name)
        cmd = "s2v10 " + ' '.join(effargs)
        print cmd    
        fin, fout = os.popen2(cmd)
        log +=  cmd + "\n" +''.join(fout.readlines())
        fin.close(); fout.close()

        os.chdir(curdir)
        
        return (path(self.outDir).abspath(),log)
