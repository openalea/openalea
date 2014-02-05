# -*- python -*-
#
#       OALab start here
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
from openalea.oalab.project.symlink import create_project_shortcut

def main():
    """
    OpenAleaLaboratory starts here
    """
    # Create shortcut in project dir to oalab.share dir (only if necessary)
    create_project_shortcut()
    # Launch app
    app = OALab(sys.argv)
    app.exec_()

    
if( __name__ == "__main__"):
    main()
