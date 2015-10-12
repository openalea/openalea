# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2015 INRIA - CIRAD - INRA
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


"""
========================
OpenAleaLab's extensions
========================


Create a new lab is very easy.
First, launch openalelab with ipython lab, pass in "Edit layout" and customize your interface. Once satisfied, quit openalealab.
Copy content of file $HOME/.openalea/ipython.oaui in a file.
Replace **null** with **None**, **false** with **False** and **true** with **True** to obtain a "python layout".



Copy paste this sample:

.. literalinclude:: ../../../../../openalea/oalab/src/openalea/oalab/plugin/lab.py
    :linenos:
    :pyobject: ILab

And replace "{'children': {}, 'parents': {}, 'properties': {}}" with the "python layout"

Details
=======

"""

from openalea.oalab.plugin.builtin.lab.default import DefaultLab


class ILab(object):
    name = 'mylab'
    icon = 'icon_mylab.png'
    label = 'My Lab'

    connections = []
    layout = {'children': {}, 'parents': {}, 'properties': {}}
