# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
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
__revision__ = "$Id: $"

from openalea.vpltk.qt import QtGui
from openalea.oalab.service.control import control, edit_qt


if __name__ == '__main__':


    app = QtGui.QApplication([])


    # Automatic approach
    ####################
    a = 5
    c1 = control(a)

    # Manual approach
    #################
    from openalea.oalab.control.control import  Control
    from openalea.oalab.service.control import IColorList
    c2 = Control(IColorList)

    # customizations (optional)
    ###########################
    c1.name = 'nmax'
    c1.set_value(a)

    # Edition
    #########
    w1 = edit_qt(c1)
    w1b = edit_qt(c1)
    w2 = edit_qt(c2)

    app.exec_()

#     print '1. input value: %s, final value: %s, widget value: %s' % (a, c1.value(), w1.value())
#    print '2. input value: %s, final value: %s, widget value: %s' % (a, c2.value(), w2.value())
