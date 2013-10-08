from openalea.release import Formula
from openalea.release.formula.mingw import mingw
from os.path import join as pj, abspath
import os
import glob
from openalea.release.utils import recursive_glob

class bisonflex(Formula):
    dependencies = "mingw"
    EGGIFY = True
    
    def setup(self):
        mingw_path = mingw().get_path()
        bison_path = pj(mingw_path,"msys","1.0")

        bindirs = {"bin": str(pj(bison_path,"bin"))}
        incdirs = {"include": str(pj(bison_path,"include"))}
        libdirs = {"lib": str(pj(bison_path,"lib"))}

        # GET DATA FILES (share directory and subdirs)
        OLDDIR = os.getcwd()
        BISFLEXDIR = abspath(pj(bison_path,"share"))
        BISFLEXDIR = str(BISFLEXDIR).replace("\\", "/")
        os.chdir(BISFLEXDIR)
        raw_files = os.walk(BISFLEXDIR)
        data_files = []
        for i,j,k in raw_files:
            for f in k:
                # we want to reproduce the same hierarchy inside the egg.
                # as inside the BISFLEXDIR.
                rel_direc = os.path.relpath(i,BISFLEXDIR).replace("\\","/")
                file_ = unix_style_join( rel_direc, f)        
                data_files.append( ("share" if rel_direc == "." else pj("share",rel_direc),[abspath(file_)]) )
        os.chdir(OLDDIR)
        
        return dict( 
                    VERSION  = self.version,
                    BIN_DIRS = bindirs,
                    INC_DIRS = incdirs,
                    LIB_DIRS = libdirs,
                    DATA_FILES = data_files
                    )
                    
def unix_style_join(*args):
    l = len(args)
    if l == 1 : return args[0]
    
    ret = args[0]
    for i in range(1,l-1):
        ret += ("/" if args[i]!="" else "")+ args[i]
    
    if args[l-1] != "":
        ret += ("/" if args[l-2]!="" else "") + args[l-1]
        
    return ret