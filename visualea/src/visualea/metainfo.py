"""Configuration file""" 

__license__ = "Cecill-C"
__revision__ = " $Id: metainfo.py 2000 2009-12-04 18:28:18Z dbarbeau $"


def get_version():

    import pkg_resources
    dists = pkg_resources.require("openalea.visualea")
    return dists[0].version

url = "http://openalea.gforge.inria.fr"

def get_copyrigth():

    return u"Copyright \xa9  2006-2009 INRIA - CIRAD - INRA\n"
