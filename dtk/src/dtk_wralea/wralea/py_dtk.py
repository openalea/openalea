# -*- python -*-
#
#       dtk function implementation
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

import sys, sip
from PyQt4 import QtCore, QtGui

try:
    sys.path.insert(0, dtkCorePath)
    del sys.modules['core']
    del core
except: pass

import core

from openalea.core import *


class dtk_Process(Node):
    """
    """

    def __init__(self, inputs=(), outputs=()):

        Node.__init__(self, inputs, outputs)
        self.dtk_process = None

    def __call__(self, inputs):

        if not self.dtk_process:
            self.dtk_process = core.dtkAbstractProcessFactory.instance().create(self.get_caption())
            self.dtk_process.setInput(self.get_input("dtkData"))
            for port in self.input_desc:
                self.dtk_process.setProperty(port['name'], self.get_input(port['name']))
            self.dtk_process.update()
            return self.dtk_process.output()


class dtk_View(Node):
    """
    """

    def __init__(self, inputs=(), outputs=()):

        Node.__init__(self, inputs, outputs)
        self.dtk_view = None


    def __call__(self, inputs):

        if not self.dtk_view:
            self.dtk_view = core.dtkAbstractViewFactory.instance().create(self.get_caption())
            self.dtk_view.setData(self.get_input("dtkData"))
            self.dtk_view.enableInteractor(self.get_input("dtkViewInteractor"))
        for port in self.input_desc:
            self.dtk_view.setProperty(port['name'], self.get_input(port['name']))

        widget = self.dtk_view.widget()
        widget = sip.wrapinstance(widget.__long__(), QtGui.QWidget)
        widget.show()


class dtk_Data_Reader_Writer(Node):
    """
    """

    def __init__(self, inputs=(), outputs=()):

        Node.__init__(self, inputs, outputs)
        self.dtk_data = None


    def __call__(self, inputs):

        if not self.dtk_data:
            self.dtk_data = core.dtkAbstractDataFactory.instance().create(self.get_input("dtkDataType"))
            if 'Reader' in self.get_caption():
                self.dtk_data.enableReader(self.get_caption())
                self.dtk_data.read(self.get_input("filename"))
            elif 'Writer' in self.get_caption():
                self.dtk_data.enableWriter(self.get_caption())
                self.dtk_data.write(self.get_input("filename"))
            else:
                return
        return self.dtk_data


class dtk_Data(Node):
    """
    """

    def __init__(self, inputs=(), outputs=()):

        Node.__init__(self, inputs, outputs)
        self.dtk_data = None


    def __call__(self, inputs):
        
        if not self.dtk_data:
            self.dtk_data = core.dtkAbstractDataFactory.instance().create(self.get_caption())
            self.dtk_data.setData(self.get_input("data"))
        return self.dtk_data


class dtk_Interactor(Node):
    """
    """

    def __init__(self, inputs=(), outputs=()):

        Node.__init__(self, inputs, outputs)


    def __call__(self, inputs):
        
        return self.get_caption()



#class dtk_DataReader(Node):
#    """
#   Input: filename
#   Ouput : dtkData object
#    """
#
#    def __init__(self):
#
#        Node.__init__(self)
#
#        self.plugin_manager = None
#
#        self.data_plugin = self.plugin_manager.plugin('itkDataImagePlugin')
#        data_types = self.data_plugin.types()
#
#        self.reader_plugin = self.plugin_manager.plugin('itkDataImageReaderPlugin')
#        self.reader_types = self.reader_plugin.types()
#
#        self.add_input( name = "filename", interface = IFileStr) 
#        self.add_input( name = "data type", interface = IEnumStr(data_types)) 
#        self.add_output( name = "itkDataImage", interface = None) 
#
#
#    def __call__(self, inputs):
#
#
#        data_factory = core.dtkAbstractDataFactory.instance()
#
#        file_type = self.get_input("filename").rsplit('.')[1]
#        
#        data_type= self.get_input("data type")
#        data_reader = [r for r in self.reader_types if file_type.upper() in r]
#
#	dtk_data = data_factory.create(data_type)
#        dtk_data.enableReader(data_reader[0])
#        dtk_data.read(self.get_input("filename"))
#        return dtk_data
#
