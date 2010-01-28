#!/usr/bin/env python

from setuptools import setup
import os, os.path, sys, shutil, distutils.util, glob

if distutils.util.get_platform() != "win32":
    print "Do not run this outside MSWindows."
    sys.exit(-1)

#########
# UTILS #
#########
def get_metadata(package):
    mod = __import__(package)
    web = "http://numpy.scipy.org/" if package == "numpy" else "http://www.scipy.org/"
    ret = {"name" : mod.__name__,
           "version" : mod.version.version,
           "author" : "The guys at " + web + " for the hard work, Daniel Barbeau Vasquez for this egg",
           "author_email" : "daniel.barbeau@sophia.inria.fr",
           "license" : "OpenSource (which flavour?)",
           "platforms": ["win32"]
           }
    return ret
    
def get_install_dir(package):
    mod = __import__(package)
    return os.path.dirname(mod.__file__)
    
def get_root_elements(direc):
    dirs = []
    files = []
    elements = os.listdir(direc)
    for el in elements:
        abs_el = os.path.join(direc, el)
        if os.path.isdir(abs_el):
            dirs.append(abs_el)
        else:
            files.append(abs_el)
    return files, dirs
    
def unix_style_join(*args):
    l = len(args)
    if l == 1 : return args[0]
    
    ret = args[0]
    for i in range(1,l-1):
        ret += ("/" if args[i]!="" else "")+ args[i]
    
    if args[l-1] != "":
        ret += ("/" if args[l-2]!="" else "") + args[l-1]
        
    return ret
    
    
#############################################    
# FINDING OUT WICH PACKAGE WE WANT TO BUILD #
#############################################
pkg = None
if "-pkgn" in sys.argv :
    pkg = "numpy"
    sys.argv.remove("-pkgn")
elif "-pkgs" in sys.argv :
    pkg = "scipy"
    sys.argv.remove("-pkgs")
else:
    print """
    Usage: 
    >>> python setup.py [Usual setup.py arguments] (-pkgn|-pkgs)
    
    Additionnal args: -pkgn to package numpy
                      -pkgs to package scipy
    """
    
if pkg is not None:
    ############################################
    # FINDING THE NUMPY/SCIPY INSTALLATION DIR #
    ############################################
    NUMSCI_DIR = get_install_dir(pkg)
    if not os.path.exists(NUMSCI_DIR):
        print "ERROR: could not find", pkg, "directory :", NUMSCI_DIR 
        sys.exit(-1)
    if NUMSCI_DIR == os.getcwd() :
        print "Do not run this script in the directory containing you numpy/scipy installation!" 
        sys.exit(-1)
    NUMSCI_DIR = NUMSCI_DIR.replace("\\", "/") #because distutils expects / instead of \\

    #####################################################################
    # some voodoo to identify the files to copy and where to place them #
    #####################################################################
    raw_files = os.walk(NUMSCI_DIR)
    py_modules = []
    data_files = []

    for i,j,k in raw_files:
        for f in k:
            #we want to reproduce the same hierarchy inside the egg.
            #as inside the NUMSCI_DIR.
            rel_direc = os.path.relpath(i,NUMSCI_DIR).replace("\\","/")
            rel_file = unix_style_join(rel_direc , f)
            ext = os.path.splitext(f)[1]
            if(ext == ".py"):
                #because we must represent them as modules we remove the ".py" extension
                #we replace the "./" paths by ""  and replace slashes by dots.
                py_modules.append( pkg+"."+rel_file[:-3].replace("./","").replace("/",".") ) 
            elif(ext in [".txt", ".pyd", "" , ".example"]):
                data_files.append( (pkg if rel_direc == "." else unix_style_join(pkg, rel_direc),
                                    [unix_style_join(pkg, rel_file)]) 
                                  )
            else:
                continue
            
    ###########################
    # DON'T LOOK, THIS IS UGLY #
    ###########################
    #we copy the full numpy/scipy tree locally because
    #distutils works locally
    HERE = os.getcwd()
    shutil.copytree(NUMSCI_DIR, unix_style_join(HERE, pkg))

    #############
    # Let's go! #
    #############
    metadata = get_metadata(pkg)
    metadata["py_modules"]=py_modules
    metadata["data_files"]=data_files
    metadata["zip_safe"]=False
    setup(**metadata)

    #we remove the copy of the tree so that you don't notice the uglyness.
    shutil.rmtree(unix_style_join(HERE, pkg))

    #we rename the egg to have the platform included.
    egg = glob.glob("dist/*.egg")[0]
    os.rename(egg, egg[:-4]+"-win32.egg")
        
else: setup()
      