# -*- python -*-
#
#       OpenAlea.Core:
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       Distributed under the CeCILL v2 License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

""" import qt.py from IPython to set QString and QVariant

The goal is to have the same version of QString and QVariant in all OpenAlea
"""

from IPython.external.qt import *
# import sip
# sip.setapi('QString', 2)
# sip.setapi('QVariant', 2)