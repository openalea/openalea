from string import Template

pkg_template=Template('''
  metainfo={ "version" : "${__version__}",
             "license" : "${__license__}",
             "authors" : "${__authors__}",
             "institutes" : "${__institutes__}",
             "description" : """${__doc__}""",
             "url" : "${__url__}"
             }
 
  package= Package("${package_name}", metainfo)
''')


register_node_template= Template('''
  nf = Factory( name= "${name}", 
                description= """${description}""", 
                category = "${category}", 
                nodemodule = "${module}",
                nodeclass = "${classname}",
                )
  package.add_factory( nf )
''')

register_package='''
  pkgmanager.add_package(package)
'''

def create_wralea(module_name):

  import imp
  (file, pathname, desc)= imp.find_module(module_name)
  module = imp.load_module(module_name, file, pathname, desc)
  if( file ): 
    file.close()

  pkg_dict= {}
  pkg_dict.setdefault( '__version__', 
                       module.__dict__.get('__version__','0.0.1') )
  pkg_dict.setdefault( '__license__',
                       module.__dict__.get('__license__','CECILL-C') )
  pkg_dict.setdefault( '__authors__',
                       module.__dict__.get('__authors__','CPL') )
  pkg_dict.setdefault( '__institutes__',
                       module.__dict__.get('__institutes__','CIRAD') )
  pkg_dict.setdefault( '__url__',
                       module.__dict__.get('__url__',
                        'http://openalea.gforge.inria.fr') )
  pkg_dict.setdefault('__doc__',module.__dict__.get('__doc__'))
  pkg_dict['package_name']=module_name
  pkg_str= pkg_template.safe_substitute(pkg_dict)

  wralea_str= '''
from openalea.core import *

def register_packages(pkgmanager):
'''
  wralea_str+= pkg_str

  for f_name in module.__all__:
    func= module.__getattribute__(f_name)
    d= {}
    d['name']= f_name

    desc= func.__doc__
    if func.__doc__ != None:
      d['description']= func.__doc__
    else: 
      d['description']= ""

    d['category']= 'user node'
    d['module']=module_name
    d['classname']= f_name

    s= register_node_template.substitute(d)
    wralea_str+= s

  wralea_str+= register_package
  return wralea_str




    
