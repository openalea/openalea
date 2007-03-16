
################################################################################
# -*- python -*-
#
#       OpenAlea.Installer :  OpenAlea installation
#
#       Copyright or © or Copr. 2006 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#          http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__doc__ = """

"""

__revision__="$Id$"
__license__="Cecill-C"

import os
import sys

class distribution:
    """ """
    
    def __init__(self, filehandler):
        """ Parse an XML distribution descriptor """

        self.packages = []



class package:
    """ A package descriptor """

    def __init__(self, name, version):

        self.name = name
        self.version = version
        
        self.author = ""
        self.description = ""
        self.copyright = ""
        self.license = ""
        
        
        self.resources = [] 
        self.dependencies = [] # list of packages



    def build_resource(self, type, url):

        type_map = { "rpm" : rpm_resource,
                     "exe" : exe_resource,
                     "pysrc" :py_src_resource,
                     }

        resource_class = type_map.get(type, None)

        if(resource_class):
            return resource_class(platform, type, url)
        else:
            return None
        

    def install(self):
        """ Try to install a package "

        # install dependencies

        # install the resource
        for r in self.resources:
            if(r.platform in sys.platform):

                try:
                    r.install()
                    return  # Install succeed
                except:
                    # Install failed : Try an other resource
                    pass
            
    

class resource:
    """ A resource on the web """
    
    def __init__(self, platform, type, url):
        self.platform = platform
        self.type = type
        self.url = url

    def download(self):
        """
        Download the resource
        Return file name if it succeeds
        Return None if it fails
        """
        
        from urllib import urlretrieve
        (tmp_filename, header ) = urlretrieve(self.url)
        return tmp_filename
        
        
    def install(self):
        """ Install the resource """
        raise RuntimeError
        


class rpm_resource(resource):

    def install(self):

        filename = self.download()
        os.system("rpm -i %s"%(filename))


class exe_resource(resource):
    
    def install(self):
        
        filename = self.download()
        os.system(filename)
            

class pysrc_resource(resource):

    def install(self):

        # Uncompress the directory

        # Execute python 
#         pythonexe = self.get_python_exe()
#         os.system(pythonexe + " setup.py install" + )





