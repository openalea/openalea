#!/usr/bin/env python

from setuptools import setup
import os, os.path, sys, shutil, distutils.util, glob

if distutils.util.get_platform() != "win32":
    print "Do not run this outside MSWindows."
    sys.exit(-1)

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
    
if pkg is not None:
    ############################################
    # FINDING THE NUMPY/SCIPY INSTALLATION DIR #
    ############################################
    NUMSCI_DIR = get_install_dir(pkg)

    if not os.path.exists(NUMSCI_DIR):
        print "ERROR: could not find", pkg, "directory :", NUMSCI_DIR 
        sys.exit(-1)
        
    all_copyable_files = get_root_elements(NUMSCI_DIR)
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
            rel = os.path.relpath(i,NUMSCI_DIR).replace("\\","/")
            abs_file = unix_style_join(i.replace("\\","/"), f)
            rel_file = unix_style_join(rel , f)
            ext = os.path.splitext(f)[1]
            if(ext == ".py"):
                py_modules.append( rel_file[:-3].replace("./","").replace("/",".") ) #because we must represent them as modules
            elif(ext == ".txt" or ext == ".pyd" or ext == "" or ext == ".example"):
                data_files.append( ("" if rel == "." else rel,[rel_file]) )
            else:
                continue
            
    ###########################
    # DON'T LOOK, THIS IS UGLY #
    ###########################
    HERE = os.getcwd()
    for file in all_copyable_files[0] : 
        shutil.copy2(file, HERE)
    for dir in all_copyable_files[1] : 
        shutil.copytree(dir, unix_style_join(HERE, os.path.relpath(dir,NUMSCI_DIR)))


    #############
    # Let's go! #
    #############
    metadata = get_metadata(pkg)
    metadata["py_modules"]=py_modules
    metadata["data_files"]=data_files
    metadata["zip_safe"]=False
    setup(**metadata)

    for file in all_copyable_files[0] : 
        os.remove(unix_style_join(HERE, os.path.relpath(file,NUMSCI_DIR)))
    for dir in all_copyable_files[1] : 
        shutil.rmtree(unix_style_join(HERE, os.path.relpath(dir,NUMSCI_DIR)))

    egg = glob.glob("dist/*.egg")[0]
    os.rename(egg, egg[:-4]+"-win32.egg")
        
else: setup()
      