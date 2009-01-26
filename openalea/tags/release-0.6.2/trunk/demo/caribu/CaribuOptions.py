import os
import time
import string
from openalea.core.path import path

def dQuote(fn):
    return '"%s"'%fn

class CaribuOptions(object):
    """  Front end for caribu dataflow options""" 
    cpt = 0
    
    def __init__(self):
        self.outDir="CaribuOutDir%i"%(CaribuOptions.cpt)
        CaribuOptions.cpt += 1


    def __call__(self,
                 option_simulateInfinity,
                 optval_patternFileName,
                 option_addSoil,
                 optval_maxSoilTri,
                 option_noMultipleScattering,
                 optval_nz,
                 optval_Dz,
                 optval_radius,
                 option_reUseFF,
                 option_savelog,
                 optval_logFileName,
                 option_cleanUp):

        curdir= path('.').abspath()
        d=curdir/self.outDir
        if not d.exists():
            d.mkdir(mode=755)
        os.chdir(d)

        
        if option_simulateInfinity:
            if optval_patternFileName is None:
                raise "=> PyCaribu : need a pattern to simulate infinity"
        else:
            optval_patternFileName=None
            
        if option_noMultipleScattering:
            optval_nz=None
            optval_Dz=None
            optval_radius=None
        else:
            #on veut le diffus
            if optval_nz is None or optval_Dz is None or optval_radius is None:
                raise "=> PyCaribu : need nz,Dz and radius to simulate reflexions"
        FFmatrix_InFile=None
        FFmatrix_OutFile=None

        if option_reUseFF:
            if os.exists("Caribu.FF"):
                FFmatrix_InFile=os.abspath("Caribu.FF")
            else:
                FFmatrix_OutFile=d/"Caribu.FF"
        
        os.chdir(curdir)
        
        return(optval_patternFileName,
               optval_nz,
               optval_Dz,
               optval_maxSoilTri,
               FFmatrix_OutFile,
               FFmatrix_InFile,
               optval_radius)
