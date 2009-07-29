# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe pradal at cirad fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
############################################################################
"""doc todo"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


import os
import sys
import re
from random import randint
from openalea.core.path import path


def vlab_object(directory, pkgmanager):
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
    obj = VlabObject2(directory, pkgmanager)
    return obj

# Factories to build nodes from vlab components.
# A component may be a data, an editor or a program.
# The difference between an editor and a program is that
# an editor have the same output value than its input,
# and a program may have many inputs but unknow outputs.


class VlabFile(object):

    def __init__(self, name):
        self.name = name
        self.deps = []
        self.editors = {}


class VlabObject(object):
    """
    A vlab object is a directory containing a specification file,
    and a set of data.
    """
    text = ['TEXT', 'HINTS']
    editors = ['MAP', 'loadmap', 'savemap', 'EDIT', 'SURFACE',
               'bezieredit', 'PALETTE', 'palette', 'MEDIT', 'medit',
               'GALLERY', 'gallery', 'EDIT', 'funcedit', 'panel', 'CHAR']#panel
    programs = ['cpfg', 'lpfg']
    ignore = [';', '#']
    name2program = {'MAP': 'medit',
                'SURFACE': 'bezieredit',
                'PALETTE': 'palette',
                'MEDIT': 'medit',
                'GALLERY': 'gallery',
                'EDIT': 'edit',
                'CHAR': 'edit',
                'loadmap': 'palette'}

    def __init__(self, directory, pkgmanager):
        self.dir = directory
        print "Import into OpenAlea the %s directory"%self.dir.basename()
        self._programs = []
        self._files = {}
        self._text = {}
        self._editors = {}
        self.pm = pkgmanager
        self.sg = None
        self.sgfactory = None
        self.factories = []
        self._package = None

    def pkgname(self):
        names = []

        def search_name(d):
            name= d.name
            if name == 'ext':
                search_name(d.dirname())
            elif (d/'.id').isfile() or (d/'specifications').isfile():
                names.insert(0, name)
                search_name(d.dirname())
            else:
                return
        d = self.dir
        search_name(d)
        _pkgname = 'vlab.'+'.'.join(names)
        print _pkgname
        return 'vlab.'+'.'.join(names)

    def get_package(self):
        if not self._package:
            self.build_package()
        self._package.write()
        return self._package

    def build_package(self):
        from openalea.core.package import UserPackage
        # Build MetaData
        metainfo = dict(
            version = '',
            license = '',
            authors = '',
            institutes = '',
            description = '',
            url = '',
            )
        icons = self.dir.glob('icon.*')
        if len(icons) > 0:
            metainfo['icon'] = icons[0].basename()

        name = self.pkgname()
        self._package = UserPackage(name, metainfo, str(self.dir))

        if not self.sgfactory:
            self.read_specification()

        # Add factorie of the dataflow
        self._package.add_factory(self.sgfactory)
        #  Add data factories there
        #for f in self.factories:
        #    self._package.add_factory(f)

    def read_specification(self):
        spec = self.dir / 'specifications'
        from openalea.core.compositenode import CompositeNodeFactory
        from openalea.core.compositenode import CompositeNode

        f = spec.open()
        self.sg = CompositeNode()
        #name  = self.dir.basename().split('-')[-1]
        name = self.dir.basename()
        self.sgfactory = CompositeNodeFactory(name)

        self.read_files(f)
        self.read_commands(f)
        self.process_files()
        self.build_graph()

        f.close()

    def read_files(self, f):
        pattern ='\w+\.\w+'
        for l in f:
            if 'ignore:' in l or l is '*':
                break
            fn = l.strip()
            if ':' not in fn and re.match(pattern, fn):
                self._files[fn]=[]

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
                self.process_command('.'.join(menus), cmd)

    def process_command(self, name, cmd):
        command = cmd.split()
        prog = command[0]
        command[0] = self.name2program.get(prog, prog)
        if prog in self.programs:
            self.process_program(name, command)
        elif prog in self.editors:
            self.process_editor(name, command)
        elif prog in self.text:
            self.process_text(name, command)
        else:
            print 'Do not know how to process this command: %s' % cmd

    def process_program(self, name, command):
        """ Build a process node from the command.
        """
        node = self.pm.get_node("vlab.bin", "process")
        node.set_input(1, ' '.join(command))
        prog_node = self.sg.add_node(node)
        self._programs.append(prog_node)

    def process_editor(self, name, command):
        """
        Find the file on which the editor works on.
        """
        cmd = ' '.join(command)
        fn = ''
        if len(command) > 1:
            fn = command[-1]
            if fn not in self._files.keys():
                print "WARNING: the file %s used by the editor %s in not in the specification file." %(fn, cmd)
                return
                #self._files[fn] = []

        prog = command[0]
        if prog != 'EDIT':
            node = self.pm.get_node("vlab.bin", "editor")
            node.set_input(1, cmd)
            node.set_input(2, str(self.dir))
        else:
            node = self.pm.get_node("vlab.bin", "text editor")
            filename = self.dir/fn
            node.set_input(0, str(filename))

        edit_node = self.sg.add_node(node)
        self._editors.setdefault(fn, []).append(edit_node)

    def process_text(self, name, command):
        node = self.pm.get_node('catalog.file', 'viewfile')
        text_node = self.sg.add_node(node)
        filename = command[-1]
        self._text.setdefault(filename, []).append(text_node)

    def process_files(self):
        from openalea.core.data import DataFactory
        deps = self._files
        files = deps.keys()
        for f in files:
            fn = self.dir/f
            if fn.ext in ['.map', '.txt', '.s', '.e', '.rgb']:
                continue #binary file or other
            deps[f] = search(fn, files)

        self._filenodes = {}
        for f in files:
            factory = DataFactory(f)
            factory.package = self._package
            self.factories.append(factory)

            node = self.pm.get_node("vlab.bin", "vlab file stamp")
            node.set_input(1, str(self.dir/f))
            fnode = self.sg.add_node(node)
            self._filenodes[f] = fnode

    def build_graph(self):
        """
        Specify connections between nodes.
        """
        prog_deps = []
        files = self._files.keys()
        for p in self._programs:
            cmd = self.sg.node(p).inputs[1].split()
            fdeps = [f for f in files if f in cmd]
            for f in fdeps:
                fnode = self._filenodes[f]
                self.sg.connect(fnode, 0, p, 0)
        for f in files:
            for fdep in self._files[f]:
                depnode = self._filenodes[fdep]
                node = self._filenodes[f]
                self.sg.connect(depnode, 0, node, 0)
        for f, nodes in self._editors.iteritems():
            if not f: # an editor can act withouot a file
                continue
            fnode = self._filenodes[f]
            for node in nodes:
                self.sg.connect(node, 0, fnode, 0)
        for f, nodes in self._text.iteritems():
            fnode = self._filenodes[f]
            for node in nodes:
                self.sg.connect(fnode, 0, node, 0)
        layout(self)
        self.sg.to_factory(self.sgfactory)


def search(file, filenames):
    """
    Returns the filenames that are referenced in a file.
    """
    f = open(file)
    text = f.read()
    f.close()
    l = [fn for fn in filenames if fn != file and (' %s '%fn in text)]
    return l


def random_layout(obj):
    sg = obj.sg
    size = 600
    for vid in sg:
        x, y = randint(0, size), randint(0, size)
        data = sg.node(vid).internal_data
        data['posx'] = x
        data['posy'] = y

min_dx = 100
size=(800, 250)


def layout(obj):
    # compute a layout of the graph
    size = 500
    sg= obj.sg
    dy = 80
    y = 250
    progs = obj._programs
    n = len(progs)+1
    dx = x = size / n
    dx = max(min_dx, dx)
    for vid in progs:
        data = sg.node(vid).internal_data
        data['posx'] = x
        data['posy'] = y
        x+= dx

    size = size/n
    for vid in obj._programs:
        l = list(sg.in_neighbors(vid))
        if not l:
            continue
        n1 = sg.node(vid)
        x0, y0 = n1.internal_data['posx'], n1.internal_data['posy']
        dx1 = max(min_dx, size/(2*len(l)+1))
        y1 = y0 - dy
        x1 = x0 - size/2
        for node_id in l:
            data = sg.node(node_id).internal_data
            data['posx'] = x1
            data['posy'] = y1
            x1 += dx1
            compute_layout(sg, node_id, x1, dx1, y1, dy)

    # compute layout for nodes which are not connected to a program
    x = 60
    y = 40
    for vid in obj._filenodes.values():
        data = sg.node(vid).internal_data

        if not data.get('posx'):
            data['posx'], data['posy'] = x, y
            x+= min_dx
            compute_layout(sg, vid, x, 0, y, dy)
    # add editor


def compute_layout(sg, vid, x, dx, y, dy):
    l = list(sg.in_neighbors(vid))
    if not l:
        return
    x = x - dx/2
    dx /= len(l)
    dx = max(min_dx, dx)
    y -= dy
    for node_id in l:
        data = sg.node(node_id).internal_data
        if 'posx' in data:
            return
        data['posx'] = x
        data['posy'] = y
        x += dx
        compute_layout(sg, node_id, x, dx, y, dy)

#--------------------------------------------------------------------
# new implementation
# add files as data with editors inside.


class VlabObject2(VlabObject):

    def __init__(self, *args, **kwds):
        VlabObject.__init__(self, *args, **kwds)

    def read_files(self, f):
        pattern ='\w+\.\w+'
        for l in f:
            if 'ignore:' in l or l is '*':
                break
            fn = l.strip()
            if re.match(pattern, fn) and fn[-1] != ':':
                self._files[fn] = VlabFile(fn)

    def process_editor(self, name, command):
        """
        Find the file on which the editor works on.
        """
        cmd = ' '.join(command)
        fn = ''
        if len(command) > 1:
            fn = command[-1]
            if fn not in self._files.keys():
                print "WARNING: the file %s used by the editor %s in not in the specification file." %(fn, cmd)

        prog = command[0]
        if prog.lower() != 'edit':
            if fn and fn in self._files:
                vlabfile = self._files.get(fn)
                command[-1]="%s"
                vlabfile.editors[name]=' '.join(command)

    def process_text(self, name, command):
        pass

    def process_files(self):
        from openalea.core.data import DataFactory

        deps = self._files
        files = deps.keys()
        for f, vf in deps.iteritems():
            assert f[-1] != ':'
            fn = self.dir/f
            if fn.ext in ['.map', '.txt', '.s', '.e', '.rgb']:
                continue #binary file or other
            vf.deps = search(fn, files)

        # create the data here
        # Create vlab data rather than simple data
        self._filenodes = {}
        for vf in deps.itervalues():
            factory = DataFactory(vf.name, editors=vf.editors)
            self._package.add_factory(factory)
            self.factories.append(factory)

            # TODO: Create data rather than files
            node = factory.instantiate()
            #self.pm.get_node("vlab.bin", "vlab file stamp")
            #node.set_input(1,str(self.dir/f))
            node = self.sg.add_node(node)
            self._filenodes[vf.name] = node
            vf.node = node

    def build_graph(self):
        """
        Specify connections between nodes.
        """
        prog_deps = []
        files = self._files.keys()
        for p in self._programs:
            cmd = self.sg.node(p).inputs[1].split()
            fdeps = [f for f in files if f in cmd]
            for f in fdeps:
                fnode = self._filenodes[f]
                self.sg.connect(fnode, 0, p, 0)
        for f in files:
            for fdep in self._files[f].deps:
                depnode = self._filenodes[fdep]
                node = self._filenodes[f]
                self.sg.connect(depnode, 0, node, 2)
        #for f, nodes in self._editors.iteritems():
        #    if not f: # an editor can act withouot a file
        #        continue
        #    fnode = self._filenodes[f]
        #    for node in nodes:
        #        self.sg.connect(node,0,fnode,0)
        #for f, nodes in self._text.iteritems():
        #    fnode = self._filenodes[f]
        #    for node in nodes:
        #        self.sg.connect(fnode, 0, node, 0)
        layout(self)
        self.sg.to_factory(self.sgfactory)


# TESTS


def test1(directory):
    from openalea.core.pkgmanager import PackageManager
    pm = PackageManager()
    pm.init(verbose=False)
    obj = vlab_object(directory, pm)
    pkg = obj.get_package()
    pkg.write()
