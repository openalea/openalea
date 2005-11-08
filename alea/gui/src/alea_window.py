# -*- coding: utf-8 -*-
"""
Module implementing the main window of the ALEA application.

:author: Barbier de Reuille Pierre, Donès Nicolas
:version: 0.1
:since: 08/11/2005
"""

from alea_base_window import BaseWnd
from pyCute import PyCute
import qt
from sys import argv
from pkg_explorer import PkgExplorer

class AleaWnd( BaseWnd ):
  """
  Main ALEA window.

  :IVariables:
    - `shell_layout`: layout used to include the Python shell
    - `shell`: instance of a graphical Python shell

  :Types:
    - `shell_layout`: qt.QHBoxLayout
    - `shell`: PyCute
  """
  def __init__( self ):
    """
    Initialization of the window.

    Instanciate the graphical shell, and fill the explore tabs.
    """
    BaseWnd.__init__( self )

    # Inserting pyCute shell
    self.shell_layout = qt.QHBoxLayout( self.shell_frame )
    self.shell = PyCute(parent=self.shell_frame)
    self.shell_layout.add( self.shell )

    # Fill the package tabs
#    eframe = self.explore_frame.page( 0 )
#    self.pkg_explore = PkgExplorer(self.explore_frame.page( 0 ), name = "Package Explorer")
#    self.eframe.layout.add( self.pkg_explore )

    # Fill the objects tabs

    # Fill the file system tabs

  def fileExit( self ):
    """
    Method called before closing the main window ( and thus the application ).
    """
    self.close()

  def fileOpen( self ):
    """
    Method opening a stored ALEA worskpace.
    """
    pass

  def fileSave( self ):
    """
    Save the current ALEA workspace.
    """
    pass

  def fileSaveHistory( self ):
    """
    Save the content of the shell history into a Python file.
    """
    #dlg = qt.QFileDialog()
    pass

  def fileOpenHistory( self ):
    """
    Load the content of a python file into the current shell.

    :Warning: Empty lines are meaningful ( as in an interactive Python shell )
    """
    pass

if __name__ == "__main__":
    app=qt.QApplication(argv)
    w=AleaWnd()
    app.setMainWidget(w)
    w.show()
    app.exec_loop()

