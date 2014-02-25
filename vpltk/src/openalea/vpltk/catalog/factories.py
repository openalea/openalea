# -*- python -*-
#
#       Plugin System for vpltk
# 
#       OpenAlea.VPLTk: Virtual Plants Lab Toolkit
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

from openalea.core.node import NodeFactory
from openalea.core.signature import Signature

class InterfaceFactory(NodeFactory):
    def __init__(self, interface, **kargs):
        name = interface.__name__
        description = interface.__doc__
        category='interfaces'

        if hasattr(interface, '__authors__'):
            authors = interface.__authors__
        else :
            authors = ''

        s = Signature(interface.__init__)

        super(InterfaceFactory, self).__init__(name=name,
                 description=description,
                 category=category,
                 inputs=s.parameters,
                 outputs=None,
                 authors=authors)

        self.interface = interface

    def instantiate(self):
        return self.interface


class ObjectFactory(NodeFactory):
    def __init__(self,
                 name,
                 description = '',
                 category = '',
                 interfaces=None,
                 inputs=None,
                 outputs=None,
                 nodemodule = '',
                 nodeclass = None,
                 search_path = None,
                 authors = None,
                 **kargs):
        super(ObjectFactory, self).__init__(name=name,
                 description=description,
                 category=category,
                 inputs=inputs,
                 outputs=outputs,
                 nodemodule=nodemodule,
                 nodeclass=nodeclass,
                 search_path=search_path,
                 authors=authors)

        if interfaces is None:
            self.__interfaces__ = []
        else:
            self.__interfaces__ = interfaces

    def classobj(self):
        # The module contains the node implementation.
        module = self.get_node_module()
        classobj = module.__dict__.get(self.nodeclass_name, None)

        if classobj is None:
            raise Exception("Cannot instantiate '" + \
                self.nodeclass_name + "' from " + str(module))
        return classobj

    def instantiate(self, *args, **kargs):
        classobj = self.classobj()
        return classobj(*args, **kargs)

