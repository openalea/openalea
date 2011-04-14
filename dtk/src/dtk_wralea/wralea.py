# -*- python -*-
#
#       dtk package: DTK package interface
#
#       2010 INRIA - CIRAD - INRA  
#
#       File author(s): Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

'''
CR: Paths are user dependent.
Options: 
    - Use environment variable: DTK_DIR or DTKPATH
    - Search on the system where DTK is installed
    - use config files (.dtkrc)

Another option is to add DTKPATH in the config settings of OpenAlea.
'''

# The file .config/inria/dtk.conf is used to set Plugins PATH

dtkCorePath = "/Users/moscardi/Work/dtk/dtk_build/modules"
dtkCorePath = "/home/pradal/local/inria/modules"

import os, sys
dtkPath = os.getenv('DTKPYTHONPATH',dtkCorePath)

# DTK must be installed as a Python package.
# Change import core into import dtk.core
# You do not have the permission to change the singleton sys.modules
# until you have to restore it at the end of the file.
try:
    sys.path.insert(0, dtkPath)
    del sys.modules['core']
    del core
except: pass


import core
from openalea.core import *
from openalea.core.external import *


def register_packages(pkgmanager):

    metainfo={ 'version' : '',
               'license' : '',
               'authors' : '',
               'institutes' : 'INRIA',
               'description' : '',
               'url' : ''
                }

    dtk_manager = DTKPluginManager()

    for plugin in dtk_manager.plugins:
        # create a python property for plugil_description
        # name it description rather than plugin_description
        desc = plugin.description()
        metainfo['description'] = desc
        package = dtk_manager.alea_package(plugin, metainfo)
        if package:
            pkgmanager.add_package(package)


class DTKPluginManager(object):
    """
    """

    def __init__(self):
        
        
        self.plugin_manager = None
        self._plugins = None
        self._data_plugins = {}
        self.factory = None
        self.inputs_list = []

        self._init()

    def _init(self):
        """
        Loading of plugin manager of dtk
        """

        self.plugin_manager = core.dtkPluginManager.instance()
        self.plugin_manager.initialize()
    

    @property
    def plugins(self):
        """
        Loading the list of plugins
        """
    
        if self._plugins is None:
            self._plugins = list(self.plugin_manager.plugins())
        return self._plugins
    


    @property
    def data_plugins(self):
        """
        Return the list of data plugins
        """
        if not self._data_plugins:
            for plugin in self.plugins:
                for t in plugin.types():
                    dtk_data = core.dtkAbstractDataFactory.instance().create(t)
                    if dtk_data:
                        self._data_plugins[dtk_data] = t
        return self._data_plugins

    def alea_package(self, plugin, metainfo):
        ''' Create an OpenAlea package. '''
        package = Package("dtk.%s" %plugin.name(), metainfo)
        self.add_alea_factories(plugin, package)

        return package


    def add_alea_factories(self, plugin, package):
        # getting of category of plugin (data, view or process)   
        desc = plugin.description()
        category = self.get_category(plugin)
        if category == "Reader" or category == "Writer":
            # creating of dtkFactory (dtkAbstractData, dtkAbstractView, or dtkAbstractProcess)
            #self.create_dtk_factory(t, category)
            #in_list = self.define_inputs(category)
            #out_list = self.define_outputs(category)
            #node_class = self.define_nodeclass(plugin)   
            nf = Factory(name= "%s" %plugin.name(), 
                        description= desc,
                        category = "dtk", 
                        nodemodule = "py_dtk",
                        nodeclass = "dtk%s" %category,
                        inputs = [dict(name='filename', interface= IFileStr)],
                        outputs = (dict(name='dtkData', interface=None),)
                        )
            package.add_factory( nf )

        else :

            if category != "Data":

                for t in plugin.types():
                    # creating of dtkFactory (dtkAbstractData, dtkAbstractView, or dtkAbstractProcess)
                    self.create_dtk_factory(t, category)
                    in_list = self.define_inputs(t, category)
                    out_list = self.define_outputs(t, category)
                    node_class = self.define_nodeclass(t, category)   
                    nf = Factory(   name= t, 
                            description= desc,
                            category = "dtk.%s" %category, 
                            nodemodule = "py_dtk",
                            nodeclass = "dtk%s" %category,
                            inputs = in_list,
                            outputs = out_list
                            )
            
                    package.add_factory( nf )


    def create_dtk_factory(self, plugin_type, category):

        if category == 'View':
            view_factory = core.dtkAbstractViewFactory.instance()
            if 'Interactor' in plugin_type:
                self.factory = view_factory.interactor(plugin_type)
            elif 'Animator' in plugin_type:
                self.factory = view_factory.animator(plugin_type)
            elif 'Navigator' in plugin_type:
                self.factory = view_factory.navigator(plugin_type)
            else : 
                self.factory = view_factory.create(plugin_type)
  
        if category == 'Process': 
            self.factory = core.dtkAbstractProcessFactory.instance().create(plugin_type)

        if category == 'Data':
            if ('Reader' in plugin_type) or ('Writer' in plugin_type):
                self.factory = None
            else: 
                self.factory = core.dtkAbstractDataFactory.instance().create(plugin_type)


    def define_inputs(self, plugin_type, category):
        inputs_list = [] 
        #data_plugins = self.data_plugins

        if self.factory:
            try:
                self.inputs_list = self.factory.properties()
                inputs_list = [dict(name=input, interface=IEnumStr(self.factory.propertyValues(input)), value=self.factory.property(input)) for input in self.inputs_list]
            except:
                pass
            #if category == 'Data':
            #    inputs_list.insert(0,dict(name='data', interface= None))

            if category == 'View':
                if not ('Interactor' in plugin_type) or ('Animator' in plugin_type) or ('Navigator' in plugin_type):
                    inputs_list.insert(0,dict(name='dtkData', interface=None))
                    inputs_list.append(dict(name='dtkViewAnimator', interface= None))
                    inputs_list.append(dict(name='dtkViewInteractor', interface= None))
                    inputs_list.append(dict(name='dtkViewNavigator', interface= None))
            elif category == 'Process':
                inputs_list.insert(0,dict(name='dtkData', interface=None))
        else:
            #if category == 'Data':
            #    inputs_list.insert(0,dict(name='filename', interface= IFileStr))
            #    if ('Reader' in plugin_type):
            #        inputs_list.append(dict(name='dtkDataType', interface=IEnumStr([k for d, k in data_plugins.iteritems() if d.reader(plugin_type)]),))
            #    elif ('Writer' in plugin_type):
            #        inputs_list.append(dict(name='dtkDataType', interface=IEnumStr([k for d, k in data_plugins.iteritems() if d.writer(plugin_type)]),))
            #    else:
            #        return    
            #else:
            #    inputs_list = None
            if category == 'Reader' or category == 'Writer':
                inputs_list.append(dict(name='filename', interface= IFileStr))
        return inputs_list


    def define_outputs(self, plugin_type, category):
        if category == 'View':
            if ('Interactor' in plugin_type):
                output = (dict(name='dtkViewInteractor', interface=None),)
            elif ('Animator' in plugin_type):
                output = (dict(name='dtkViewAnimator', interface=None),)
            elif ('Navigator' in plugin_type):
                output = (dict(name='dtkViewNavigator', interface=None),)
            else:
                output = (dict(name='dtkData', interface=None),)
        else:
            output = (dict(name='dtkData', interface=None),)

        return output


    def define_nodeclass(self, plugin_type, category):
        node_class = None

        if self.factory:           
            if category == 'View':
                if ('Interactor' in plugin_type) or ('Animator' in plugin_type) or ('Navigator' in plugin_type):
                    node_class = 'dtk_Interactor'
                else:
                    node_class = 'dtk_View'
            else:
                node_class = 'dtk_%s' %category

        elif category == 'Data':
            node_class = 'dtk_Data_Reader_Writer'
        
        return node_class


    def get_category(self, plugin):
        category = None
        if 'view' in plugin.tags():
            category = 'View'
        elif 'process' in plugin.tags():
            category = 'Process'
        elif 'data' in plugin.tags():
            if 'reader' in plugin.tags():
                category = 'Reader'
            elif 'writer' in plugin.tags():
                category = 'Writer'
            else:
                category = 'Data'
        return category


