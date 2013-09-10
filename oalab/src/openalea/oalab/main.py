# -*- python -*-
#
#       VPlantsLab start here
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

import sys
from openalea.oalab.gui.app import OALab

def main():
    """
    VirtualPlantsLaboratory starts here
    """
    app = OALab(sys.argv)
    app.exec_()

    
if( __name__ == "__main__"):
    main()
