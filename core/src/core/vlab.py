# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2008 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe pradal at cirad fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

import os, sys
import re
from openalea.core.path import path
from openalea.core.pkgmanager import PackageManager
from openalea.core.compositenode import CompositeNodeFactory, CompositeNode

def vlab_object(directory):
    """
    Create an openalea package from a vlab object.
    First, read the specification file and parse it.
    Create the list of data, the list of editors, 
    and the list of programs.
    Build the graph of dependencies.
    Compute the layout of the graph. 
    Create a package with data and a composite node.
    
    """
    directory = path(directory)
    return

# Factories to build nodes from vlab components.
# A component may be a data, an editor or a program.
# The difference between an editor and a program is that
# an editor have the same output value than its input,
# and a program may have many inputs but unknow outputs.
def data(name):
    return

def editor(command):
    return

def program(command):
    return


class VlabObject(object):
    """
    A vlab object is a directory containing a specification file,
    and a set of data.
    """
    text = ['TEXT','HINTS']
    editors = ['MAP', 'loadmap', 'savemap', 'EDIT', 'SURFACE', 
               'bezieredit','PALETTE', 'palette', 'MEDIT', 'medit',
               'GALLERY', 'gallery', 'EDIT']
    programs = ['cpfg', 'lpfg']
    ignore = [';', '#']
    name2program = {'MAP' : 'loadmap',
                'SURFACE' : 'bezieredit',
                'PALETTE' : 'palette',
                'MEDIT' : 'medit',
                'GALLERY' : 'gallery'}

    def __init__(self, directory):
        self.dir = directory
        self._programs = []
        self._files = {}
        self._text = {}
        self._editors = {}

    def read_specification(self):
        spec = self.dir / 'specifications'

        f = spec.open()
        # start the package manager
        self.pm = PackageManager()
        self.pm.init(verbose=False)
        self.sg = CompositeNode()
        self.sgfactory = CompositeNodeFactory(self.dir.basename())

        self.read_files(f)
        self.read_commands(f)
        self.process_files()
        self.build_graph()

        f.close()

    def read_files(self, f):
        pattern ='\w+\.\w+'
        for l in f:
            if 'ignore:' in l:
                break
            fn = l.strip()
            if re.match(pattern,fn):
                self._files[fn]=None

    def read_commands(self, f):
        pattern = '\t*[a-zA-Z0-9_ \\-]+:\\s*$'
        menus = []
        for l in f:
            if re.match(pattern, l):
                level = l.rstrip().count('\t')
                menu = l.strip()[:-1]
                if len(menus) <= level:
                    menus.append(menu)
                else:
                    menus[level] = menu
                    menus = menus[:level+1]
                continue

            # skip ignore files : logic no menus have been created.
            if not menus:
                continue
            cmd = l.strip()
            if cmd:
                self._process_command('.'.join(menus), cmd)

    def process_command(self, name, cmd):
        command = cmd.split()
        prog = command[0]
        command[0] = name2program.get(prog,prog)
        if prog in self.programs:
            self.process_program(name, command)
        elif prog in self.editors:
            self.process_editor(name, command)
        elif prog in self.text:
            self.process_text(name, command)
        else: 
            print 'Do not know how to process this command: %s'%cmd

    def process_program(self, name, command):
        """ Build a process node from the command.
        """
        node = self.pm.get_node("vlab","process")
        node.set_input(1,' '.join(command))
        prog_node = self.sg.add_node(node)
        self._programs.append(prog_node)

    def process_editor(self, name, command):
        """
        Find the file on which the editor works on.
        """
        fn = command[-1]
        cmd = ' '.join(command)
        if fn not in self._files.keys():
            print "WARNING: the file %s used by the editor %s in not in the specification file." %(fn, cmd)
        prog = command[0]
        if prog != 'EDIT':
            node = self.pm.get_node("vlab", "editor")
            node.set_input(1,cmd)
        else:
            node = self.pm.get_node("vlab", "text editor")
        # TODO : replace this entry by a data object
        filename = self.dir / fn
        node.set_input(0,filename)

        edit_node = self.sg.add_node(node)
        self._editors.setdefault(fn,[]).append(edit_node)

    def process_text(self, name, command):
        node = self.pm.get_node('catalog.file', 'viewfile')
        text_node = self.sg.add_node(node)
        self._text.setdefault(command[-1], []).append(text_node)

    def process_files(self):
        deps = self._files
        files = deps.keys()
        for f in files:
            fn = self.dir/f
            if fn.ext in ['.map', '.txt', '.s']: 
                continue #binary file or other
            print "Search dependencies in %s"%f
            deps[f] = search(fn, files)
            
        self._filenodes = {}
        for f in files:
            # TODO: Create data rather than files
            node = self.pm.get_node("vlab", "vlab file stamp")
            node.set_input(1,f)
            fnode = self.sg.add_node(node)
            self._filenodes[f] = fnode

    def build_graph(self):
        """
        Specify connections between nodes.
        """
        for p in self._programs:
            pass
            
        

def search (file, filenames):
    """
    Returns the filenames that are referenced in a file.
    """
    f = open(file)
    text = f.read()
    f.close()
    l = filter(lambda x: ' '+x+' ' in text, filenames)
    return l
    
# TESTS
def test():
    spec = path('specifications')
    f = open(spec)
    p1 = '\w+\.\w+'
    p2 = '\t*[a-zA-Z0-9_ \\-]+:\\s*$'
    menus = []
    for l in f:
        if 'ignore:' in l:
            break
        fn = l.strip()
        if re.match(p1,fn):
            print fn
    for l in f:
        if re.match(pattern, l):
            level = l.rstrip().count('\t')
            menu = l.strip()[:-1]
            if len(menus) <= level:
                menus.append(menu)
            else:
                menus[level] = menu
                menus = menus[:level+1]
            continue
        if not menus:
            continue
        cmd = l.strip()
        if cmd:
            test_process_command('.'.join(menus), cmd)
    f.close()
def test_process_command(name, cmd):
        command = cmd.split()
        prog = command[0]
        command[0] = name2program.get(prog,prog)
        if prog in programs:
            print 'Program %s'%(' '.join(command))
            #self.process_program(name, command)
        elif prog in editors:
            print 'Editor %s'%(' '.join(command))
            #self.process_editor(name, command)
        elif prog in text:
            print 'Text %s'%(' '.join(command))
            #self.process_text(name, command)
        else: 
            print 'Do not know how to process this command: %s'%cmd
"""
text = ['TEXT','HINTS', 'EDIT']
editors = ['MAP', 'loadmap', 'savemap', 'EDIT', 'SURFACE', 
        'bezieredit','PALETTE', 'palette', 'MEDIT', 'medit',
        'GALLERY', 'gallery']
programs = ['cpfg', 'lpfg']
ignore = [';', '#']
name2program = {'MAP' : 'loadmap',
                'SURFACE' : 'bezieredit',
                'PALETTE' : 'palette',
                'MEDIT' : 'medit',
                'GALLERY' : 'gallery'}
"""
