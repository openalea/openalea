# This file allow to use openalea packages without installing them.

def set_path():
    import os, sys
    from os.path import join
    import pkg_resources
    openalea = sys.modules['openalea']


    dir = os.path.dirname(__file__)

    pkg_resources._handle_ns('openalea.core', join('trunk/core/src'))
    

    pkg_dirs = { 'openalea.core': "trunk/core/src",
                 'openalea.visualea':"trunk/visualea/src",
                 'openalea.catalog' : "trunk/catalog/src",
                 'openalea.sconsx' : "trunk/sconsx/src",
                 'openalea.plotools' : "trunk/plotools/src",
                 'openalea.stand' : "trunk/stand/src",
                 'openalea.image' : "trunk/image/src",
                 'openalea.stat' : "trunk/stat/src",
                 }

 
    for name, subdir in  pkg_dirs.items():

        pkg_resources._handle_ns(name, join(dir, subdir))

    try:
        import vplants
        openalea.__path__ += vplants.__path__
    except:
        pass


