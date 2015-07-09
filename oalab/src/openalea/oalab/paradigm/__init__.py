# -*- python -*-
#
#       OpenAlea.OALab
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
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


class IModelController(object):

    """
    """

    default_name = unicode
    default_file_name = unicode
    pattern = unicode
    extension = unicode
    mimetype = unicode
    icon = unicode

    def __init__(self, **kwds):
        """
        Possible keywords:
            - model: object derivating from Model and matching mimetype
            - data: object derivating from Data and matching mimetype
            - code/content: content
            - filepath: data path (filename and name are mutually exclusive)
            - name: model name (filename and name are mutually exclusive)
            - parent: Qt parent, used only by instantiate_widget widget

        If nothing is passed, an empty Model will be created
        """
        pass

    def instantiate_widget(self):
        """
        Create an editor for obj

        :return: the instantiated widget
        """

    def execute(self):
        """
        Get selected part in editor an run it.
        """

    def run(self, *args, **kwargs):
        """
        """

    def step(self, *args, **kwargs):
        """
        """

    def stop(self, *args, **kwargs):
        """
        """

    def animate(self, *args, **kwargs):
        """
        """

    def init(self, *args, **kwargs):
        """
        """

    def sync(self):
        """
        Synchronize editor with data/model
        """

    def widget(self):
        """
        :return: the edition widget
        """
        return self._widget
