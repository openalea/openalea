# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
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
__revision__ = "$Id: $"

from path import path
from openalea.vpltk.project.project import check_unicity

class Scripts(dict):
    """ Hack if we works outside of project
    
    This "fake project" respond to a part of the api of Project (vpltk.project.project)
    """
    def __init__(self):
        super(Scripts, self).__init__()
        """
        name is a dict complete_name_of_file : short_name_of_file
        ez_name is a dict short_name_of_file : complete_name_of_file
        name is used to know were is the file
        ez_name is used to display a short name in editor
        """
        self.ez_name = dict()
        self.name = dict()
        self.controls = dict()
        
    def add_script(self, name, script):
        self[str(name)] = str(script)
        
        # easy_name is used to display file_name
        # Thanks to self.ez_name, we can found the real name to save file.
        ez_n = str(path(name).splitpath()[-1])
        ez_n = check_unicity(name=ez_n, all_names=self.ez_name.values())
        self.ez_name[ez_n] = name
        self.name[name] = ez_n

    def get_ez_name_by_name(self, name):
        name = str(name)
        if name in self.name.keys(): 
            return self.name[name]
        else:           
            return False   
        
    def get_name_by_ez_name(self, ez_name):
        ez_name = str(ez_name)
        if ez_name in self.ez_name.keys():        
            return self.ez_name[ez_name]
        else:
            return False
                
    def rm_script(self,name):
        name = str(name)
        if name in self.keys():
            del self[name]
            ez_name = str(self.name[name])
            del self.ez_name[ez_name]
            del self.name[name]
            
    def rm_script_by_ez_name(self,ez_name):
        ez_name = str(ez_name)
        if ez_name in self.ez_name.keys():
            self.rm_script(self.ez_name[ez_name])
            
    def rename_script(self, old_name, new_name):
        old_name = str(old_name)
        new_name = str(new_name)
        self.add_script(new_name, self[old_name])
        self.rm_script(old_name)
        
    def is_project(self):
        return False
        
    def is_script(self):
        return True

    def __repr__(self):
        return "Scripts short-named " + str(self.name.values()) + " . Complete names: " + str(self.name.keys())
