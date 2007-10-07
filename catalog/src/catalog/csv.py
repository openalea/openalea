# -*- python -*-
#
#       OpenAlea.Catalog.Library: OpenAlea Catalog Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): BOUDON Frederic <frederic.boudon@cirad.fr>
#                       Da SILVA David <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#



__doc__="""
Csv Nodes
"""

__license__= "Cecill-C"



class Obj:
    def __init__(self,pid,propname,value):
      #print propname
      self.pid = pid
      for i in range(len(propname)):
        try:
          val = value[i]
          if len(val) > 0:  
            try:
                val = int(val)
            except:
                try:
                    # val = value[i].replace(',','.')
                    val = float(val)
                except:
                    val = str(value[i])
            self.__dict__[propname[i].replace('"', '')] = val
        except IndexError:
          print "index : ", i, " prop : ", propname[i]

def parseText(text = '', separator=',', lineseparator='\n'):
        lines = text.split(lineseparator)
        propname = lines.pop(0).split(separator)
        objList = []
        for i, l in enumerate(lines):
          values = l.split(separator)
          if len(values) == len(propname) :
            objList.append( Obj(i+1, propname, values) )

        #return ([Obj(i+1,propname,l.split(separator)) for i,l in enumerate(lines)],)
        return (objList, )
