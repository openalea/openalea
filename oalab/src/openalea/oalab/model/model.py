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
    default_name = ""
    default_file_name = ""
    pattern = ""
    extension = ""
    icon = ""
    
    def __init__(self, name, code="", inputs=[], outputs=[]):
        """
        :param name: name of the model (name of the file?)
        :param code: code of the model, can be a string or an other object
        :param inputs: list of identifier of inputs that come from outside model (from world for example)
        :param outputs: list of objects to return outside model (to world for example)
        """
        # TODO: how to manage time?
        self.name = name
        self.code = code
        self.inputs = inputs
        self.outputs = outputs

    def repr_code(self):
        """
        :return: a string representation of model to save it on disk
        """
        pass

    def run(self, interpreter):
        """
        execute model
        """
        pass

    def reset(self, interpreter):
        """
        go back to initial step
        """
        pass

    def step(self, interpreter):
        """
        execute only one step of the model
        """
        pass

    def stop(self, interpreter):
        """
        stop execution
        """
        pass

    def animate(self, interpreter):
        """
        run model step by step
        """
        pass

