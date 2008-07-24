# -*- python -*-
#
#       OpenAlea.Catalog
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__doc__=""" Python Nodes """
__license__= "Cecill-C"
__revision__=" $Id$ "

from openalea.core import *
import os
import operator

def py_ifelse(c=True,a=None,b=None):
    """ Return a if c is true else b """
    return bool(c) and a or b


def delitem(obj, key):
    """ call __delitem__ on obj"""
    
    ret = obj.__delitem__(key)
    return (obj,)


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


def py_getitem(obj, index):
    """ obj.__getitem__ """

    try:
        return operator.getitem(obj, index)
    except IndexError, e:
        print "getitem: Bad Index", e
        
        return None


def py_print(x):
    """ Print to the console """
    print x


def py_method(obj=None, name="", args=()):
    """ call obj.name(*args) """
    m = getattr(obj, name)
    m(*args)


def py_getattr(items, member_name):
    """__getitem on class dictionary"""
    try:
	return getattr(items, member_name)
    except:
	return None


def py_eval(str):
    """ Python eval """
    return (eval(str),)


def py_exec(str):
    """ Python exec """
    exec(str)


def py_zip(s1=(), s2=()):
    __doc__ = zip.__doc__
    return (zip(s1,s2),)


def py_flatten( l = []):
    """ Flatten nested list """
    tobeflatten = False
    for v in iter(l):
        if hasattr(v,'__iter__'):
            tobeflatten = True
            break
    if not tobeflatten:
        return (l,)
    else:
        nl = []
        for v in iter(l):
            for x in iter(py_flatten(v)[0]):
                nl.append(x)
        #print nl
        return (nl,)


def extract(indexable, keys):
    """ Extract from indexable object indexed by keys"""
    outlist = []

    for k in keys:
        try:
            outlist.append(indexable[k])
        except KeyError, IndexError:
            pass

    return (outlist,)



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
        self.connect(self, QtCore.SIGNAL("currentRowChanged(int)"), self.changed)

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
        if(not seq) : return

        if(self.mode == "DICT") : seq = seq.keys()

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
        if(item and self.mode == "DICT") : key = str(item.text())
        elif(row>=0) : key = row

        if(key):
            self.node.set_input(1, key)


