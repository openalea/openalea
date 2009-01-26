# -*- coding: utf-8 -*-
"""
Module implementing the view of the packages.

Visible attributes are : loaded or not. Loading a package will be done using a dropdown menu.

Inside load packages, we show the components and widgets available from this package.

:author: Barbier de Reuille Pierre, Donès Nicolas, Florence Chaubert
:version: 0.1
:since: 08/11/2005
"""
import sys
from PyQt4 import QtCore, QtGui
from alea.kernel import package

loaded_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x10\x00\x00\x00\x10" \
    "\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\x00\x00\x00" \
    "\x21\x49\x44\x41\x54\x38\x8d\x63\x60\x18\xf2\x80" \
    "\x11\x85\xf7\x9f\xe1\x3f\x91\xba\xe0\xfa\x98\x28" \
    "\x75\xc1\xa8\x01\xa3\x06\x0c\x13\x00\x00\xa7\xf7" \
    "\x02\x14\x5e\x1f\xbe\x42\x00\x00\x00\x00\x49\x45" \
    "\x4e\x44\xae\x42\x60\x82"

notloaded_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x10\x00\x00\x00\x10" \
    "\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\x00\x00\x00" \
    "\x22\x49\x44\x41\x54\x38\x8d\x63\x60\x18\xf2\x80" \
    "\x11\x99\xf3\x9f\x81\xe1\x3f\x91\x9a\xe0\xfa\x98" \
    "\x28\x75\xc1\xa8\x01\xa3\x06\x0c\x13\x00\x00\xa8" \
    "\xf7\x02\x14\xa2\x8e\x85\x45\x00\x00\x00\x00\x49" \
    "\x45\x4e\x44\xae\x42\x60\x82"



class PkgExplorer( QtGui.QListWidget ):
  def __init__( self, parent = None, name = "", fl = 0 ):
    QtGui.QListWidget.__init__( self, parent, name, fl )
    '''self.col_name = self.addColumn( "Name" )
    self.col_installed = self.addColumn( " " )
    self.col_loaded = self.addColumn( " " )
    self.col_desc = self.addColumn( "Description" )
    self.col_sysname = self.addColumn( "System name" )'''
    self.loaded_pixmap = QtGui.QPixmap()
    self.loaded_pixmap.loadFromData( loaded_data, "PNG" )
    self.notloaded_pixmap = QtGui.QPixmap()
    self.notloaded_pixmap.loadFromData( notloaded_data, "PNG" )
    self.setRootIsDecorated( True )
    self.fill()

  def fill( self ):
    pm = package.load()
    for p in pm.packages():
      self.add_package( p )

  def add_package( self, pkg ):
    i = QtGui.QListWidgetItem( self )
    i.setText( self.col_name, pkg.name )
    i.setText( self.col_desc, pkg.description )
    i.setText( self.col_sysname, pkg.sys_name )
    if pkg.is_loaded:
      i.setIcon(QtGui.QIcon(self.loaded_pixmap))
      #i.setPixmap( self.col_loaded, self.loaded_pixmap )
      enabled = True
    else:
      i.setPixmap( self.col_loaded, self.notloaded_pixmap )
      enabled = False
    if pkg.is_installed:
      i.setText( self.col_installed, "+" )
    else:
      i.setText( self.col_installed, "-" )
    for c in pkg.components:
      cli = qt.QListViewItem( i, c )
      cli.setEnabled( enabled )


