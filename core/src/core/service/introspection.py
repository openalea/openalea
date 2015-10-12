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


def name(obj):
    if hasattr(obj, 'name'):
        return obj.name
    elif hasattr(obj, '__class__'):
        return obj.__class__.__name__
    elif hasattr(obj, '__name__'):
        return obj.__name__
    else:
        return str(obj)


def label(obj):
    if hasattr(obj, '__label__'):
        return obj.__label__
    elif hasattr(obj, 'label'):
        return obj.label
    else:
        return str(name(obj)).capitalize()
