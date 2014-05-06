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


class Model(object):
    def __init__(self, code="", inputs=[], outputs=[]):
        """
        :param code: code of the model, can be a string or whatever object
        :param inputs: list of identifier of inputs that come from outside model (from world for example)
        :param outputs: list of objects to return outside model (to world for example)
        """
        # TODO: how to manage time?
        self.code = code
        self.inputs = inputs
        self.outputs = outputs

    def get_code(self):
        """
        :return: a string representation of model to save it
        """
        pass

    def run(self):
        """
        execute model
        """
        pass

    def reset(self):
        """
        go back to intial step
        """
        pass

    def step(self):
        """
        execute only one step of the model
        """
        pass

    def stop(self):
        """
        stop execution
        """
        pass

    def animate(self):
        """
        run model step by step
        """
        pass

