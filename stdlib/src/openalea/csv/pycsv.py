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


def read_csv_from_file(filename=None, delimiter=' ', header=False):
    """Read CSV file

    This function reads a CSV file (see format information below).
    A delimiter can be provided (default is a space). If there is
    a header in the CSV file, it can be used if hedaer is set to True (default is False)

    The function uses the **csv** python module. Therefore, it returns
    a *csv_header* object. If the header is set to False, a list is returned.
    This list contains each row that has been read in the file. If the header is True
    then a dictionary is returned, each key correspond to a column/field.

    :Parameters:

    `filename` - input filename of a valid CSV file
    `delimiter` delimiter such as ',', ' ', ';'
    `header` - boolean to skip the first line (header)


    :Returns:

        `csv_header` object (see csv python module)

        `list` is header=False, `dict` is header=True

    :Format Information:

    While there are various specifications and implementations for the
    CSV format, there is no formal specification, which allows for a
    wide variety of interpretations of CSV files.

    We follow these rules:

     * Each record is located on a separate line, delimited by a line break::
       
           aaa,bbb,ccc
           zzz,yyy,xxx

     * There maybe an optional header line appearing as the first line
       of the file with the same format as normal record lines.
       The presence or absence of the header line should be indicated via
       the optional "header" parameter::

           field_name,field_name,field_name CRLF
           aaa,bbb,ccc CRLF
           zzz,yyy,xxx CRLF


    :Example:

        >>> csv_reader, csv_dict  = read_csv_from_file('test.csv', delimiter=' ', header=True)
        >>> csv_reader, csv_list  = read_csv_from_file('test.csv', delimiter=',', header=False)

    :Author:

        T. Cokelaer

    """
    import csv
    from os import path
    if path.exists(filename):
        csv_data = csv.reader(open(filename), delimiter=delimiter)
    else:
        IOError('%s filename does not exist' % filename)
        return (None, None)
    if header == False:
        res = []
        for r in csv_data:
            res.append(r)
    elif header == True:
        res = {}
        header = csv_data.next()
        for x in header:
            res[x] = []
        for row in csv_data:
            for h,x in zip(header, row):
                res[h].append(x)

    return (csv_data, res)


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
