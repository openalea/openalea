# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Julien Diener  <julien.diener@inria.fr>
#                       Julien Coste   <julien.coste@inria.fr>
#                       Guillaume baty <guillaume.baty@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""
Automatical extraction of openalea factories for python modules and packages  

TODO: bad name. The module is not parsed but imported.
"""
"""
TODO:
  - remove all ##
  - parse package (hierarchically)a. REVIEW: Replace parse by traverse.
  
"""
import sys
from openalea.core.package   import DynamicPackage
from openalea.core.node      import Factory
from openalea.core.signature import Signature

def parse_module(module, module_dir=None):
    """
    Create an openalea package from a python module
    
    :Inputs::
      `module`: 
        - either a python module
        - or the *full* name of the module to parse (e.g. 'pkg.sub_pkg.module')
      `module_dir`:
        Base directory of `module` if it is not in the python path. 
    """
    if isinstance(module,type(sys)):
        module_name = module.__name__
    else:
        module_name = module                           
        module = import_module(module_name, [module_dir] if module_dir else [])
    
    info = dict()
    info['editable']    = getattr(module, '__editable__', True)
    info['icon']        = getattr(module, '__icon__', '')
    info['license']     = getattr(module, '__license__', 'not licensed')
    info['version']     = getattr(module, '__version__', '0.1.0')
    info['authors']     = getattr(module, '__authors__', '')
    info['institutes']  = getattr(module, '__institutes__', '')
    info['url']         = getattr(module, '__url__', '')
    info['doc']         = getattr(module, '__doc__')
    info['description'] = getattr(module, '__description__', '')
    info['publication'] = getattr(module, '__publication__', '')
    

    pkg = DynamicPackage(name=module_name,metainfo=info)
    
    for fct in getattr(module, '__factories__', []):
        add_factory(pkg,fct)

    return pkg     
    
def add_factory(pkg, fct, base_dir=None):
    """
    Add a (Node) Factory for function `fct` into package `pkg`
    
    If function does not contain suitable meta_info, try to take it from `pkg_info`
    """
    s = Signature(fct)
    base_dir = [base_dir] if base_dir else None
    
    fac = Factory(s.name, description=s.get_doc(), inputs=s.parameters, outputs=None,
                  nodemodule=fct.__module__, nodeclass=s.name, search_path=base_dir, authors=pkg.metainfo.get('authors',None))
        ##, category='', widgetmodule=None, widgetclass=None, **kargs

    pkg[s.name] = fac
    
def import_module(module_name, search_path=[]):
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
