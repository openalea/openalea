"""Configuration file""" 

__license__ = "Cecill-C"
__revision__ = " $Id$"


def get_version():

    import pkg_resources
    dists = pkg_resources.require("openalea.visualea")
    return dists[0].version

url = "http://openalea.gforge.inria.fr"

def get_copyright():

    return u"Copyright \xa9 2006-2012 INRIA/CIRAD/INRA\n"
