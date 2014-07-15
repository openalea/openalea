"""
Package that provides a unique qt widget for matplotlib figure

To get pyplot actions redirected to this widget, use::

    from openalea.oalab import matplotlib as oampl
    oampl.activate_in_pyplot()
    
To disable it, do::

    from openalea.oalab import matplotlib as oampl
    oampl.desactivate_in_pyplot()


#########################################################
#   OpenAlea.OALab.matplotlib: matplotlib in OpenAleaLab
#   
#   Copyright 2013 INRIA - CIRAD - INRA
#   
#   File author(s): Julien Diener <julien.diener@inria.fr>
#   
#   File contributor(s):
#   
#   Distributed under the Cecill-C License.
#   See accompanying file LICENSE.txt or copy at
#       http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#   
#   OpenAlea WebSite : http://openalea.gforge.inria.fr
#########################################################
"""
from __future__ import absolute_import

__revision__ = "0.1"

# to save mpl function to replace
_origin_new_figure_manager = None


def activate_in_pyplot():
    """ redirect pyplot to TabWidget """
    import matplotlib.backends.backend_qt4agg as _qt4agg
    from .widget import new_figure_manager_given_figure
    
    global _origin_new_figure_manager
    _origin_new_figure_manager = _qt4agg.new_figure_manager_given_figure
    _qt4agg.new_figure_manager_given_figure = new_figure_manager_given_figure

def desactivate_in_pyplot():
    """ desibal pyplot redirection """
    import matplotlib.backends.backend_qt4agg as _qt4agg
    
    global _origin_new_figure_manager
    if _origin_new_figure_manager is not None:
        _qt4agg.new_figure_manager_given_figure = _origin_new_figure_manager


