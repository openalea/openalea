# -*- python -*-
#
#       openalea.deploy.qtpatch
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

"""This module converts hard coded compilation paths inside Qt binairies into
relative paths suitable for use inside eggs."""

__license__ = "Cecill-C"
__revision__ = " $Id$"

import sys
import os, os.path
import fnmatch
import shutil

def patch(files, qtDirPath, where):
    if not os.path.isdir(qtDirPath):
        print qtDirPath, "does not exist"
        sys.exit(-1)
    
    if os.path.exists( files ):
        with open(files, "r") as fn:
            filesToPatch = fn.read().split()            
    else:
        filesToPatch = []
        patterns = files.split(",")
        for dir_path, sub_dirs, subfiles in os.walk(where):
            for pat in patterns:
                for fn in fnmatch.filter(subfiles, pat):
                    filesToPatch.append( os.path.join(dir_path, fn) )
  
    # Make all paths relative to the patched file.
    # PortableExecutables have file size encoded in header.
    # Instead of modifying the header we replace by a string 
    # of exactly the same size using padding "/".
    replacement = bytearray(".." + "/"*(len(qtDirPath)-2))
    qtDirPathA  = bytearray(qtDirPath)
    qtDirPathA2 = bytearray(qtDirPath.replace("\\", "/"))
    patches     = 0 # a counter 
    
    print "about to try to patch", len(filesToPatch), "files"
    for f in filesToPatch:
        prefix = u"" + qtDirPath
        f = os.path.join(prefix,f)
        
        print "patch file", f,
        if not os.path.exists(f):
            print "qpatch: warning: file not found", f
            continue
              
        source = None
        stat   = None
        with open(f, "rb") as file_:
            source = bytearray(file_.read())
            # store permissions
            stat = os.fstat(file_.fileno())
            
        if source.find(qtDirPathA) == -1 and source.find(qtDirPathA2) == -1:
            print "string not found"
            continue
  
        # make backup, if backup already exists, skip the patching.
        if not os.path.exists( f+"_bkp" ):
            shutil.move(f, f+"_bkp")
        else:
            print "backup already exists, ignoring"
            continue
  
        patched = source.replace(qtDirPathA, replacement)
        patched = patched.replace(qtDirPathA2, replacement)
               
        with open( f, "wb") as out_:
            out_.write(patched)
        
            # restore permissions
            try:
                os.fchmod(out_.fileno(), stat.st_mode)
                os.fchown(out_.fileno(), stat.st_uid, stat.st_gid)
            except Exception, e:
                print "\n\tOops! Couldn't copy file metadata", type(e), e
        
        patches += 1
        print "ok"
            
    print "patched", patches, "files"
    
if __name__ == "__main__":
    try:
        files, qtDirPath, where = sys.argv[1:]
        patch(files, qtDirPath, where)
    except:
        import traceback
        traceback.print_exc()
        print "Usage: python patch files oldQtDir where"
        sys.exit(-1)    
    