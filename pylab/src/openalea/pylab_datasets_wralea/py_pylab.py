###############################################################################
# -*- python -*-
#
#       amlPy function implementation
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__doc__="""Simple data sets to play with openalea.pylab"""

__license__= "Cecill-C"
__revision__=" $Id$ "

#//////////////////////////////////////////////////////////////////////////////


from openalea.core import Node
from openalea.core import Factory, IFileStr, IInt, IBool, IFloat, \
    ISequence, IEnumStr, IStr, IDirStr, ITuple3, IDict


class PyLabBivariateNormal(Node):
    def __init__(self):
        import numpy as np
        Node.__init__(self)
        delta = 0.025
        self.add_input(name='X', interface=ISequence, value=np.arange(-3, 3, delta))
        self.add_input(name='Y', interface=ISequence, value=np.arange(-3, 3, delta))
        self.add_output(name='Z', interface=ISequence, value=[])

    def __call__(self, inputs):
        from matplotlib.mlab import bivariate_normal
        X = self.get_input('X')
        Y = self.get_input('Y')
        Z1 = bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
        Z2 = bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
        # difference of Gaussians
        Z = 10.0 * (Z2 - Z1)

        return Z

