# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
""" Python Nodes """

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core import *
import os
import operator


def py_ifelse(c=True, a=None, b=None):
    """ Return a if c is true else b """
    return a if bool(c) else b


def keys(obj):
    """ call keys() on obj """

    ret = obj.keys()
    return (ret,)


def values(obj):
    """ call values() on obj """

    ret = obj.values()
    return (ret,)


def items(obj):
    """ call items() on obj """

    ret = obj.items()
    return (ret,)


def pyrange(start=0, stop=0, step=1):
    """ range(start, stop, step) """

    return (range(start, stop, step),)


def pyenumerate(obj):
    """ enumerate(iterable) -> iterator for index, value of iterable """

    return (list(enumerate(obj)),)



def pylen(obj):
    """ len(obj) """

    f = len(obj)
    return ( f, )


# def py_getitem(obj, index):
    # """ obj.__getitem__ """

    # return operator.getitem(obj, index)

def py_setitem(obj, index, value):
    """ obj.__setitem__ """

    operator.setitem(obj, index, value)
    return (obj, )

def py_delitem(obj, key):
    """ call __delitem__ on obj"""
    operator.delitem(obj, key)
    return (obj,)

def py_print(x):
    """ Print to the console """
    print x
    return (x,)


def py_method(obj=None, member_name="", args=()):
    """ call obj.name(\*args) """
    m = getattr(obj, member_name)
    m(*args)
    return obj


def py_getattr(items, member_name):
    """ getattr """
    return getattr(items, member_name)

def py_setattr(obj, member_name, value_str):
    setattr(obj, member_name, eval(value_str))
    return obj,

def py_eval(str):
    """ Python eval """
    return (eval(str),)


def py_exec(str):
    """ Python exec """
    l= {}
    exec(str, globals(),l)
    return l,

def py_zip(s1=(), s2=()):
    __doc__ = zip.__doc__
    return (zip(s1, s2),)

def py_zip2(args):
    __doc__ = zip.__doc__
    return (zip(*args),)

def py_flatten(obj=[]):
    """ Flatten nested list """
    tobeflatten = False
    for v in iter(obj):
        if hasattr(v,'__iter__'):
            tobeflatten = True
            break
    if not tobeflatten:
        return (obj,)
    else:
        nl = []
        for v in iter(obj):
            for x in iter(py_flatten(v)[0]):
                nl.append(x)
        #print nl
        return (nl,)


class PyGetItem(Node):

    def __call__(self, inputs):
        """ Python __getitem__ method like obj[key] """
        obj, key = inputs[0:2]
        if isinstance(obj, dict):
            if obj and (key not in obj):
                key = obj.iterkeys().next()
                # send an event to the node to set the 2nd inputs
                self.set_input(1,key)
            return obj[key],
        else:
            return obj[key],

def extract(indexable, keys):
    """ Extract from indexable object indexed by keys"""
    outlist = []

    for k in keys:
        try:
            outlist.append(indexable[k])
        except KeyError, IndexError:
            pass

    return (outlist,)

def pysum(sequence):
    return (sum(sequence), )

def pymean(sequence):
    return (sum(sequence)/float(len(sequence)), )

# DEPRECATED

def py_fwrite(x="", filename="", mode="w"):
    """ Write to a file """

    print "This node is DEPRECATED. Use %s instead"%("Catalog.File.write")
    f = open(filename, mode)
    f.write(x)
    f.close()


class FileRead(object):
    """ Read a file """

    def __init__(self):

        self.mtime = 0 # modification time
        self.filename = ''
        self.s = ''

    def __call__(self, filename=""):

        print "This node is DEPRECATED. Use %s instead"%("Catalog.File.read")
        try:
            mtime = os.stat(filename).st_mtime
        except:
            mtime = 0

        if(filename != self.filename or
           mtime != self.mtime):

            self.filename = filename
            self.mtime = mtime

            f = open(filename, 'r')
            self.s = f.read()
            f.close()

        return self.s

################################################################################
# Widgets

from openalea.visualea.node_widget import NodeWidget
from openalea.core.observer import lock_notify

from PyQt4 import QtGui, QtCore

class ListSelectorWidget(QtGui.QListWidget, NodeWidget):
    """ This Widget allows to select an element in a list
    or in a dictionnary """

    def __init__(self, node, parent):
        """
        @param node
        @param parent
        """

        QtGui.QListWidget.__init__(self, parent)
        NodeWidget.__init__(self, node)
        self.connect(self, QtCore.SIGNAL("currentRowChanged(int)"),
                     self.changed)

        self.mode = None
        self.notify(node, ("input_modified", 0))
        self.notify(node, ("input_modified", 1))


    def notify(self, sender, event):
        """ Notification sent by node """

        if(event[0] != "input_modified"): return

        # Read Inputs
        seq = self.node.get_input(0)

        index = self.node.get_input(1)

        if(event[1] == 0): # index of modified input

            # Define the mode depending of the type of input
            if(isinstance(seq, dict)) :
                self.mode = "DICT"
            else :
                self.mode = None

            self.update_list(seq)

        elif(event[1] == 1): # index == 1

            if(self.mode == "DICT"):
                try:
                    i = seq.keys().index(index)
                    self.setCurrentRow(i)
                except:
                    pass
            else:
                try:
                    self.setCurrentRow(index)
                except: pass


    def update_list(self, seq):
        """ Rebuild the list """

        self.clear()
        if(not seq):
            return

        if(self.mode == "DICT"):
            seq = seq.keys()

        for elt in seq :

            item = QtGui.QListWidgetItem(str(elt))
            item.setFlags(QtCore.Qt.ItemIsEnabled|
                          QtCore.Qt.ItemIsSelectable)
            self.addItem(item)


    @lock_notify
    def changed(self, p):
        """ Update the index"""

        row = self.currentRow()
        item = self.currentItem()

        key = None
        if (item and self.mode == "DICT"):
            key = str(item.text())
        elif row >= 0:
            key = row

        if key is not None:
            self.node.set_input(1, key)


