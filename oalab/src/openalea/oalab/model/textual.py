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
from openalea.vpltk.model import Model


class TextualModel(Model):
    default_name = "Textual"
    default_file_name = ""
    pattern = ""
    extension = ""
    icon = ""
    mimetype = ""

    def repr_code(self):
        """
        :return: a string representation of model to save it on disk
        """
        return self.code

    def run(self, *args, **kwargs):
        """
        execute entire model
        """
        return None

    def init(self, *args, **kwargs):
        """
        go back to initial step
        """
        return None

    def step(self, i=None, *args, **kwargs):
        """
        execute only one step of the model
        """
        return None

    def stop(self, *args, **kwargs):
        """
        stop execution
        """
        return None

    def animate(self, *args, **kwargs):
        """
        run model step by step
        """
        return None
