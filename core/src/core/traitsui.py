# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Szymon Stoma <szymon.stoma@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""View for organizing the component lookout."""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


class View(object):
    """Describes the layout of widget.

    <Long description of the class functionality.>
    """

    def __init__(self, *values, **kargs):
        """Basic constructor."""
        self.content = values
        self.layout = kargs.get("layout", "|")
        self.label=kargs.get("label", "")


class Item(object):
    """Describes the atom of View.

    <Long description of the class functionality.>
    """

    def __init__(self, name, **keys):
        """Basic constructor.
        """
        self.name = name
        self.show_label = keys.get("show_label", True)


class Group(object):
    """Describes the group for  View.

    <Long description of the class functionality.>
    """

    def __init__(self, label, *values, **keys):
        """Basic constructor.
        """
        self.content = values
        self.label = label
        self.layout = keys.get("layout", "|")
