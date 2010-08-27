# -*- python -*-
#
#       OpenAlea.Deploy: OpenAlea setuptools extension
#
#       Copyright 2008 INRIA - CIRAD - INRA  
#
#       File author(s): Thomas Cokelae
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

"""INRIA GForge SOAP python API wrappers (based on SOAPpy)

"""
from os.path import join as pj

__license__ = "Cecill-C"
__revision__ = " $Id: gforge.py 2243 2010-02-08 17:08:47Z cokelaer $ "

def get_shared_data_path(package_path, filename=None, share_path=pj('share','data')):
    """Return a valid pathname pointing to shared-data directory

    In a package, the shared data are expected to be found in `./share/data`.

    :param package_path: a list of paths as provided within an __init__ file
        by the variable __path__
    :param filename: an optional valid filename without any path that is expected
        to be found in the directory __path__[0]/share/data

    :return: a valid pathname if filename is not provided and a valid path to 
        filename (including filename) otherwise. If no valid path is found, returns 
        nothing and raise an exception.
       


       >>> get_shared_data_path(['/home/user/mypackage'])
       '/home/user/mypackage/share/data'
       >>> get_shared_data_path(['/home/user/mypackage'], mypath='share/databases')
       '/home/user/mypackage/share/databases'
    """
    from os.path import join, realpath, isdir
    # in develop mode, we need to move in the tree directory one 
    # more time than in install mode

    ff = pj( package_path[0], '..', '..', share_path)
    ff = realpath(ff)
    if isdir(ff) is False:
       ff = pj(package_path[0], '..', '..', '..', share_path)
       ff = realpath(ff)
       if isdir(ff) is False:
           raise IOError('Could not find share/data directory make sure first argument is a valid path.')

    if filename==None:
        return ff
    else:
        from os.path import isfile
        ff = pj(ff, filename)
        if isfile(ff):
            return realpath(ff)
        else:
            raise IOError("%s not found. Check the filename." % ff)
