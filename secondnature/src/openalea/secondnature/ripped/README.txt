# -*- README -*-
#
#       OpenAlea.Secondnature
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

This directory contains modules ripped away from openalea.visualea because they needed tweaks to work
properly out of the visualea context. The idea is that a good refactoring of the original files
will eliminate the need for ripped out modules!

- node_treeview.py : some classes require a reference to visualea's mainwindow. Remove that dependency!
