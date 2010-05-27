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

dtkCorePath = "/Users/moscardi/Work/dtk/dtk_build/modules"
PluginsPath = "/Users/moscardi/Work/medular-plugins/medular-plugins_build/lib:/Users/moscardi/Work/mars-plugins/build/lib"

import sys

try:
    sys.path.insert(0, dtkCorePath)
    del sys.modules['core']
    del core
except: pass

import core
from openalea.core import *
from openalea.core.external import *

#import py_dtk


def register_packages(pkgmanager):

    metainfo={ 'version' : '',
               'license' : '',
               'authors' : '',
               'institutes' : 'INRIA',
               'description' : '',
               'url' : ''
                }

    dtk_obj = dtk_Builder(PluginsPath)
    dtk_obj.get_plugins()

    for plugin in dtk_obj.plugins:
        dtk_obj.get_plugin_description(plugin)
        metainfo['description'] = dtk_obj.plugin_description
        package = dtk_obj.add_package(plugin, metainfo)
        #dtk_obj.add_factory(plugin, package)
        if package:
            pkgmanager.add_package(package)


class dtk_Builder(object):
    """
    """

    def __init__(self, plugins_path = PluginsPath):
        
        self.plugins_path = plugins_path

        self.plugin_manager = None
        self.plugins = None
        self.data_plugins = {}
        self.plugin_name = None
        self.plugin_types = None
        self.plugin_description = None
        self.category = None
        self.factory = None
        self.inputs_list = []
        self.inputs = None
        self.load_plugin_manager()
        self.get_data_plugins()

    def load_plugin_manager(self):
        """
        Loading of plugin manager of dtk
        """

        self.plugin_manager = core.dtkPluginManager.instance()
        self.plugin_manager.setPath(self.plugins_path)
        self.plugin_manager.initialize()
    

    def get_plugins(self):
        """
        Loading the list of plugins
        """
    
        self.plugins = [p.name() for p in self.plugin_manager.plugins()]
    

    def get_plugin_name(self, plugin):
        """
        Getting the plugin name
        """
    
        self.plugin_name = self.plugin_manager.plugin(plugin).name()


    def get_plugin_types(self, plugin):
        """
        Loading the list of plugin types
        """
    
        self.plugin_types = self.plugin_manager.plugin(plugin).types()


    def get_plugin_description(self, plugin):
        """
        Getting of the description of plugin
        """
    
        self.plugin_description = self.plugin_manager.plugin(plugin).description()


    def get_data_plugins(self):
        """
        Getting the list of data plugins
        """
    
        self.get_plugins()
        for p in self.plugins:
            self.get_plugin_types(p)
            for t in self.plugin_types:
                dtk_data = core.dtkAbstractDataFactory.instance().create(t)
                if dtk_data:
                    self.data_plugins[dtk_data] = t


    def add_package(self, plugin, metainfo):
        self.get_category(plugin)
        #if self.category == 'Data':
        #    if ('Reader' in plugin) or ('Writer' in plugin):
        #        package = Package("dtk.%s" %plugin, metainfo)
        #        self.add_factory(plugin, package)
        #    else:
        #        package = None 
        #else:
        #    package = Package("dtk.%s" %plugin, metainfo)
        #    self.add_factory(plugin, package)
    
        package = Package("dtk.%s" %plugin, metainfo)
        self.add_factory(plugin, package)

        return package


    def add_factory(self, plugin, package):
        self.get_plugin_types(plugin)
        # getting of category of plugin (data, view or process)   
        for t in self.plugin_types:
            # creating of dtkFactory (dtkAbstractData, dtkAbstractView, or dtkAbstractProcess)
            self.create_dtk_factory(t)
            in_list = self.define_inputs(t)
            out_list = self.define_outputs()
            node_class = self.define_nodeclass()   
            nf = Factory(   name= t, 
                            description= self.plugin_manager.plugin(plugin).description(),
                            category = "dtk.%s" %self.category, 
                            nodemodule = "py_dtk",
                            nodeclass = node_class,
                            inputs = in_list,
                            outputs = out_list
                            )
            
            package.add_factory( nf )


    def create_dtk_factory(self, plugin_type):

        if self.category == 'View': 
            if 'Interactor' in plugin_type:
                self.factory = None    
            else : 
                self.factory = core.dtkAbstractViewFactory.instance().create(plugin_type)

        if self.category == 'Process': 
            self.factory = core.dtkAbstractProcessFactory.instance().create(plugin_type)

        if self.category == 'Data':
            if ('Reader' in plugin_type) or ('Writer' in plugin_type):
                self.factory = None
            else: 
                self.factory = core.dtkAbstractDataFactory.instance().create(plugin_type)


    def define_inputs(self, plugin_type):
        inputs_list = [] 
        if self.factory:
            try:
                self.inputs_list = self.factory.properties()
                inputs_list = [dict(name=input, interface=IEnumStr(self.factory.propertyValues(input)), value=self.factory.property(input)) for input in self.inputs_list]
            except:
                pass
            if self.category != 'Data':
                inputs_list.insert(0,dict(name='dtkData', interface=None))
                if self.category == 'View':
                    inputs_list.append(dict(name='dtkViewInteractor', interface= None))
            else:
                inputs_list.append(dict(name='data', interface= None))
        else:
            if self.category == 'Data':
                inputs_list.insert(0,dict(name='filename', interface= IFileStr))
                if ('Reader' in plugin_type):
                    inputs_list.append(dict(name='dtkDataType', interface=IEnumStr([self.data_plugins[d] for d in self.data_plugins if d.reader(plugin_type)]),))
                elif ('Writer' in plugin_type):
                    inputs_list.append(dict(name='dtkDataType', interface=IEnumStr([self.data_plugins[d] for d in self.data_plugins if d.writer(plugin_type)]),))
                else:
                    return    
            else:
                inputs_list = None

        return inputs_list


    def define_outputs(self):
        if self.factory:
            output = (dict(name='dtkData', interface=None),)
        else :
            if self.category == 'View':
                output = (dict(name='dtkViewInteractor', interface=None),)
            else:
                output = (dict(name='dtkData', interface=None),)

        return output


    def define_nodeclass(self):
        if self.factory:
            node_class = 'dtk_%s' %self.category            
        else:
            if self.category == 'View':
                node_class = 'dtk_Interactor' 
            elif self.category == 'Data':
                node_class = 'dtk_Data_Reader_Writer'
            else:
                return
 
        return node_class


    def get_category(self, plugin):

        if 'view' in self.plugin_manager.plugin(plugin).tags():
            self.category = 'View'
 
        elif 'process' in self.plugin_manager.plugin(plugin).tags():
            self.category = 'Process'
 
        elif 'data' in self.plugin_manager.plugin(plugin).tags():
            self.category = 'Data'
 
        else:
            'unknown plugin'
            return

