# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
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


class SplitterApplet(object):
    icon = 'oxygen_view-split-top-bottom.png'
    name = 'SplitterApplet'
    alias = 'Splitter'

    def __call__(self):
        from openalea.oalab.gui.splittablewindow import SplitterApplet
        return SplitterApplet
