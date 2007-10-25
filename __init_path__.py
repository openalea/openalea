# This file allow to use openalea packages without installing them.

def set_path():
    import os, sys
    from os.path import join
    import pkg_resources
    openalea = sys.modules['openalea']


    dir = os.path.dirname(__file__)

    pkg_resources._handle_ns('openalea.core', join('core/src'))
    

    pkg_dirs = { 'openalea.core': "core/src",
                 'openalea.visualea':"visualea/src",
                 'openalea.catalog' : "catalog/src",
                 'openalea.sconsx' : "sconsx/src",
                 'openalea.plotools' : "plotools/src",
                 'openalea.scipy' : "scipy/src",
                 'openalea.rpy' : "rpy/src",
				 'openalea.spatial' : "spatial/src",
                 'openalea.stand' : "stand/src",
                 }

 
    for name, subdir in  pkg_dirs.items():

        pkg_resources._handle_ns(name, join(dir, subdir))

    try:
        import vplants
        openalea.__path__ += vplants.__path__
    except:
        pass


