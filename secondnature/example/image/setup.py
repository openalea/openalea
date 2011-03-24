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


setup( # -- OAEX Prefix to easily locate packages that are SecondNature extensions --
       name         = "OAEX Image",
       version      = "0.1",
       # -- Tell setuptools to install image_ext.py: --
       py_modules   = ['image_ext'],
       # -- Add values to the openalea.app.applet_factory entry point --
       entry_points = {"openalea.app.applet_factory": ["ImageViewer.f = image_ext:ImageViewerFactory"],
                       }
    )
