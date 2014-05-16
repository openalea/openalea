# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
import collections

class Model(object):
    default_name = ""
    default_file_name = ""
    pattern = ""
    extension = ""
    icon = ""
    
    def __init__(self, name="", code="", inputs=[], outputs=[]):
        """
        :param name: name of the model (name of the file?)
        :param code: code of the model, can be a string or an other object
        :param inputs: list of identifier of inputs that come from outside model (from world for example)
        :param outputs: list of objects to return outside model (to world for example)
        """
        self.name = name
        self.code = code
        self.inputs_info = inputs
        self.outputs_info = outputs
        self._inputs = []
        self._outputs = []

    def repr_code(self):
        """
        :return: a string representation of model to save it on disk
        """
        pass

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        """
        execute model
        """
        pass

    def reset(self, *args, **kwargs):
        """
        go back to initial step
        """
        pass

    def step(self, *args, **kwargs):
        """
        execute only one step of the model
        """
        pass

    def stop(self, *args, **kwargs):
        """
        stop execution
        """
        pass

    def animate(self, *args, **kwargs):
        """
        run model step by step
        """
        pass

    @property
    def inputs(self):
        """
        List of inputs of the model.

        :use:
            >>> model.inputs = 4, 3
            >>> model.run()
        """
        return self._inputs

    @inputs.setter
    def inputs(self, *args):
        self._inputs = dict()
        if args:
            inputs = args[0]
            if not isinstance(inputs, list):
                if isinstance(inputs, collections.Iterable):
                    inputs = list(inputs)
                else:
                    inputs = [inputs]
            if isinstance(inputs[0], list):
                inputs = inputs[0]
            inputs.reverse()

            for input_info in self.inputs_info:
                if len(inputs):
                    inp = inputs.pop()
                elif input_info.default:
                    inp = eval(input_info.default)
                else:
                    raise Exception("Model %s have inputs not setted. Please set %s ." %(self.name,input_info.name))
                self._inputs[input_info.name] = inp

    @property
    def outputs(self):
        """
        Return outputs of the model after running it.

        :use:
            >>> model.run()
            >>> print model.outputs
        """
        return self._outputs

    @outputs.setter
    def outputs(self, outputs=[]):
        self._outputs = outputs