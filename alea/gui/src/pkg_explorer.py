# -*- coding: utf-8 -*-
"""
Module implementing the view of the packages.

Visible attributes are : loaded or not. Loading a package will be done using a dropdown menu.

Inside load packages, we show the components and widgets available from this package.

:author: Barbier de Reuille Pierre, Donès Nicolas
:version: 0.1
:since: 08/11/2005
"""
import qt
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

class PkgExplorer( qt.QListView ):
  def __init__( self, parent = None, name = "", fl = 0 ):
    qt.QListView.__init__( self, parent, name, fl )
    self.addColumn( "Name" )
    self.addColumn( "Description" )
    self.addColumn( "System name" )
    self.loaded_pixmap = qt.QPixmap()
    self.loaded_pixmap.loadFromData( loaded_data, "PNG" )
    self.notloaded_pixmap = qt.QPixmap()
    self.notloaded_pixmap.loadFromData( notloaded_data, "PNG" )
    self.fill()

  def fill( self ):
    pm = package.load()
    for p in pm.packages():
      self.add_package( self, p )

  def add_package( self, pkg ):
    if pkg.is_installed:
      name = pkg.name
    else:
      name = "*"+pkg.name
    i = qt.QListViewItem( self, name, pkg.description, pkg.sys_name )
    if pkg.loaded():
      i.setPixmap( 0, self.loaded_pixmap )
      enabled = True
    else:
      i.setPixmap( 0, self.notloaded_pixmap )
      enabled = False
    comp = qt.QListViewItem( i, "components" )
    comp.setEnabled( enabled )
    for c in pkg.components:
      cli = qt.QListViewItem( comp, c )
      cli.setEnabled( enabled )
    if pkg.is_gui:
      inter = qt.QListViewItem( i, "widgets" )
      inter.setEnabled( enabled )
      for c in pkg.interfaces:
        cli = qt.QListViewItem( inter, c )
        cli.setEnabled( enabled )


