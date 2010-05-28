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

class DtkNode(Node):
    """

    """
    def __init__(self, inputs, outputs):
        super(DtkNode,self).__init__(inputs, outputs)
        self.dtk_factory = None
        self._data = None
    
    def data(self, name='dtkData'):
        factory = self.dtk_factory

        if factory is None:
            self._data = self.get_input(name)
            factory.setInput(self._data)
            
        data = self.get_input(name)
        if data != self._data:
            self._data = data
            factory.setInput(self._data)

    def setProperty(self):        
        for p in self.dtk_factory.properties():
            self.dtk_factory.setProperty(p, self.get_input(p))

    #@property
    def name(self):
        return self.get_caption()


class dtk_Process(DtkNode):
    """
    """

    def __call__(self, inputs):

        if self.dtk_factory is None:
            self.dtk_factory = core.dtkAbstractProcessFactory.instance().create(self.name())
            
        self.data('dtkData')
        self.setProperty()

        self.dtk_factory.update()
        return self.dtk_factory.output(),


class dtk_View(DtkNode):
    """
    """

    def interact(self, name):
        self.dtk_factory.enableInteractor(name)
        return self.dtk_factory.interactor(name)
    def animate(self, name):
        self.dtk_factory.enableAnimator(name)
        return self.dtk_factory.animator(name)
    def navigate(self, name):
        self.dtk_factory.enableNavigator(name)
        return self.dtk_factory.navigator(name)

    def __call__(self, inputs):

        if self.dtk_factory is None:
            self.dtk_factory = core.dtkAbstractViewFactory.instance().create(self.name())
            self.dtk_factory.showMaximized()

        self.data('dtkData')
        self.setProperty()

        d = dict(zip(("dtkViewInteractor","dtkViewNavigator","dtkViewAnimator"),
                     (self.interact, self.navigate, self.animate)))        
        for dtkview, method in d.items():
            
            input = self.get_input(dtkview)
            if input:
                name = input['name']
                properties = input['properties']
                interactor = method(name)

                for p, k in properties.iteritems():
                    interactor.setProperty(p, k)
                
        self.dtk_factory.update()
        self.dtk_factory.reset()

        widget = self.dtk_factory.widget()
        widget = sip.wrapinstance(widget.__long__(), QtGui.QWidget)
        widget.show()


class dtk_Data_Reader_Writer(DtkNode):
    """
    """


    def __call__(self, inputs):

        if self.dtk_factory is None:
            self.dtk_factory = core.dtkAbstractDataFactory.instance().create(self.get_input("dtkDataType"))
            if 'Reader' in self.name():
                self.dtk_factory.enableReader(self.name())
                self.dtk_factory.read(self.get_input("filename"))
            elif 'Writer' in self.name():
                self.dtk_factory.enableWriter(self.name())
                self.dtk_factory.write(self.get_input("filename"))
            else:
                return
        return self.dtk_factory


class dtk_Data(DtkNode):
    """
    """

    def __call__(self, inputs):
        
        if self.dtk_factory is None:
            self.dtk_factory = core.dtkAbstractDataFactory.instance().create(self.name())

        self.data('data')
        self.setProperty()

        return self.dtk_factory


class dtk_Interactor(DtkNode):
    """
    """

    def __call__(self, inputs):
        
        output = {}
        properties = {}
        output['name'] = self.name()

        for p in range(self.get_nb_input()):
            input_name = self.input_desc[p]['name']
            properties[input_name] = inputs[p]
        output['properties'] = properties
        return output,




