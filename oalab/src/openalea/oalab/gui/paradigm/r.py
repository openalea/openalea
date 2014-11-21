# -*- python -*-
#
#       R Manager applet
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#                       Christophe Pradal <christophe.pradal@inria.fr>
#                       Christian Fournier <christophe.fournier@inria.fr>
#                       Guillaume Baty <guillaume.baty@inria.fr>
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
__revision__ = ""


from openalea.oalab.model.r import RModel, RFile
from openalea.oalab.gui.paradigm.python import PythonModelController


class RModelController(PythonModelController):
    default_name = RModel.default_name
    default_file_name = RModel.default_file_name
    pattern = RModel.pattern
    extension = RModel.extension
    icon = RModel.icon
    mimetype_data = RFile.mimetype
    mimetype_model = RModel.mimetype

    def execute(self):
        if self._widget:
            code = self._widget.get_selected_text()
            code = "\%\%R\n" + code
            return self.model.execute(code)
