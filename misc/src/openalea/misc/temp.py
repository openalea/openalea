# -*- python -*-
#
#       A module to handle temporary file names
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Daniel BARBEAU <daniel.barbeau@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#       http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__license__ = "CeCILL v2"
__revision__ = " $Id$ "


import tempfile

def temp_name(suffix):
    f = tempfile.NamedTemporaryFile(suffix=suffix)
    name = f.name
    f.close()
    return name
