"""
Package.

The package manager register, install and load packages.
"""

# $License: $

import cPickle
import config
from path import path

###############################################################################

class NodeFactory(object):
    def __init__(self, name, desc, cat, dep, node, widget= ''):
	"""
	Create a node factory.
	
	>>> class mynode(alea.node.Node):
	...    def __call__( self, inputs ):
	...        pass
	        
	 >>> 
	 >>> n= NodeFactory('MyNode', 'This is my node','Data',
         ['gnuplot','alea'],mynode)
	 >>> p= Package('blablabla',[n],[w])
	 >>> PackageManager.register(p)

	:Parameters:
	  - `name` : user name for the node
	  - `desc` : description of the node
	  - `cat` : category of the node
	  - `dep` : dependencies of this module
	  - `node` : class of the node to be created
	  - `widget` : alea widget name associated if any
	
	:Types:
	  - `name` : String
	  - `desc` : String
	  - `cat` : String
	  - `dep` : list [String]
	  - `node` : class
	  - `widget` : String
	"""

        self.name=name
        self.description=desc
        self.category=cat
        self.dependencies=dep
        self.node=node
        self.widget= widget
        
    def __call__(self):
        return self.node()

###############################################################################

class WidgetFactory(object):
    def __init__(self, name, icons, widget, node ):
	"""
	>>> w= WidgetFactory("mywidget","toto.pxm",mywidget,mynode)
	>>> 
	"""
	self.name= name
	self.icons= icons
	self.widget= widget
	self.node= node
        
    def __call__(self, node):
        if isinstance(node,self.node):
            return self.widget(node)
        return None
            

###############################################################################

def create_node2widget( widgets ):
    '''
    Return a dict [node] = associated widget
    '''
    d= {}
    for w in widgets:
        d[w.node.__name__]= w
    return d
        

class Package(object):

    def __init__(self, 
    		 name, 
    		 system_name,
    		 version, 
                 legal_stuff={'license':'','authors':''}, 
                 node_factories= [],
                 widget_factories= [],
                 directories= {'pkg':'','doc':'','test':'','example':'','lib':'','bin':'','setting':''}
                 ):
        self.name=name  
    	self.system_name=system_name 
    	self.version=version 
    	self.legal_stuff=legal_stuff 
    	self.node_factories=node_factories
    	self.widget_factories= widget_factories
    	self.directories=directories
        self.node2widget= create_node2widget(widget_factories)
	self.loaded= False
	self.installed= False
    
    def get_nodes(self):
    	""" for now a composent is a name """
        return self.node_factories
    nodes= property(get_nodes) 
    
    def get_dependencies(self):
        d= {}
        for n in self.nodes:
            deps= n.dependencies
            for dep in deps:
                d[dep]= dep
        return d.keys()
    dependencies= property(get_dependencies)
    
    def load(self):
    	""" Load the current package """
    	self.loaded= True
    	return True
    
    def install(self, dest_pkg):
        """ Install this package in the dest package directories"""
        self.installed= True
        return True

    def uninstall(self, dest_pkg):
        """ UnInstall this package in the dest package directories"""
        self.installed= False
        return True
        
        

###############################################################################

def pid(package):
    """ Package id. """
    return package.name

###############################################################################

#TODO
def alea_package():
    dirs={}
    dirs['settings']='.'
    
    return Package('alea', 'alea', config.version,directories=dirs)

###############################################################################

class PackageManager(object):
    """
    The PackageManager registers, installs and loads packages.
    """
    def __init__(self):
        self.pkgs= {}
        self._node2widget=None

    def __repr__(self):
        return repr(self.pkgs)
        
    def register( self, package ):
        '''
        Registers a package in the package manager
        Returns true

        :Parameters:
        - package
        '''
        self.pkgs[pid(package)]= package
        self._node2widget= None
        return True

    def unregister( self, package ):
        '''
        Removes a package from the available package list of the package manager
        Returns true if the package was in the list, false otherwise
        
        :Parameters: 
        - package
        '''
        if pid(package) in self.pkgs:
            del self.pkgs[pid(package)]
            self._node2widget= None
            return True
        else:
            return False
                
    def install( self, package ):
        """
        Installs the package's files in the OpenAlea file tree

        :Parameters:
        - package
        """
        if not pid(package) in self.pkgs:
            self.register(package)
        return package.install(alea_package())

    def uninstall( self, package ):
        '''
        Removes package's files from the OpenAlea file tree

        :Parameters: 
        - package 
        '''
        if pid(package) in self.pkgs:
            self.unregister(package)
        return package.uninstall(alea_package())

    def packages(self):
        '''
        Returns a package id list which contains the available packages

        '''
        return self.pkgs.keys()

    def loaded_packages(self):
        '''
        returns the list of loaded packages id 
        ''' 
    	return [ name for name, pkg in self.pkgs.iteritems() if pkg.loaded ]

    def installed_packages(self):
        '''
        returns the list of installed packages id 
        '''
    	return [ name for name, pkg in self.pkgs.iteritems() if pkg.installed ]

    def widget(self, node):
        """
        Return a widget instance for a given node instance. 
        """
        if not self._node2widget:
            self._compute_node2widget()
            
        w= self._node2widget.get(node.__class__.__name__)
        if w:
            return w(node)
        else:
            return None

    def __getitem__(self,pkg_id):
        '''
        returns the package identified by pkg_id
        '''
        return self.pkgs[pkg_id]
        
    def _compute_node2widget( self ):
        '''
        rebuild dependencies list between nodes and widget
        '''
        self._node2widget= {}
        for p in self.pkgs.values():
            self._node2widget.update(p.node2widget)

###############################################################################
# PackageManager Factory

def load_pkg_manager():
    '''
    Return the OpenAlea PackageManager.
    '''
    fn= config.setting_dir / "PackageManager.ini"
    if fn.exists():
        f= fn.open()
        pkg_mgr= cPickle.load(f)
    else:
        pkg_mgr= PackageManager()
        
    return pkg_mgr
    
def save_pkg_manager( pkg_manager ):
    '''
    Save the PackageManager into an ini file
    '''
    fn= config.setting_dir / "PackageManager.ini"
    f= fn.open('w')
    cPickle.dump(pkg_manager,f)

def register(package):
    '''
    Register a package into the OpenAlea PackageManager
    Saves the new registered package list
    '''
    pkg_manager= load_pkg_manager()
    is_ok= pkg_manager.register(package)
    save_pkg_manager(pkg_manager)
    return is_ok

def install(package):
    
    pkg_manager= load_pkg_manager()
    is_ok= pkg_manager.install(package)
    save_pkg_manager(pkg_manager)
    return is_ok

def unregister(package):
    pkg_manager= load_pkg_manager()
    is_ok= pkg_manager.unregister(package)
    save_pkg_manager(pkg_manager)
    return is_ok

def uninstall(package):
    pkg_manager= load_pkg_manager()
    is_ok= pkg_manager.uninstall(package)
    save_pkg_manager(pkg_manager)
    return is_ok

