"""
Automatical extraction of openalea factories for python modules and packages  
"""

"""
TODO:
  - remove all ##
  - parse package (hierarchically)
  
"""
from openalea.core.package import Package


def parse_module(module_name):
    """
    Create an openalea package from a python module
    
    :Inputs::
      `module_name`: 
        - either a python module
        - or the *full* name of the module to parse (i.e. 'pck.sub_pck.module')
    """
    if isinstance(module,type(sys)):
        modulename = module.__name__
    else:
        modulename = module                           
        module = load_module(modulename, [])
    
    info = dict()
    info['license']     = getattr(module,'__license__',    'not licensed')
    info['version']     = getattr(module,'__version__',    '0.1.0')
    info['authors']     = getattr(module,'__authors__',    '')
    info['institutes']  = getattr(module,'__institutes__', '')
    info['url']         = getattr(module,'__url__',        '')
    info['description'] = getattr(module,'__description__',module.__doc__)
    info['publication'] = getattr(module,'__publication__','')
    
    pck = package.Package(name=modulename,metainfo=info)
    
    ##todo: for all fct in module.__factories__: pck.add_factory
    
    return pck    
    
def load_module(module_name, search_path=[]):
    """
    load `module_name`
    
    :Inputs:
      - `module_name`
          string with the name of the module as it is given to import 
          (i.e. containing package dependancies separated by '.')
      - `search_path`
          Additional search directories, given as a list of string, to look for 
          `module_name` (and its parent package) if it is in not in `sys.path`.
    """
    if len(search_path)>0:
        syspath  = sys.path
        sys.path = search_path + sys.path
        
    module = __import__(module_name,globals(),{}, [''], -1)
    
    if len(search_path)>0:
        sys.path = syspath

    return module
