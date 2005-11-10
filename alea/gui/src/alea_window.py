# -*- coding: utf-8 -*-
"""
Module implementing the main window of the ALEA application.

:author: Barbier de Reuille Pierre, Dones Nicolas
:version: 0.1
:since: 08/11/2005
"""

from alea_base_window import BaseWnd
from pyCute import PyCute
import qt
import sys
from pkg_explorer import PkgExplorer
from alea_workspace import WSCanvas

DEBUG_INOUT = True

class RedirectWriteFile( object ):
  def __init__( self, embed, log ):
    self.log = log
    self.embed = embed
  def write( self, text ):
    self.log.write( text )
    self.embed.write( text )
  def __getattr__( self, attr ):
    if attr not in [ "log", "embed", "write" ]:
      return getattr( self.embed, attr )
    else:
      return object.__getattr__( self, attr )
  def __setattr__( self, attr, value ):
    if attr not in [ "log", "embed" ]:
      return setattr( self.embed, attr, value )
    else:
      return object.__setattr__( self, attr, value )

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

    # Fill the package tabs
    eframe = self.explore_frame.page( 0 )
    self.pkg_explore = PkgExplorer(eframe, name = "Package Explorer")
    eframe.layout().add( self.pkg_explore )

    # Fill the objects tabs

    # Fill the file system tabs

    # Fill the workspace with an empty one
    wframe = self.workspaces.page( 0 )
    self.wscanvas = WSCanvas( wframe, name = "WSCanvas" )
    self.workspace_layout = qt.QHBoxLayout( wframe )
    self.workspace_layout.add( self.wscanvas )

    # Inserting pyCute shell
    self.shell_layout = qt.QHBoxLayout( self.shell_frame )
    self.shell = PyCute(parent=self.shell_frame)
    self.shell_layout.add( self.shell )

    # DEBUG
    if DEBUG_INOUT:
      self.stderr = file( "log_err.txt", "w" )
      self.stdout = file( "log_out.txt", "w" )

      sys.stderr = RedirectWriteFile( sys.stderr, self.stderr )
      sys.stdout = RedirectWriteFile( sys.stdout, self.stdout )

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
    app=qt.QApplication(sys.argv)
    w=AleaWnd()
    app.setMainWidget(w)
    w.show()
    app.exec_loop()

