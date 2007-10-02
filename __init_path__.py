# This file allow to use openalea packages without installing them.

def set_path():
    import os
    from distutils.sysconfig import get_python_lib
    import openalea

    openalea_dir = os.path.join(get_python_lib(),'openalea')

    pkg_dirs = [ "core/src",
                 "visualea/src",
                 "catalog/src",
                 "distx",
                 "sconsx/src",
                 "plotools/src",
                 "scipywrap/src",
                 "rpywrap/src",
                 openalea_dir
                 ]

 
    for subdir in  pkg_dirs:
        for p in openalea.__path__:
        
            newpath = os.path.abspath(os.path.join(p, os.path.normpath(subdir)))
            if(os.path.isdir(newpath)):
                openalea.__path__.append(newpath)
                break


    try:
        import vplants
        openalea.__path__ += vplants.__path__
    except:
        pass



    del get_python_lib
    del openalea_dir
