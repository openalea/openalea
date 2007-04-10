# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
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
Classes to create user package and Node
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


from core import Package, NodeFactory
import os


# Exceptions

class FactoryExistsError(Exception):
    pass


################################################################################

class UserPackage(Package):
    """ Package user editable and persistent """

    def __init__(self, name, metainfo, path=None):
        """ @param path : directory where to store wralea and module files """
        
        Package.__init__(self, name, metainfo)

        # package directory
        if(not path):
            import inspect
            self.path = os.path.dirname(
                os.path.abspath(inspect.stack()[1][1]))
        else:    
            self.path = path
            if(not os.path.isdir(self.path)):
                self.path = os.path.dirname(self.path)
           
        # wralea.py full path
        self.wralea_path = os.path.join(self.path, "%s_wralea.py"%(name))


    def get_wralea_path(self):
        """ Return the full path of the wralea.py (if set) """
        return self.wralea_path


    def write(self):
        """ Return the writer class """

        from persistence import PyPackageWriter
        writer = PyPackageWriter(self)

        if(not os.path.isdir(self.path)):
            os.mkdir(self.path)

        writer.write_wralea(self.wralea_path)
        

    def create_user_factory(self, name, category, description):
        """
        Return a new user factory
        This function create a new python module in the package directory
        The factory is added to the package """

        if(self.has_key(name)):
            raise FactoryExistsError()

        localdir = self.path

        # Create the module file
        template = 'from openalea.core import *\n'+\
                   '\n'+\
                   'class %s(Node):\n'%(name)+\
                   '    """  Doc... """ \n'+\
                   '\n'+\
                   '    def __init__(self):\n'+\
                   '        Node.__init__(self)\n'+\
                   '        self.add_input( name = "X", interface = None, value = None)\n'+\
                   '        self.add_output( name = "Y", interface = None) \n'+\
                   '\n'+\
                   '\n'+\
                   '    def __call__(self, inputs):\n'+\
                   '        return inputs\n'
        
        module_path = os.path.join(localdir, "%s.py"%(name))
        
        file = open(module_path, 'w')
        file.write(template)
        file.close()

        # Register the factory
        factory = NodeFactory(name=name,
                              category=category,
                              description=description,
                              nodemodule=name,
                              nodeclass=name,
                              search_path = [localdir]
                              )

        self.add_factory(factory)
        self.write()
        
        return factory


