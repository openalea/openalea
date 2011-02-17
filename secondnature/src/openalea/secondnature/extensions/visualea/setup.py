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


setup( name = "Visualea Extension",
       version = "0.1",
       py_modules = ['visualeapg'],
       entry_points = {"openalea.app.document" : ["visualea.pm = visualeapg:pmanager"],
                       "openalea.app.layout":["visualea.df1 = visualeapg:df1",
                                              "visualea.df2 = visualeapg:df2"],
                       "openalea.app.widget_factory":["Visualea.oa = visualeapg:dataflow_f",
                                                      "Visualea.pmv = visualeapg:pmanager_f"],
#                       "openalea.ext":["Visualea = visualeapg.visualea"]
                       }
    )
