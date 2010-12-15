# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2010 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

__doc__ = """ A node that morphs its inputs according to a userèchosen method of the input object. """
__revision__ = " $Id$ "

from openalea.core.node import Node
from openalea.core.signature import Signature
import inspect
import re

class SelectCallable(Node):
    def __init__(self, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)
        self.internal_data["methodName"] = None
        self.internal_data["methodSig"]  = None
        self.add_output(name='func_result')

    def __call__(self, inputs):
        instance = inputs[0]
        methodName = self.internal_data.get("methodName")
        if methodName is not None:
            return getattr(inputs[0], methodName)(*inputs[1:]),

    def _init_internal_data(self, d):
        Node._init_internal_data(self, d)
        methodSig = d.get("methodSig")
        methodName = d.get("methodName")
        if methodSig:
            sig = Signature(methodSig)
            inputs = sig.get_all_parameters()
            self.set_caption(methodName)
            self.internal_data["methodName"] = methodName
            self.internal_data["methodSig"] = sig
            self.__doc__ = sig.get_doc()
            self.build_ports(inputs)

    def get_method_name(self):
        return self.internal_data["methodName"]

    def set_method_name(self, name):
        instance = self.get_input(0)
        if instance and name:
            meth = getattr(instance, name, None)
            if meth:
                sig = Signature(meth)
                inputs = sig.get_all_parameters()
                prefix = str(instance)
                if len(prefix)>15:
                    prefix = prefix[:5]+"..."+prefix[-5:]
                self.set_caption(prefix+" : "+name)
                self.internal_data["methodName"] = name
                self.internal_data["methodSig"] = sig
                self.__doc__ = sig.get_doc()
                self.build_ports(inputs)

    def discard_method_name(self):
        self.internal_data["methodName"] = None
        self.__validMethArgs = False
        self.build_ports([])
        self.set_caption("select callable")

    def build_ports(self, inputs):
        inputDescs = []

        # -- the first input is always the instance : we save it --
        instance = self.inputs[0]
        inputDescs.append( self.input_desc[0] )

        # -- save the output desc --
        outputDescs = self.output_desc[:]

        # -- the old dataflow ports have to be deleted --
        if self._composite_node : #can we get access to the dataflow through this proxy?
            cnode = self._composite_node
            for input in self.input_desc[1:]:
                gpid = cnode.in_port(self.get_id(), input.get_id())
                cnode.remove_port(gpid)

        # -- now we can safely clean the inputs (to rebuild them later, of course) --
        self.clear_inputs()
        self.clear_outputs()

        # -- create the descriptions for other inputs --
        inputDescs.extend(inputs)

        # -- rebuild ourselves --
        self.set_io(inputDescs, outputDescs)
        self.set_input("object", instance, False)

        # -- update dataflow structure with new input ports --
        if self._composite_node : #can we get access to the dataflow through this proxy?
            cnode = self._composite_node
            for input in self.input_desc[1:]:
                cnode.add_in_port(self.get_id(), input.get_id())

        # -- finally transfer listeners so that GUIs update correctly --
        inputDescs[0].transfer_listeners(self.input_desc[0])

