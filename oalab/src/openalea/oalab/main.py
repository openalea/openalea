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
from openalea.oalab.cli.parser import CommandLineParser
from openalea.oalab.project.symlink import create_project_shortcut
from openalea.oalab.gui.session import Session

def main():
    """
    OpenAleaLaboratory starts here
    """
    # Create shortcut in project dir to oalab.share dir (only if necessary)
    create_project_shortcut()
    # Launch app
    
    #session = Session()
    #cli = CommandLineParser(sys.argv)

    app = OALab(sys.argv)
    app.exec_()
    
def main_plantlab():
    """
    OpenAleaLaboratory starts here
    """
    # Create shortcut in project dir to oalab.share dir (only if necessary)
    create_project_shortcut()
    # Launch app
    app = OALab(["-e", "plant"])
    app.exec_()
    
def main_tissuelab():
    """
    OpenAleaLaboratory starts here
    """
    # Create shortcut in project dir to oalab.share dir (only if necessary)
    create_project_shortcut()
    # Launch app
    app = OALab(["-e", "tissue"])
    app.exec_()
    
def main_3dlab():
    """
    OpenAleaLaboratory starts here
    """
    # Create shortcut in project dir to oalab.share dir (only if necessary)
    create_project_shortcut()
    # Launch app
    app = OALab(["-e", "3d"])
    app.exec_()
    
def main_minilab():
    """
    OpenAleaLaboratory starts here
    """
    # Create shortcut in project dir to oalab.share dir (only if necessary)
    create_project_shortcut()
    # Launch app
    app = OALab(["-e", "mini"])
    app.exec_()

    
if( __name__ == "__main__"):
    main()
