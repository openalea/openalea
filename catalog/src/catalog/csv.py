# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
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
        print(value)
        self.pid = pid
        for i in range(len(propname)):
          val = value[i]
          if len(val) > 0:  
            try:
                val = int(val)
            except:
                try:
                    # val = value[i].replace(',','.')
                    val = float(val)
                except:
                    val = value[i]
            self.__dict__[propname[i]] = val

def parseText(text = '', separator=',', lineseparator='\n'):
        lines = text.split(lineseparator)
        propname = lines.pop(0).split(separator)
        return ([Obj(i+1,propname,l.split(separator)) for i,l in enumerate(lines)],)
