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
###############################################################################
"""CSV Nodes"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


class Obj(object):

    def __init__(self, pid, propnames, values):
        """ todo"""
        self.pid = pid
        self.read(propnames, values)

    def read(self, propnames, values):
        """todo"""
        for i, prop in enumerate(propnames):
            try:
                val = values[i]
                if len(val) > 0:
                    try:
                        val = int(val)
                    except:
                        try:
                            # val = value[i].replace(',','.')
                            val = float(val)
                        except:
                            val = str(values[i])
                    self.__dict__[prop.replace('"', '')] = val
            except IndexError:
                print "index : ", i, " prop : ", propnames[i]

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def merge_header(self, propname):
        return propname.union(set(self.__dict__.keys()))

    def write(self, propnames, separator=','):
        res = ''
        nbprop = len(propnames)
        for i, prop in enumerate(propnames):
            if hasattr(self, prop):
                v = self.__dict__[prop]
                if type(v) == str:
                    res += '"'+v+'"'
                else:
                    res += str(v)
            if i < nbprop-1:
                res += separator
        return res

    def __repr__(self):
        res = 'Obj('
        nbprop = len(self.__dict__)
        if nbprop:
            propid = 0
            for key, val in self.__dict__.iteritems():
                res += str(key) + '=' + str(val)
                propid += 1
                if propid < nbprop:
                    res += ','
        res += ')'
        return res


def parseText(text = '', separator=',', lineseparator='\n'):
    lines = text.split(lineseparator)
    propname = lines.pop(0).split(separator)
    objList = []
    for i, l in enumerate(lines):
        values = l.split(separator)
        if len(values) == len(propname):
            objList.append(Obj(i+1, propname, values))

    #return ([Obj(i+1,propname,l.split(separator)) for i,l in enumerate(lines)],)
    return (objList, propname)


def writeObjs(objects, separator=',', lineseparator='\n'):
    res = ''
    propnames = set()
    for obj in objects:
        propnames = obj.merge_header(propnames)
    nbprop = len(propnames)
    for i, prop in enumerate(propnames):
        if type(prop) == str:
            res += '"'+prop+'"'
        else:
            res += str(prop)
        if i < nbprop -1:
            res += separator
    res += lineseparator
    for obj in objects:
        res += obj.write(propnames, separator)
        res += lineseparator
    return (res, )
