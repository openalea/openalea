__license__ = "Cecill-C"
__revision__ = " $Id$ "

import os
import time
import string
from openalea.core.path import path

def dQuote(fn):
    return '"%s"'%fn

class Canestra(object):
    """  Nested radiosity illumination of a 3D Scene """ 
    cpt = 0

    def __init__(self):
        self.outDir="CanestraOutDir%i"%(Canestra.cpt)
        Canestra.cpt += 1


    def __call__(self,
                 scene_file,
                 pattern_file,
                 light_sailFile,
                 light_sourceFile,
                 optical_file,
                 scene_addSoilOpt,
                 sensor_file,
                 FFmatrix_OutFile,
                 FFmatrix_InFile,
                 FFmatrix_InDir,
                 FFmatrix_printOpt,
                 output_genCanOpt,
                 output_genEtriOpt,
                 option_sphereRadius,
                 option_sphereDiameter,
                 option_discResolution,
                 option_nbSim,
                 option_CGnbiter,
                 option_CGthreshold,
                 option_lightScreenResolution,
                 option_testInnerTriangle,
                 option_verboseLevel,
                 option_estimateMemory,
                 option_printHelp):

        log = "\nCanestra :Last call => " + time.asctime() + "\n"

       
            
        effargs=[]

        if scene_file is not None:
            effargs+=["-M", dQuote(scene_file)]
        if scene_addSoilOpt is not None:
            effargs+=["-s",str(scene_addSoilOpt)]
            
        if pattern_file is not None:
            effargs+=["-8", dQuote(pattern_file)]

        if optical_file is not None:
            effargs+=["-p", dQuote(optical_file)]

        if sensor_file is not None:
            effargs+=["-C", dQuote(sensor_file)]

        if light_sourceFile is not None:
            effargs+=["-l", dQuote(light_sourceFile)]
            
        if light_sailFile is None:
            #no diffuse
            log += " No Far contribution in input=> simple projection mode\n"
            effargs+=["-1"]
        else:
            #set the diffuse options
            effargs+=["-e", dQuote(light_sailFile)]
            if FFmatrix_OutFile is not None:
                effargs+=["-f", dQuote(FFmatrix_OutFile)]
            if FFmatrix_InFile is not None:
                effargs+=["-w", dQuote(FFmatrix_InFile)]
            if FFmatrix_InDir is not None:
                effargs+=["-t", dQuote(FFmatrix_InDir)]
            if FFmatrix_printOpt:
                effargs+=["-F"]
            if option_sphereRadius is not None:
                effargs+=["-r",str(option_sphereRadius)]
            if option_sphereDiameter is not None and option_sphereRadius is None:
                effargs+=["-d",str(option_spherediameter)]

        #other options
        if output_genCanOpt:
            effargs+=["-g"]
        if output_genEtriOpt:
            effargs+=["-A"]
        if option_discResolution is not None:
                effargs+=["-R",str(option_discResolution)]
        if option_nbSim is not None:
                effargs+=["-S",str(option_nbSim)]
        if option_CGthreshold is not None:
                effargs+=["-a",str(option_CGthreshold)]
        if option_CGnbiter is not None:
                effargs+=["-i",str(option_CGnbiter)]
        if option_lightScreenResolution is not None:
                effargs+=["-L",str(option_lightScreenResolution)]
        if option_testInnerTriangle:
            effargs+=["-B"]
        if option_estimateMemory:
            effargs+=["-T"]
        if option_verboseLevel is not None:
                effargs+=["-v",str(option_verboseLevel)]
        if option_printHelp:
            effargs+=["-h"]
        

        curdir= path('.').abspath()
        d=curdir/self.outDir
        if not d.exists():
            d.mkdir(mode=755)
        os.chdir(d)

        cmd = "canestrad "
        for opt in effargs:
            cmd += opt + " "
        
        
        print cmd    
        fin, fout = os.popen2(cmd)
        log +=  cmd + "\n" +''.join(fout.readlines())
        fin.close(); fout.close()

        os.chdir(curdir)
        candir=path(self.outDir).abspath()
        return (path(self.outDir).abspath(),candir/"scene.can",candir/"Eabs.vec",log)
