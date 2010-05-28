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

try:
    sys.path.insert(0, dtkCorePath)
    del sys.modules['core']
    del core
except: pass

from PyQt4 import QtCore, QtGui
import core
import sip

from openalea.core import *


class dtk_Process(Node):
    """
    """

    def __init__(self, inputs=(), outputs=()):

        Node.__init__(self, inputs, outputs)
        self.process = None

    def __call__(self, inputs):

        if not self.process:
            self.process = core.dtkAbstractProcessFactory.instance().create(self.get_caption())
            self.process.setInput(self.get_input("dtkData"))
            for port in self.input_desc:
                self.process.setProperty(port['name'], self.get_input(port['name']))
            self.process.update()
            return self.process.output()


class dtk_View(Node):
    """
    """

    def __init__(self, inputs=(), outputs=()):

        Node.__init__(self, inputs, outputs)
        self.view = None


    def __call__(self, inputs):

        if not self.view:
            self.view = core.dtkAbstractViewFactory.instance().create(self.get_caption())
            self.view.showMaximized()

            self.view.setData(self.get_input("dtkData"))

        for p in self.view.properties():
            self.view.setProperty(p, self.get_input(p))

        if (self.get_input("dtkViewInteractor")):

            interactor_name = self.get_input("dtkViewInteractor")['name']
            interactor_properties = self.get_input("dtkViewInteractor")['properties']

            self.view.enableInteractor(interactor_name)
            interactor = self.view.interactor(interactor_name)
            
            for p in interactor_properties:
                interactor.setProperty(p, interactor_properties[p])
                
        if (self.get_input("dtkViewNavigator")):
            
            navigator_name = self.get_input("dtkViewNavigator")['name']
            navigator_properties = self.get_input("dtkViewNavigator")['properties']

            self.view.enableNavigator(navigator_name)
            navigator = self.view.navigator(navigator_name)
            
            for p in navigator_properties:
                navigator.setProperty(p, navigator_properties[p])

        if (self.get_input("dtkViewAnimator")):
            
            animator_name = self.get_input("dtkViewAnimator")['name']
            animator_properties = self.get_input("dtkViewAnimator")['properties']

            self.view.enableAnimator(animator_name)
            animator = self.view.animator(animator_name)
            
            for p in animator_properties:
                animator.setProperty(p, animator_properties[p])
        
        self.view.update()
        self.view.reset()
        widget = self.view.widget()
        widget = sip.wrapinstance(widget.__long__(), QtGui.QWidget)
        widget.show()


class dtk_Data_Reader_Writer(Node):
    """
    """

    def __init__(self, inputs=(), outputs=()):

        Node.__init__(self, inputs, outputs)
        self.data = None


    def __call__(self, inputs):

        if not self.data:
            self.data = core.dtkAbstractDataFactory.instance().create(self.get_input("dtkDataType"))
            if 'Reader' in self.get_caption():
                self.data.enableReader(self.get_caption())
                self.data.read(self.get_input("filename"))
            elif 'Writer' in self.get_caption():
                self.data.enableWriter(self.get_caption())
                self.data.write(self.get_input("filename"))
            else:
                return
        return self.data


class dtk_Data(Node):
    """
    """

    def __init__(self, inputs=(), outputs=()):

        Node.__init__(self, inputs, outputs)
        self.data = None


    def __call__(self, inputs):
        
        if not self.data:
            self.data = core.dtkAbstractDataFactory.instance().create(self.get_caption())
            self.data.setData(self.get_input("data"))
        return self.data


class dtk_Interactor(Node):
    """
    """

    def __init__(self, inputs=(), outputs=()):

        Node.__init__(self, inputs, outputs)
        self.dtkViewInteractor = None

    def __call__(self, inputs):
        
        output = {}
        properties = {}
        output['name'] = self.get_caption()
        for p in range(self.get_nb_input()):
            input = self.input_desc[p]['name']
            properties[input] = self.get_input(input)
        output['properties'] = properties
        return output




