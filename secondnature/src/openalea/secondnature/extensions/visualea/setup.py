# -*- python -*-
#
#       OpenAlea.SecondNature
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

__license__ = "CeCILL v2"
__revision__ = " $Id$ "


from setuptools import setup


setup( name         = "OAEX Visualea",
       version      = "0.1",
       py_modules   = ['visualea_ext'],
       entry_points = {"openalea.app.layout":["visualea.df1 = visualea_ext:df1"],
                       "openalea.app.applet_factory": ["Visualea.oa = visualea_ext:DataflowViewFactory"],
                       }
    )
